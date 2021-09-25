from collections import Counter
from json import JSONEncoder


class OperationsReport():
    def __init__(self, key, fname='test') -> None:
        self.name = key
        self.amounts = Counter()
        self.total_amounts = 0
        self.children = {}

    def add_row(self, path, date, total_sum):
        self.amounts[date] += total_sum
        self.total_amounts += total_sum

        if path:
            key = path.pop(0)
            child = self.children.get(key)
            if not child:
                child = self.children[key] = OperationsReport(key)
            child.add_row(path, date, total_sum)

    # f"{[round(x, 2) for x in self.amounts.values()]}"
    def to_json(self):
        json_dict = {
            'name': self.name,
            'amounts': str([
                round(x[1], 2)
                for x in sorted(self.amounts.items(), key=lambda k: k[0])
            ]),
            'total_amounts': round(self.total_amounts, 2),
        }
        if list(self.children.values()):
            json_dict['children'] = list(self.children.values())
        return json_dict

    def set_zeros(self, dates):
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
