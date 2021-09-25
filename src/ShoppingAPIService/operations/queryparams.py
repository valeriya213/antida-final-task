from datetime import date
from fastapi import HTTPException
from fastapi import status
from fastapi import Request


class QueryParams:
    def __init__(self, date_from, date_to, shops, categories):
        self.date_from = date_from
        self.date_to = date_to
        self.shops = shops
        self.categories = categories

    @property
    def date_from(self):
        return self._date_from

    @date_from.setter
    def date_from(self, date_from: str):
        if not date_from:
            self._date_from = None
            return

        try:
            self._date_from = date.fromisoformat(date_from)
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

    @property
    def date_to(self):
        return self._date_to

    @date_to.setter
    def date_to(self, date_to):
        if not date_to:
            self._date_to = None
            return

        try:
            self._date_to = date.fromisoformat(date_to)
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

    @property
    def shops(self):
        return self._shops

    @shops.setter
    def shops(self, shops):
        if not shops:
            self._shops = None
            return
        self._shops = [
            int(x) for x in shops.split(',') if x.isdigit()
        ]
        if shops and not self._shops:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        if not categories:
            self._categories = None
            return
        self._categories = [
            int(x) for x in categories.split(',') if x.isdigit()
        ]
        if categories and not self._categories:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)


def get_query_params(request: Request):
    return QueryParams(
        date_from=request.query_params.get('date_from'),
        date_to=request.query_params.get('date_to'),
        shops=request.query_params.get('shops'),
        categories=request.query_params.get('categories'),
    )
