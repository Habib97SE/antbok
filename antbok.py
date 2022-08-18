import shopify

API_KEY = "454fbbfe5a878f728dbe109f1282fbc2"
STORE_NAME = "antbok"
TOKEN_ACCESS = "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"
store_url = "https://%s:%s@%s.myshopify.com/admin" % (
    API_KEY, TOKEN_ACCESS, STORE_NAME)

shopify.ShopifyResource.set_site(store_url)
shop = shopify.Shop.current


def get_product(product_id):
    return shopify.Product.find(product_id)


def get_all_products():
    return shopify.Product.find()


def add_product(new_product: dict):
    """
    Add a new product to the shopify store.
        Param : new_product : dict : The product to add which should include:
            title : str : The title of the product
            body_html : str : The body of the product\
            price : str : The price of the product
            vendor : str : The vendor of the product
            product_type : str : The type of the product
            image : str : url to the image of the product
            tags : str : The tags of the product
            product_type : str : The type of the product
            status : str : The status of the product
            handle : str : The handle of the product.

        Return :
            shopify.Product : The product that was added.
    """
    product = shopify.Product()
    product.title = new_product["title"]
    product.body_html = new_product["body_html"]
    product.vendor = new_product["vendor"]
    product.product_type = new_product["product_type"]
    product.tags = new_product["tags"]
    product.barcode = new_product["sku"]
    product.status = new_product["status"]
    product.handle = new_product["handle"]
    product_saved = product.save()
    if product_saved:
        return product_saved
    return False


def get_barcode(product_id):
    product = get_product(product_id)
    variants = product.variants
    for variant in variants:
        return variant.barcode


def create_new_variant(product_id, new_variant):
    """
    Create a new variant for a product with given product_id.
        Param :
                product_id : int : The id of the product to add the variant to.
                new_variant : dict : The variant to add which should include:
        Return :
                bool : True if the variant was created, False if not.
    """
    variant = shopify.Variant()
    variant.product_id = product_id
    variant.price = new_variant["price"]
    variant.sku = new_variant["isbn"]
    variant.barcode = new_variant["isbn"]
    variant.weight = new_variant["weight"]
    variant.inventory_quantity = new_variant["inventory_quantity"]
    variant.inventory_policy = new_variant["inventory_policy"]
    return variant.save()


def main():
    # add_product(product)
    products = get_all_products()
    for product in products:
        product_id = product.id
        barcode = get_barcode(product_id)

        if (barcode == "3240923"):
            new_variant= {}
            new_variant["product_id"] = product_id
            new_variant["price"] = "100"
            new_variant["isbn"] = "3240923"
            new_variant["weight"] = "0.1"
            new_variant["inventory_quantity"] = "100"
            new_variant["inventory_policy"] = "deny"
            result = create_new_variant(product_id, new_variant)
            if (result):
                print(get_product(product_id))
            else:
                print("Failed to create variant")




if __name__ == "__main__":
    main()
