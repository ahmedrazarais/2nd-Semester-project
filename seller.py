from login import *

# Making new class seller that inherits from login class in which we add products in thier table
# Modify the Seller class constructor to accept the user_id parameter
class Seller(Login):

    """This class continues multilevel inheritance It allows and handle multiple sellers 
       Differeny sellers have access to thier dashboard add products in ary store
       update delete view and many more options to explore
       Instanec Attribute : user id , cataegory  """
    
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.cataegory=self.get_cataegory()  # get cataegory name of seller
    

    # Method to extract data from cataegory table
    def extract_data_from_cataegory_table(self):
        """This method is to extract data from cataegory table.we use sql queries to get data
        and we get data in 2d form a list and tuple."""

        #use try except to avoid conflicts
        try:


            # query to use store database
            self.cursor.execute("USE store")


            # wriittng query to fetch data from accounts info table
            get_data_query=f"SELECT * FROM {self.cataegory}"

            # execute that query
            self.cursor.execute(get_data_query)

            # quert to get data in 2d format
            data=self.cursor.fetchall()

            # commit that change
            self.conn.commit()
            
            # getting packed data u=in 2-d format
            return data

        except mysql.connector.Error as e:
            print_error(f"Getting error in extracting data {e}.")
            exit()



    # Methhod to use method extract data from accounts table to get cataegory name
    def get_cataegory(self):
        """This method is to get cataegory name of seller from accounts table
           we use extract data method to get cataegory name of seller."""
        

        # calling parent class method to extract data from accounts table
        data=super().extract_data_from_accounts_table()
      

        # checking in database that user_id matches with user_id so we get cataegory name
        for items in data:
            if self.user_id==items[4]:
                return items[8]
        else:
            print_error("Cataegory Not Found.")
            return
        
       
       
        


    #generating random product id check in file if it is unique save it in file if not then return
    def random_product_id(self):
        """This method is to generate random product id for seller we use random module
           to generate random product id and check in file if it is unique save it in file
           if not then return that product id."""
        
        # first make file name ids.txt
        with open("ids.txt","a+") as file:
            file.seek(0)
            ids=file.readlines()
            while True:
                product_id=random.randrange(1000,9999)
                if f"{product_id}\n" not in ids:
                    file.write(f"{product_id}\n")
                    return product_id
                else:
                    continue

    

    # Method to take product name input also check product name must be unique
    def get_product_name(self):
        """This method is to take product name input from seller also check product name must be unique
           we use extract data from cataegory table to check if product name is unique or not."""
        
        while True:
            # calling method to extract data from cataegory table
            data=self.extract_data_from_cataegory_table()

            # Taking product name input
            product_name=input("Enter Product Name (enter 0 to back):").strip().lower()


            # if he want to go back
            if product_name=="0":
                return
            
            # check if product name is empty
            if product_name=="":
                print_error("Product Name is mandatory to be set.")
                continue

            # checking if data or not
            if data:
                for items in data:
                    if product_name==items[1]:
                        print_error("Product Name Already Taken By someone else. Please select another.")
                        break

                else:
                    return product_name
            
            # return product name if no data in table
            else:
                return product_name
            

    # Method to take quantity input only digits allowed must be greater than 0
    def get_quantity(self):
        """This method is to take quantity input from seller only digits allowed
           must be greater than 0."""
        
        while True:
            # Taking quantity input
            quantity=input("Enter Quantity (enter 0 to back):").strip()

            # if he want to go back
            if quantity=="0":
                return
            
            # checking for empty input
            if quantity=="":
                print_error("Quantity is mandatory to be set.")
                continue


             # checking for only digits
            if not quantity.isdigit():
                print_error("Quantity Must contain only digits.")
                continue
            
            # checking for greater than 0
            if int(quantity)<=0:
                print_error("Quantity Must be greater than 0.")
                continue


       

            
            
            # typecast into integer
            return int(quantity)

    
    # Method to take price input only digits allowed must be greater than 0
    def get_price(self):
        """This method is to take price input from seller only digits allowed
           must be greater than 0."""
        
        while True:
            # Taking price input
            price=input("Enter Price (enter 0 to back):").strip()

            # if he want to go back
            if price=="0":
                return
            
            # checking for empty input
            if price=="":
                print_error("Price is mandatory to be set.")
                continue

            # checking for only digits
            if not price.isdigit():
                print_error("Price Must contain only digits.")
                continue

            # checking for greater than 0
            if int(price)<=0:
                print_error("Price Must be greater than 0.")
                continue
            
            # typecast into integer
            return int(price)
        

    # Method to insert data in cataegory table
    def insert_data_in_cataegory_table(self,product_id,product_name,quantity,price):
        """This method is to insert data in cataegory table after getting all inputs by seller
           It takes argument and when we call this function we passed all required parameters"""
        
        # use try except to avoid conflicts
        try:
            # query to use store database
            self.cursor.execute("USE store")

            # query to insert data in cataegory table
            query=f"INSERT INTO {self.cataegory} (product_id,product_name,quantity,price) VALUES (%s,%s,%s,%s)"
            
            # execute that query
            self.cursor.execute(query,(product_id,product_name,quantity,price))

            # commit the change
            self.conn.commit()

        except mysql.connector.Error as e:
            print_error(f"Error in insertion data  {e}.")
            exit()
    

    # Method for procedure to adding product in cataegory table
    def add_product_procedure(self):
        """This method is to control the flow of adding product in cataegory table we use it in client's code
           we call all necessary interior methods here also we generate product id and add product in cataegory table."""
        
        while True:
            # calling parent class method to get cataegory name
            cataegory=self.get_cataegory()
            if cataegory:
                # calling method to generate random product id
                product_id=self.random_product_id()
                product_name=self.get_product_name()
                if product_name:
                    quantity=self.get_quantity()
                    if quantity:
                        price=self.get_price()
                        if price:
                            # call insert data method to write details in table
                            self.insert_data_in_cataegory_table(product_id,product_name,quantity,price)
                            print("\n\033[92mProduct Added Successfully...\033[0m\n")
                            return
                        else:
                            print_error("\nNot Getting Valid Input..Back From The Area.\n")
                            return
                    else:
                        print_error("\nNot Getting Valid Input..Back From The Area.\n")
                        return
                else:
                    print_error("\nNot Getting Valid Input..Back From The Area.\n")
                    return
            else:
                print_error("Categories are not found.")

    
    


    # Method to display all products in cataegory table in formatted way
    def display_products(self):
        """This method is to display all products in cataegory table in formatted way
           we use extract data from cataegory table to get all products and display them."""
        
        # calling parent class method to extract data from cataegory table
        data=self.extract_data_from_cataegory_table()

        # checking if data or not
        if data:
            print(f"\n\t\t\t{self.cataegory} Products\n")
            print("\n{:<12}{:<20}{:<10}{:<8}".format("Product Id", "Product Name", "Quantity", "Price"))
            print("-"*100)
            for items in data:
                print("{:<12}{:<20}{:<10}{:<8}".format(items[0], items[1], items[2], items[3]))
            print("\n")
        else:
            print_error("No Products Found. Add Some Products First.")

    
    # Method to delete product from cataegory table
    def delete_product(self):
        """This method is to delete product from cataegory table we use extract data from cataegory table
           to get all products and delete them."""
        
        while True:
            # calling parent class method to extract data from cataegory table
            data=self.extract_data_from_cataegory_table()

            # checking if data or not
            if not data:
                print_error("No Products Found. Can't Delete Products Rightnow.")
                return
            
            # display all products
            self.display_products()
            
            # Taking product id input
            product_id=input("Enter Product Id to delete (enter 0 to back):").strip()

            # if he want to go back
            if product_id=="0":
                return
            
            # check if product id is empty
            if product_id=="":
                print_error("Product Id is mandatory to be set.")
                continue

            # checking if data or not
            if data:
                for items in data:
                    if product_id==str(items[0]):
                        # query to delete product from cataegory table
                        query=f"DELETE FROM {self.cataegory} WHERE product_id=%s"
                        self.cursor.execute(query,(product_id,))
                        self.conn.commit()
                        print("\n\033[92mProduct Deleted Successfully...\033[0m\n")
                        return
                else:
                    print_error("Product Id Not Found.")
                    continue
            else:
                print_error("No Products Found.")
                return
    

    # Method to update product quantity in cataegory table
    def update_product_quantity(self):
        """This method is to update product quantity in cataegory table we use extract data from cataegory table
           to get all products and update them."""
        
        while True:
            # calling parent class method to extract data from cataegory table
            data=self.extract_data_from_cataegory_table()

            if not data:
                print_error("No Products Found. Can't Update Products Details Rightnow.")
                return
            
            self.display_products()

            # Taking product id input
            product_id=input("Enter Product Id to update quantity (enter 0 to back):").strip()

            # if he want to go back
            if product_id=="0":
                return
            
            # check if product id is empty
            if product_id=="":
                print_error("Product Id is mandatory to be set.")
                continue

            # checking if data or not
            if data:
                for items in data:
                    if product_id==str(items[0]):
                        # Taking quantity input
                        quantity=self.get_quantity()
                        if quantity:
                            # query to update product quantity in cataegory table
                            query=f"UPDATE {self.cataegory} SET quantity=%s WHERE product_id=%s"
                            self.cursor.execute(query,(quantity,product_id))
                            self.conn.commit()
                            print("\n\033[92mProduct Quantity Updated Successfully...\033[0m\n")
                            return
                        else:
                            print_error("Not Getting Valid Input..Back From The Area.")
                            continue
                else:
                    print_error("Product Id Not Found.")
                    continue
            else:
                print_error("No Products Found.")
                return

    
    # Method to update product price in cataegory table
    def update_product_price(self):
        """This method is to update product price in cataegory table we use extract data from cataegory table
           to get all products and update them."""
        
        while True:
            # calling parent class method to extract data from cataegory table
            data=self.extract_data_from_cataegory_table()

            if not data:
                print_error("No Products Found. Can't Update Products Details Rightnow.")
                return
            
            self.display_products()

            # Taking product id input
            product_id=input("Enter Product Id to update price (enter 0 to back):").strip()

            # if he want to go back
            if product_id=="0":
                return
            
            # check if product id is empty
            if product_id=="":
                print_error("Product Id is mandatory to be set.")
                continue

            # checking if data or not
            if data:
                for items in data:
                    if product_id==str(items[0]):
                        # Taking price input
                        price=self.get_price()
                        if price:
                            # query to update product price in cataegory table
                            query=f"UPDATE {self.cataegory} SET price=%s WHERE product_id=%s"
                            self.cursor.execute(query,(price,product_id))
                            self.conn.commit()
                            print("\n\033[92mProduct Price Updated Successfully...\033[0m\n")
                            return
                        else:
                            print_error("Not Getting Valid Input..Back From The Area.")
                            continue
                else:
                    print_error("Product Id Not Found.")
                    continue
            else:
                print_error("No Products Found.")
                return

    

    # Method to search product in cataegory table
    def search_product(self):
        """This method is to search product in cataegory table we use extract data from cataegory table
           to get all products and search them."""
        
        while True:
            # calling parent class method to extract data from cataegory table
            data=self.extract_data_from_cataegory_table()


            if not data:
                print_error("No Products Found. Can't Search Products Details Rightnow.")
                return
            
            self.display_products()

            # Taking product name input
            product_id=input("Enter Product Id to search (enter 0 to back):").strip()

            # if he want to go back
            if product_id=="0":
                return
            
            # check if product name is empty
            if product_id=="":
                print_error("Product Id is mandatory to be set.")
                continue

            # checking if data or not
            if data:
                for items in data:
                    if product_id==str(items[0]):
                        print("\n{:<12}{:<20}{:<10}{:<8}".format("Product Id", "Product Name", "Quantity", "Price"))
                        print("{:<12}{:<20}{:<10}{:<8}".format(items[0], items[1], items[2], items[3]))
                        return
                else:
                    print_error("Product Id Not Found.")
                    continue
            else:
                print_error("No Products Found.")
                return

    

    # Main page for seller

    def seller_main_page(self):
        """This method is to control the flow of seller we use it in client's code
           we call all necessary interior methods here also we check if user is seller or customer."""
        
        while True:
               
            print(f"\t1.Add Product in {self.cataegory} Cataegory.")
            print(f"\t2.View products in your {self.cataegory} cataegory.")
            print(f"\t3.Delete Product From Your {self.cataegory} Cataegory.")
            print(f"\t4.Update Product Quantity From Your {self.cataegory} Cataegory.")
            print(f"\t5.Update Product Price From Your {self.cataegory} Cataegory.")
            print(f"\t6.Search Product in your {self.cataegory} cataegory.")
            print("\t7.Back From Seller Dashboard.\n")

            # Taking choice by user
            choice=input("Enter Your Choice In Seller Area:").strip()
            
            # handle the choices

            # Add product
            if choice=="1":
                # calling respective methods
                self.add_product_procedure()
           
            # Display products
            elif choice=="2":
                # calling respective methods
                self.display_products()
    
            # Delete product
            elif choice=="3":
                # calling respective methods
                self.delete_product()
            
            # Update product quantity
            elif choice=="4":
                # calling respective methods
                self.update_product_quantity()
            
            # Update product price
            elif choice=="5":
                # calling respective methods
                self.update_product_price()
            
            # Search product
            elif choice=="6":
                # calling respective methods
                self.search_product()
            
            # If he want to come back from seller
            elif choice=="7":
                print("\nBack From Seller..\n")
                return
            
            # For invalid choice.
            else:
                print_error("Invalid Choice. Please Enter Correct Choice.")