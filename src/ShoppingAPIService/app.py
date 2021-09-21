from fastapi import FastAPI

from .accounts import api as accounts_api
from .categories import api as categories_api
from .operations import api as operations_api
from .shops import api as shops_api


app = FastAPI()


accounts_api.initialize_app(app)
categories_api.initialize_app(app)
operations_api.initialize_app(app)
shops_api.initialize_app(app)
