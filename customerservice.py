# imprting for abstract class
from abc import ABC, abstractmethod

# Making class  name customer services that is basically absract class, the methds in this class are abstract methods whose implementation is in customer class                 
class CustomerServices(ABC):
    """This  is abstract class having abstract methods and implemented in customer class"""


    # Method name adding products procedure is abstract method
    @abstractmethod
    def adding_products_procedure(self):
        pass


    # Method name display_cart is abstract method
    @abstractmethod
    def display_cart(self):
        pass


    # Method name delete_product_from_cart is abstract method                                                       
    @abstractmethod
    def delete_product_from_cart(self):
        pass

    # Method name checkout is abstract method
    @abstractmethod
    def checkout(self):                                                             
        pass


    # Method name view_history is abstract method
    @abstractmethod
    def view_history(self):
        pass

    # Method name feedback is an abstract method
    @abstractmethod
    def feedback(self):
        pass
