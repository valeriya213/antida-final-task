from collections import Counter
from datetime import date
from json import JSONEncoder
from operator import attrgetter
from typing import Union


class OperationsReport():
    def __init__(self, key: str):
        self.name = key
        self.amounts = Counter()
        self.total_amounts = 0
        self.children = {}

    def add_row(
        self,
        path: list,
        date: Union[str, date],
        total_sum: Union[float, int]
    ):
        self.amounts[date] += total_sum
        self.total_amounts += total_sum

        if path:
            key = path.pop(0)
            child = self.children.get(key)
            if not child:
                child = self.children[key] = OperationsReport(key)
            child.add_row(path, date, total_sum)

    def to_json(self) -> dict:
        json_dict = {
            'name': self.name,
            'amounts': str([
                round(x[1], 2)
                for x in sorted(self.amounts.items(), key=lambda k: k[0])
            ]),
            'total_amounts': round(self.total_amounts, 2),
        }
        if list(self.children.values()):
            json_dict['children'] = sorted(
                list(self.children.values()),
                key=attrgetter('total_amounts'),
                reverse=True,
            )
        return json_dict

    def set_zeros(self, dates: 'list[Union[str, date]]'):
        for date in dates:
            self.amounts.setdefault(date, 0)
        if self.children:
            for child in self.children.keys():
                self.children[child].set_zeros(dates)


class OperationsJSONEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        elif isinstance(obj, set):
            return f'{sorted(list(obj))}'
        return obj
