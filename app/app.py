from flask import Flask, request
from data.bakery_db import categories, products

app = Flask(__name__)


## GET Requests


# Category


@app.get("/category")
def get_categories():
    """
    Retrieves all categories from the bakery.

    Returns:
        categories: The specified category.

    Response Codes:
        200: Successful Request.
    """
    return {"categories": categories}, 200


@app.get("/category/{category_id}")
def get_category_by_id(category_id):
    """
    Retrieves a specific category by its ID.

    Parameters:
    category_id (integer): category identifier.

    Returns:
        category: The specified category.

    Response Codes:
        200: Successful Request.
        400: The category ID given does not exist/did not fetch anything.
    """
    try:
        return categories[category_id], 200
    except KeyError:
        return 404


# Product


@app.get("/product")
def get_products():
    """
    Retrieves all products from the bakery.

    Returns:
        products: The specified category.

    Response Codes:
        200: Successful Request.
    """
    return {"products": products}, 200


## POST Requests

# Category


@app.post("/category")
def create_category():
    request_data = request.get_json()

    new_category = {
        "category_id": (max(categories.keys()) + 1),
        "category_name": request_data["category_name"],
    }
    categories.append(new_category)
    return new_category, 201
