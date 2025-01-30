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


@app.get("/category/<int:category_id>")
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
        return {"message:Category not found or does not exist"}, 404


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
    """
    Creates a new category in the bakery.

    Returns:
        products: The newly created category.

    Response Codes:
        200: Successful Request.
        400: The JSON payload does not contain the category name or the given category name exists already.
    """
    request_data = request.get_json()

    if "category_name" not in request_data:
        return {"message": "Request must include 'category_name' field"}

    for category in categories.values():
        if request_data["category_name"] == category["category_name"]:
            return {"message": "Category already exists"}, 400

    category_id = max(categories.keys()) + 1

    newer_category = {**request_data, "category_id": category_id}

    categories[category_id] = newer_category

    return newer_category


## DELETE requests

# Category


@app.delete("/category/<int:category_id>")
def delete_category(category_id):
    """
    Deletes a category from the bakery.

    Params:
        category_id (integer): category identifier

    Response Codes:
        200: Successful Request.
        400: the category is not deleted because there are products associated with the given category
        404: the given category identifier does not exist
    """
    for product in products.values():
        if category_id == product["category_id"]:
            return {
                "message": "Category cannot be deleted due to having products associated with it"
            }, 400

    try:
        del categories[category_id]
        return {"message": "Category deleted"}, 200
    except KeyError:
        return {"message": "Category not found"}, 404
