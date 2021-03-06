import json
from datetime import date
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Query
from typing import List

from ..database import Session, get_session
from ..exseptions import EntiyUnprocessableError
from ..accounts.models import Account
from ..categories.models import Category
from ..shops.models import Shop
from .models import Operation
from .report import OperationsReport, OperationsJSONEncoder
from .schemas import OperationRequest
from .queryparams import QueryParams


class OperationsServices():
    def __init__(
        self,
        session: Session = Depends(get_session),
    ):
        self.session = session

    def add_operation(
        self,
        new_operation: OperationRequest,
        current_user: Account,
    ) -> Operation:
        if not self._validate_operation_data(
            new_operation,
            current_user,
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
                      .filter(Operation.category_id.in_(quary_params.categories))
        return o_query

    def get_report(
        self,
        current_user: Account,
        quary_params: QueryParams,
    ) -> dict:
        operations_data = self._get_operations(
            current_user,
            quary_params,
        ).order_by(Operation.date).all()

        report = self._get_report(operations_data)
        self._set_correct_dates_in_report(quary_params, report)

        return json.loads(
            json.dumps(
                report,
                indent=4,
                cls=OperationsJSONEncoder,
                ensure_ascii=False,
            )
        )

    def _set_correct_dates_in_report(
        self,
        quary_params: QueryParams,
        report: dict,
    ):
        min_date = quary_params.date_from or \
            date.fromisoformat(min(report['time_points']))
        max_date = quary_params.date_to or \
            date.fromisoformat(max(report['time_points']))

        while min_date <= max_date:
            report['time_points'].add(min_date.isoformat())
            next_month = min_date.month + 1
            min_date = date(
                min_date.year + (next_month-1) // 12,
                (next_month - 1) % 12 + 1,
                1,
            )
        self._set_zeros_for_new_dates(report)

    def _set_zeros_for_new_dates(self, report: dict):
        report['buy'].set_zeros(report['time_points'])
        report['sale'].set_zeros(report['time_points'])

    def _get_report(self, operations_data) -> dict:
        report = {
            'time_points': set(),
            'buy': OperationsReport('??????????????'),
            'sale': OperationsReport('??????????????'),
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
        return report
