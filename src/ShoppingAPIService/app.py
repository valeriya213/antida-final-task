from fastapi import FastAPI

from .accounts import api as accounts_api
from .categories import api as categories_api
from .operations import api as operations_api
from .shops import api as shops_api


description = """
API service for accounting for sales and buys

## Accounts
You can create an account and log in to work with the API.

## Categories
You can:
* **Create** a category
* **Edit** a category
* **Read** all categories
* **Delete** a category

## Operations
You can:
* **Entering information about a product operation** (buy or sale) in a certain shop
* **Getting a list of operations** for a certain period with the ability to filter
* **Formation of a monthly report** on commodity operations for a certain period with the possibility of filtering

## Shops
You can:
* **Create** a shop
* **Edit** a shop
* **Read** all shops
* **Delete** a shop
"""

tags_metadata = [
    {
        'name': 'Accounts',
        'description': 'Account registration and authorization',
    },
    {
        'name': 'Categories',
        'description': 'Create, read, edit, and delete categories',
    },
    {
        'name': 'Operations',
        'description': 'Work with commodity operations',
    },
    {
        'name': 'Shops',
        'description': 'Create, read, edit, and delete shops',
    },
]


app = FastAPI(
    title='ShoppingAPIService',
    description=description,
    openapi_tags=tags_metadata,
)


accounts_api.initialize_app(app)
categories_api.initialize_app(app)
operations_api.initialize_app(app)
shops_api.initialize_app(app)
