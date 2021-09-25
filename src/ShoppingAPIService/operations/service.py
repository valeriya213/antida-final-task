from datetime import date
import json
from typing import List
from fastapi import Depends

from ..config import Settings, get_settings
from ..database import Session, get_session
from ..accounts.models import Account
from ..shops.models import Shop
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
        quary_params: QueryParams,
    ) -> List[Operation]:
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
            o_query = o_query.filter(Operation.shop_id.in_(quary_params.shops))
        if quary_params.categories:
            o_query = o_query.filter(Operation.shop_id.in_(quary_params.categories))

        return o_query.all()

    def get_report(
        self,
        current_user: Account,
        quary_params: QueryParams,
    ):
        operations_data = self.get_operations(
            current_user,
            quary_params,
        )

        report = {
            'time_points': set(),
            'buy': OperationsReport('Покупки'),
            'sale': OperationsReport('Продажи'),
        }

        for operation in operations_data:
            type = str(operation.type)
            o_date = date.isoformat(operation.date.replace(day=1))
            path = [
                str(operation.shop.name),
                str(operation.category.name),
                str(operation.name),
            ]
            total_sum = float(operation.amount * operation.price)

            report['time_points'].add(o_date)
            report[type].add_row(path, o_date, total_sum)

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
