from flask import Flask, request
from data.bakery_db import categories, products

app = Flask(__name__)


## GET Requests


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


@app.get("/product/<int:product_id>")
def get_product_by_id(product_id):
    """
    Retrieves a specific product by its ID.

    Parameters:
    product_id (integer): product identifier.

    Returns:
        product: The specified category.

    Response Codes:
        200: Successful Request.
        400: The product ID given does not exist/did not fetch anything.
    """
    try:
        return products[product_id], 200
    except KeyError:
        return {"message: Product not found or does not exist"}, 404


## POST Requests


@app.post("/category")
def create_category():
    """
    Creates a new category in the bakery.

    Request Body:

    The JSON representation of the new category
    Example:
        {
            "category_name": "Cakes"
        }

    Returns:
        new_category: The newly created category.

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

    new_category_id = max(categories.keys()) + 1

    new_category = {**request_data, "category_id": new_category_id}

    categories[new_category_id] = new_category

    return new_category, 201


@app.post("/product")
def create_product():
    """
    Creates a new product in the bakery.

    Request Body:

        The JSON representation of the new category
        Example:
        {
        "category_id": 3,
        "product_code": "cnrP",
        "product_name": "Cinnamon Raisin Roll",
        "price": 1.09
        }

    Returns:
        new_product: The newly created product.

    Response Codes:
        200: Successful Request.
        400: The JSON payload does not contain the product name or the given product name exists already.
    """
    request_data = request.get_json()
    required_fields = ["category_id", "product_code", "product_name", "price"]

    for field in required_fields:
        if field not in request_data:
            return {
                "message": "The request failed because the JSON payload does not contain all name-value pairs as specified in the above example."
            }, 400
    for product in products.values():
        if request_data["product_code"] == product["product_code"]:
            return {
                "message": "The request failed because the given product_code exists already."
            }, 400
    for category in categories.values():
        if request_data["category_id"] not in categories:
            return {
                "message": "The request failed because the given category_id doesn't exists or wasn't found."
            }, 400

    new_product_id = max(products.keys()) + 1
    new_product = {**request_data, "product_id": new_product_id}
    products[new_product_id] = new_product

    return new_product, 201


## DELETE requests


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


@app.delete("/product/<int:product_id>")
def delete_product(product_id):
    """
    Deletes a product from the bakery.

    Params:
        product_id (integer): product identifier

    Response Codes:
        200: Successful Request.
        404: the given product identifier does not exist
    """
    try:
        del products[product_id]
        return {"message": "Product deleted"}, 200
    except KeyError:
        return {"message": "Product not found"}, 404


# PUT Requests


@app.put("/product/<int:product_id>")
def update_product(product_id):
    """
    Updates a product in the bakery.

    Request Body:

        The JSON representation of the new category
        Example:
        {
        "category_id": 3,
        "product_code": "cnrP",
        "product_name": "Cinnamon Raisin Roll",
        "price": 1.09
        }

    Returns:
        updated_product: The updated or new product.

    Response Codes:
        200: The existing product was updated.
        201: The product was created
        400: The JSON payload does not contain the product name or the given product name exists already.
    """
    request_data = request.get_json()
    required_fields = ["category_id", "product_code", "product_name", "price"]

    for field in required_fields:
        if field not in request_data:
            return {
                "message": "The request failed because the JSON payload does not contain all name-value pairs as specified in the above example."
            }, 400
    for category in categories.values():
        if request_data["category_id"] not in categories:
            return {
                "message": "The request failed because the given category_id doesn't exists or wasn't found."
            }, 400

    if product_id in products:
        existing_product = products[product_id]
        existing_product.update(**request_data)
        return existing_product, 200
    else:
        create_product()
        return {"message": "New product created"}, 201
