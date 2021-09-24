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

    def to_json(self):
        json_dict = {
            'name': self.name,
            'amounts': f"{list(self.amounts.values())}",
            'total_amounts': round(self.total_amounts, 2),
        }
        if list(self.children.values()):
            json_dict['children'] = list(self.children.values())
        return json_dict


class OperationsJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, "to_json"):
            return self.default(o.to_json())
        elif hasattr(o, "__dict__"):
            return o.__dict__
        return o
