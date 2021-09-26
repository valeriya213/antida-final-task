import json
from datetime import date
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Query
from typing import List

from ..config import Settings, get_settings
from ..database import Session, get_session
from ..accounts.models import Account
from ..shops.models import Shop
from ..categories.models import Category
from ..exseptions import EntiyUnprocessableError
from .models import Operation
from .schemas import OperationRequest
from .report import OperationsReport, OperationsJSONEncoder
from .queryparams import QueryParams


class OperationsServices():
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def add_operation(
        self,
        new_operation: OperationRequest,
        current_user: Account,
    ) -> Operation:
        if not self._validate_operation_data(
            new_operation,
            current_user
        ):
            raise EntiyUnprocessableError

        operation = Operation(
            type=new_operation.type,
            date=new_operation.date,
            shop_id=new_operation.shop_id,
            category_id=new_operation.category_id,
            name=new_operation.name,
            price=new_operation.price,
            amount=new_operation.amount,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def _validate_operation_data(
        self,
        operation: OperationRequest,
        current_user: Account,
    ) -> bool:
        if not operation.type.lower() in ['sale', 'buy']:
            return False

        if operation.shop_id not in self._get_account_shops(current_user):
            return False
        if operation.category_id\
           and operation.category_id not in self._get_account_categories(current_user):
            return False
        return True

    def _get_account_shops(self, current_user: Account) -> list:
        return self.session.execute(
            select(Shop.id)
            .where(
                Shop.account_id == current_user.id,
            )
        ).scalars().all()

    def _get_account_categories(self, current_user: Account) -> list:
        return self.session.execute(
            select(Category.id)
            .where(
                Category.account_id == current_user.id,
            )
        ).scalars().all()

    def get_operations(
        self,
        current_user: Account,
        quary_params: QueryParams,
    ) -> List[Operation]:
        o_query = self._get_operations(
            current_user,
            quary_params,
        )
        return o_query.all()

    def _get_operations(
        self,
        current_user: Account,
        quary_params: QueryParams,
    ) -> Query:
        o_query = self.session.query(Operation)\
                              .join(Operation.category)\
                              .join(Operation.shop)\
                              .join(Shop.account)\
                              .filter(Account.id == current_user.id)
        if quary_params.date_from:
            o_query = o_query\
                      .filter(Operation.date >= quary_params.date_from)
        if quary_params.date_to:
            o_query = o_query\
                      .filter(Operation.date <= quary_params.date_to)
        if quary_params.shops:
            o_query = o_query\
                      .filter(Operation.shop_id.in_(quary_params.shops))
        if quary_params.categories:
            o_query = o_query\
                      .filter(Operation.shop_id.in_(quary_params.categories))
        return o_query

    def get_report(
        self,
        current_user: Account,
        quary_params: QueryParams,
    ):
        operations_data = self._get_operations(
            current_user,
            quary_params,
        ).order_by(Operation.date).all()

        report = {
            'time_points': set(),
            'buy': OperationsReport('Покупки'),
            'sale': OperationsReport('Продажи'),
        }

        for operation in operations_data:
            o_type = str(operation.type)
            o_date = date.isoformat(operation.date.replace(day=1))
            path = [
                str(operation.shop.name),
                str(operation.category.name),
                str(operation.name),
            ]
            total_sum = float(operation.amount * operation.price)

            report['time_points'].add(o_date)
            report[o_type].add_row(path, o_date, total_sum)

        report['buy'].set_zeros(report['time_points'])
        report['sale'].set_zeros(report['time_points'])

        return json.loads(
            json.dumps(
                report,
                indent=4,
                cls=OperationsJSONEncoder,
                ensure_ascii=False,
            )
        )
