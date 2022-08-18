import json

import requests




def get_location_id():
    return location_id


def get_product_id(product):
    return product["product"]["id"]


def get_image_id(image):
    return image["image"]["id"]


def get_variant_id(variant):
    return variant["variant"]["id"]


def check_duplicate_product(isbn):
    """
    Check if a product with the given isbn already exists in the shopify store.
        Param : isbn : str : The isbn of the product to check.
        Return : bool : True if the product already exists, False if not.
    """
    product_url = store_url + "/products.json"
    response = requests.get(product_url, headers=headers)
    products = response.json()["products"]
    for product in products:
        if product["variants"][0]["sku"] == isbn:
            return True
    return False


def create_new_product(product: dict):
    """
    Add a new product to the shopify store.
        Param : new_product : dict : The product to add which should include:
        Return : json : The product id
    """
    data = json.dumps(product)
    product_url = store_url + "/products.json"
    response = requests.post(product_url, data=data, headers=headers)
    print(response.json())
    return response.json()


def create_new_image(product_id: int, image: dict):
    """
    Add a new image to the shopify store for given product_id.
        Param : product_id : int : The id of the product to add the image to.
        Param : image : dict : The image to add which should include:
        Return : json : The image id
    """
    data = json.dumps(image)
    image_url = store_url + "/products/" + str(product_id) + "/images.json"
    response = requests.post(image_url, data=data, headers=headers)
    print(response.json())
    return get_image_id(response.json())


def create_new_variants(product_id: int, variants: dict):
    """
    Add a new variant to the shopify store for given product_id.
        Param : product_id : int : The id of the product to add the variant to.
        Param : variant : dict : The variant to add which should include:
        Return : int : The inventory item id of the variant that was added.
    """
    data = json.dumps(variants)
    variants_url = store_url + "/api/2022-07/products/" + str(product_id) + "/variants.json"
    response = requests.post(variants_url, data=data, headers=headers)
    print(response.json())
    return get_inventory_item_id(response.json())


def create_new_inventory_item(inventory_item: dict):
    """
    Add a new inventory item to the shopify store for given product_id.
        Param : inventory_item : dict : The inventory item to add which should include:
        Return : json : The inventory item that was added.
    """
    data = json.dumps(inventory_item)
    inventory_item_url = store_url + "/api/2022-07/inventory_levels/adjust.json"
    response = requests.post(inventory_item_url, data=data, headers=headers)
    print(response)


def get_variant(product_id, variant_id):
    """
    Get a variant from the shopify store for given product_id.
        Param : product_id : int : The id of the product to get the variant from.
        Param : variant_id : int : The id of the variant to get.
        Return : json : The variant that was found.
    """
    variant_url = store_url + "/api/2022-07/products/" + str(product_id) + "/variants/" + str(variant_id) + ".json"
    response = requests.get(variant_url, headers=headers)
    return response.json()


def update_option(product_id: int):
    """
    Update the option of a product in the shopify store.
        Param : product_id : int : The id of the product to update.
        Return : json : The product that was updated.
    """
    product_url = store_url + "/products/" + str(product_id) + ".json"
    response = requests.get(product_url, headers=headers)
    product = response.json()
    # check if variants exist
    if not product["product"]["variants"]:
        return False
    product["product"]["options"] = [
        {"name": "Bokformat", "values": ["Bokformat"]}
    ]
    data = json.dumps(product)
    response = requests.put(product_url, data=data, headers=headers)
    return response.json()


def update_variants(product_id: int, variants: dict):
    """
    Update the variants of a product in the shopify store.
        Param : product_id : int : The id of the product to update.
        Param : variants : dict : The variants to update which should
        include:
        Return : int : variant id .
    """
    product_url = store_url + "/products/" + str(product_id) + ".json"
    response = requests.get(product_url, headers=headers)
    product = response.json()
    product["product"]["variants"] = variants
    data = json.dumps(product)
    response = requests.put(product_url, data=data, headers=headers)
    return response.json()


def get_all_products():
    """
    Get all products from the shopify store.
        Return : json : The products that were found.
    """
    product_url = store_url + "/products.json"
    response = requests.get(product_url, headers=headers)
    return response.json()["products"]


def update_product(product_id: int, product: dict):
    """
    Update a product in the shopify store.
        Param : product_id : int : The id of the product to update.
        Param : product : dict : The product to update which should
        Return : json : The product that was updated.
    """
    product = json.dumps(product)
    product_url = store_url + "/api/2022-07/products/" + str(product_id) + ".json"
    response = requests.put(product_url, data=product, headers=headers)
    return response.status_code


def get_product(product_id: int):
    """
    Get a product from the shopify store.
        Param : product_id : int : The id of the product to get.
        Return : json : The product that was found.
    """
    product_url = store_url + "/products/" + str(product_id) + ".json"
    response = requests.get(product_url, headers=headers)
    return response.json()


def remove_default_title():
    global new_product
    products = get_all_products()
    print(products)
    for product in products:
        try:
            new_product = {
                "product": {
                },
            }
            product["options"][0]["values"] = [product["options"][0]["values"][1]]
            product["options"][0]["name"] = product["options"][0]["values"][0]

            product["variants"][0] = product["variants"][1]
            product["variants"].pop(1)

            new_product["product"]["variants"] = product["variants"]
            new_product["product"]["options"] = product["options"]
        finally:
            if update_product(product["id"], new_product):
                print("Product updated")
            else:
                print("Product not updated")


def update_variant_option(product_id):
    product_url = store_url + "/products/" + str(product_id) + ".json"
    response = requests.get(product_url, headers=headers)
    print(response.json())


def get_inventory_item_id(product_id):
    product_url = store_url + "/products/" + str(product_id) + ".json"
    response = requests.get(product_url, headers=headers)
    return int(response.json()["product"]["variants"][0]["inventory_item_id"])


def main():
    product = {
        "product": {
            "isbn": 9789163892196,
            "title": "Dino 1-2-3",
            "body_html": "This is a test",
            "vendor": "Habib",
            "product_type": "Inbunden",
            "handle": "dino-123",
            "status": "active",
            "published_at": "2020-01-01T00:00:00.000Z",
            "tags": "Saga för barn",
            "Collection": "Saga för barn",
            "options": [
                {
                    "name": "Bokformat",
                    "values": [
                        "Inbunden",
                    ]
                }
            ],
            "variants": [
                {
                    "title": "Inbunden",
                    "price": "100",
                    "sku": 9789163892196,
                    "option1": "Inbunden",
                    "barcode": 9789163892196,
                    "weight": 0.220,
                }
            ]
        }
    }
    product_id = 7770373193902
    image = {
        "image": {
            "product_id": product_id,
            "alt": "Dino 1 2 3 av Habib",
            "src": "https://bilder.forlagssystem.se/9789163892196.jpg",
            "width": 300,
            "height": 400,
        }
    }

    inventory_item = {
        "location_id": location_id,
        "inventory_item_id": get_inventory_item_id(product_id),
        "available_adjustment": 10
    }
    print(create_new_inventory_item(inventory_item))


if __name__ == "__main__":
    main()
