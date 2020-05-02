class BoughtProduct():
    product = None
    quantity = 0
    

    def __init__(self, product, quantity): 
        self.product = product
        self.quantity = quantity

    def to_dict(self)           : 
        return {
            'product'             : self.product.to_dict(),
            'quantity'            : self.quantity
        }