from datetime import date
import json
from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql.expression import join

from ShoppingAPIService import operations

from ..config import Settings, get_settings
from ..database import Session, get_session
from ..accounts.models import Account
from ..shops.models import Shop
from ..categories.models import Category
from ..exseptions import EntiyUnprocessableError
from .models import Operation
from .schemas import OperationRequest
from .report import OperationsReport, OperationsJSONEncoder


class OperationsServices():
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def add_operation(self, new_operation: OperationRequest) -> Operation:
        if not self._validate_operation_data(new_operation):
            raise EntiyUnprocessableError
        operation = Operation(
            type=new_operation.type,
            date=date.fromisoformat(new_operation.date),
            shop_id=new_operation.shop_id,
            category_id=new_operation.category_id,
            name=new_operation.name,
            price=new_operation.price,
            amount=new_operation.amount,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def _validate_operation_data(self, operation: OperationRequest) -> bool:
        if not operation.type.lower() in ['sale', 'buy']:
            return False
        if not operation.shop_id:
            return False
        if not operation.name:
            return False
        if not operation.price or not operation.amount:
            return False
        return True

    def get_operations(
        self,
        current_user: Account,
        *,
        date_from: Optional[str],
        date_to: Optional[str],
        shops: Optional[List[int]],
        categories: Optional[List[int]],
    ) -> List[Operation]:
        operations_query = self.session.query(Operation)\
                                        .join(Operation.category)\
                                        .join(Operation.shop)\
                                        .join(Shop.account)\
                                        .filter(Account.id == current_user.id)
        if date_from:
            operations_query = operations_query\
                               .filter(Operation.date >= date.fromisoformat(date_from))
        if date_to:
            operations_query = operations_query\
                               .filter(Operation.date <= date.fromisoformat(date_to))
        if shops:
            operations_query = operations_query.filter(Operation.shop_id.in_(shops))
        if categories:
            operations_query = operations_query.filter(Operation.shop_id.in_(categories))

        return operations_query.all()

    def get_report(
        self,
        current_user: Account,
        *,
        date_from: Optional[str],
        date_to: Optional[str],
        shops: Optional[List[int]],
        categories: Optional[List[int]],
    ):
        operations_data = self.get_operations(
            current_user,
            date_from=date_from,
            date_to=date_to,
            shops=shops,
            categories=categories,
        )

        report = {
            'buy': OperationsReport('Покупки'),
            'sale': OperationsReport('Продажи'),
        }

        for operation in operations_data:
            type = str(operation.type)
            o_date = date.isoformat(operation.date)
            path = [str(operation.shop), str(operation.category), str(operation.name)]
            total_sum = float(operation.amount * operation.price)

            report[type].add_row(path, o_date, total_sum)
        json_data = json.dumps(
            report,
            indent=4,
            cls=OperationsJSONEncoder,
            ensure_ascii=False,
        )

        return json.loads(json_data)
