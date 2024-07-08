from seller import *
from customerservice import *

# Making class customer which inherits seller class and customer services class
class Customer(Seller, CustomerServices):
    """This class continues multilevel inheritance also inherits customerservices this class implemented 
       all Abstract methods. 
       Instance attribute : user id , cataegory
       Key Feature: If user exit without checkout his cart detail remains saved and when he came back we give him option 
        to go with his cart or not , user has access to see his history complete access of his cart  he can add product
        update its details and delete anything many more options."""


    def __init__(self, user_id):
        # Initialize attributes specific to the Customer class
        self.user_id = user_id
        self.category = ""  # Initialize category as empty, to be updated later
        super().__init__(user_id)  # Call the __init__ method of the Seller class



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




    # Method to extract all cataegories from accounts table and make them in dictionary as key value pair to show to customer
    def extract_cataegories(self):
        """This method is to extract all cataegories from accounts table and make them in dictionary as key value pair
           to show to customer."""
        
        # calling parent class method to extract data from accounts table
        data=self.extract_data_from_accounts_table()

        # making dictionary to store cataegories
        cataegories={}

        # checking if data or not
        if data:
            for items in data:
                # we only add in dictionary if index 8 is not null
                if items[8] != "Null":
                    # we make key starts from 1 then acc to len of dictionary incremented
                    cataegories[str(len(cataegories)+1)]=items[8]


        return cataegories
    
    # method to display all cataegories in formatted way
    def display_cataegories(self):
        """This method is to display all cataegories in formatted way we use extract cataegories method to get all cataegories."""
        
        # calling method to extract cataegories
        cataegories=self.extract_cataegories()

        # checking if cataegories or not
        if cataegories:
            print("\n\t\tAll Categories\n")
            print("{:^25}{:^35}".format("Category Id", "Category Name"))
            print("-" * 60)
            for key, value in cataegories.items():
                print("{:^25}{:^35}".format(key, value))
            print("\n")
        
        else:
            print_error("No Cataegories Found.")
    

    
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
            return True
        else:
            print_error("Sorry There Are No Products In This Cataegory view another cataegory.")

    


    def adding_products_procedure(self):
        """Control the flow of adding products to the cart.
        This method displays categories, asks the user to select a category,
        then displays the products in that category and allows the user to add products to the cart.
        """
        
        while True:
            # Display all categories
            self.display_cataegories()

            # Ask user to enter category ID
            cataegory_id = input("Enter Category Id to view Products (enter 0 to go back): ").strip()

            # Validate that the category ID is an integer
            if not cataegory_id.isdigit():
                print_error("Category Id must be an integer.")
                continue

            # If the user enters 0, exit the method
            if cataegory_id == "0":
                return

            # Ensure that category ID is not empty
            if cataegory_id == "":
                print_error("Category Id is mandatory.")
                continue

            # Extract categories from the data source
            cataegories = self.extract_cataegories()

            # Check if the entered category ID exists
            if cataegory_id not in cataegories:
                print_error("Category Id not found.")
                continue

            # Set the selected category
            self.cataegory = cataegories[cataegory_id]

            # Display products in the selected category
            if self.display_products():
                while True:
                    # Ask user to enter product ID
                    product_id = input(f"Enter Product Id to add to cart from {self.cataegory} Category (enter 0 to go back): ").strip()

                    # If the user enters 0, break the inner loop and return to category selection
                    if product_id == "0":
                        break

                    # Ensure that product ID is not empty
                    if product_id == "":
                        print_error("Product Id is mandatory.")
                        continue

                    # Extract product data from the selected category
                    data = self.extract_data_from_cataegory_table()

                    if data:
                        product_found = False
                        for items in data:
                            if product_id == str(items[0]):
                                product_found = True


                                 # Check if this product ID is already in the user's cart
                                self.cursor.execute("USE store")
                                query = f"SELECT * FROM {self.user_id} WHERE product_id=%s AND status=%s"
                                self.cursor.execute(query, (product_id,"pending"))
                                product = self.cursor.fetchone()

                                if product:
                                    print_error("Product already in cart. Please update the quantity.")
                                    
                                    # Prompt the user to enter the new quantity
                                    quantity, price, total_price = self.get_quantity(product_id)

                                    if quantity is not None and price is not None and total_price is not None:
                                        # Update the product quantity in the category table
                                        self.cursor.execute("USE store")
                                        query = f"UPDATE {self.cataegory} SET quantity=%s WHERE product_id=%s"
                                        self.cursor.execute(query, (items[2] - quantity, product_id))
                                        self.conn.commit()

                                        # Update the quantity and total price in the user's cart
                                        new_quantity = product[2] + quantity
                                        new_total_price = new_quantity * price
                                        self.cursor.execute("USE store")
                                        query = f"UPDATE {self.user_id} SET quantity=%s, total_price=%s WHERE product_id=%s"
                                        self.cursor.execute(query, (new_quantity, new_total_price, product_id))
                                        self.conn.commit()

                                        print("\n\033[92mProduct quantity updated successfully in the cart...\033[0m\n")
                                        break
                                    else:
                                        continue
                                else:
                                    # Check if the product is out of stock
                                    if items[2] == 0:
                                        print_error("Product is out of stock.")
                                        continue

                                    # Prompt the user to enter the quantity they want to buy
                                    print(f"You want to buy Product {items[1]}. Please enter quantity.\n")
                                    quantity, price, total_price = self.get_quantity(product_id)

                                    if quantity is not None and price is not None and total_price is not None:
                                        # Update the product quantity in the category table
                                        self.cursor.execute("USE store")
                                        query = f"UPDATE {self.cataegory} SET quantity=%s WHERE product_id=%s"
                                        self.cursor.execute(query, (items[2] - quantity, product_id))
                                        self.conn.commit()

                                        # Insert the order details into the user's cart
                                        current_time = datetime.now().strftime("%H:%M:%S")
                                        self.cursor.execute("USE store")
                                        query = f"INSERT INTO {self.user_id} (product_id, product_name, quantity, price_per_quantity, total_price, time, status, cataegory) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                                        self.cursor.execute(query, (product_id, items[1], quantity, price, total_price, current_time, "pending", self.cataegory))
                                        self.conn.commit()

                                        print(f"\n\033[92mProduct added to cart successfully from {self.cataegory} category...\033[0m\n")

                                        # Ask if the user wants to continue shopping in the current category
                                        while True:
                                            print("Do you want to continue shopping in this category?")
                                            print("1. Yes")
                                            print("2. No\n")

                                            choice = input("Enter your choice: ").strip()

                                            if choice == "1":
                                                break  # Continue shopping in the current category

                                            elif choice == "2":
                                                break  # Break the inner loop to return to category selection

                                            else:
                                                print_error("Invalid choice. Please enter a valid choice.")
                                        
                                        if choice == "2":
                                            return
                                        
                        if not product_found:
                            print_error("Product Id not found. Please enter the correct Product Id.")
                    else:
                        print_error("No products found.")
                        break
            else:
                continue  # If no products are found in the category, return to category selection



    # Method to take quantity input by user that how many quantity he wants to buy it takes argument id that we check in self.cataegory table that the qunatity of that product id available or not
    def get_quantity(self,product_id):
        """This method is to take quantity input from customer that how many quantity he wants to buy
           it takes argument id that we check in self.cataegory table that the qunatity of that product id available or not."""
        
        while True:
            # calling parent class method to extract data from cataegory table
            data=self.extract_data_from_cataegory_table()


            # Taking quantity input
            quantity=input("Enter Quantity (enter 0 to back):").strip()

            # if he want to go back
            if quantity=="0":
                return None,None,None
            
            # checking only digits
            if not quantity.isdigit():
                print_error("Quantity Must contain only digits.")
                continue
            
            # check if quantity is empty
            if quantity=="":
                print_error("Quantity is mandatory to be set.")
                continue

            # checking if data or not
            if data:
                for items in data:
                    if product_id==str(items[0]):
                        # checking if quantity is greater than available quantity
                        if int(quantity)>items[2]:
                            print_error("Quantity Must be less than or equal to available quantity.")
                            continue
                        else:
                            # return qunatity also price of that product and total price after multiply with product
                            return int(quantity),items[3],int(quantity)*items[3]
                            
            else:
                print_error("No Products Found.")
                return


    # Method to extract data from user_id table
    def extract_data_from_user_id_table(self):
        """This method is to extract data from user_id table.we use sql queries to get data
        and we get data in 2d form a list and tuple."""
        
        #use try except to avoid conflicts
        try:
            # query to use store database
            self.cursor.execute("USE store")

            # wriittng query to fetch data from accounts info table
            get_data_query=f"SELECT * FROM {self.user_id}"

            # execute that query
            self.cursor.execute(get_data_query)

            # quert to get data in 2d format
            data=self.cursor.fetchall()

            # commit that change
            self.conn.commit()
            
            # getting packed data u=in 2-d format
            return data

        except mysql.connector.Error as e:
            print_error(f"Getting error Yousuf Bhai in extracting data {e}.")
            
    

    # Method to display cart abstract method
    def display_cart(self):
        """This method is to display cart of customer we use extract data from user_id table to get all products and display them.It is abstract method."""
        
        # calling parent class method to extract data from user_id table
        data=self.extract_data_from_user_id_table()

        # checking if data or not
        if data:
           # checking if any item is in cart that is pending then print headers and display all products
            if any(items[6]=="pending" for items in data):
                print(f"\n\t\t\tYour Cart\n")
                print("\n{:<12}{:<20}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format("Product Id", "Product Name", "Quantity", "Price/Unit", "Total Price", "Time", "Status","Cataegory"))
                print("-"*100)

                for items in data:
                    if items[6]=="pending":
                        print("{:<12}{:<20}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(items[0], items[1], items[2], items[3], items[4], items[5], items[6],items[7]))
            
                print("\n")
                return True
        

            else:
               print_error("It seems like your cart is empty.")

    
    # Method to view history abstract method
    def view_history(self):
        """This method is to view history of customer we use extract data from user_id table to get all products and display them.It is abstract method.
            we check if any order status is not pending then we display that order."""
        
        
        # calling to extracct data from user table
        data=self.extract_data_from_user_id_table()
        
        if not data:
            print_error("You have no previous History.")
            return

        # checking if data or not also add condition that status is not pending and display that order 
        if data:
                print(f"\n\t\t\tRecorded History\n")
                print("\n{:<12}{:<20}{:<10}{:<10}{:<10}{:<10}{:<10}{:>10}".format("Product Id", "Product Name", "Quantity", "Price/Unit", "Total Price", "Time", "Status", "Cataegory"))
                print("-"*100)

                for items in data:

                    if items[6]!="pending":

                        print("{:<12}{:<20}{:<10}{:<10}{:<10}{:<10}{:<10}{:>10}".format(items[0], items[1], items[2], items[3], items[4], items[5], items[6],items[7]))
                print("\n")




    def delete_product_from_cart(self):
        """This method is to delete product from the cart of the customer. 
        We use extract data from user_id table to get all products and display them.
        It is an abstract method.
        """
        
        while True:
            # Calling parent class method to extract data from user_id table
            data = self.extract_data_from_user_id_table()

            # Checking if data exists
            if data:
                if self.display_cart():
                    # Taking product id input
                    product_id = input("Enter Product Id to delete from cart (enter 0 to go back):").strip()

                    # If the user wants to go back
                    if product_id == "0":
                        return
                    
                    # Check if product id is empty
                    if product_id == "":
                        print_error("Product Id is mandatory to be set.")
                        continue

                    product_found = False
                    for items in data:
                        if product_id == str(items[0]) and items[6] == "pending":
                            product_found = True
                            print(f"You want to delete Product {items[1]}. Please enter quantity.\n")
                            
                            # Taking quantity input
                            quantity = input("Enter Quantity to delete from cart (enter 0 to go back):").strip()

                            # If the user wants to go back
                            if quantity == "0":
                                return
                                
                            # Check if quantity is empty
                            if quantity == "":
                                print_error("Quantity is mandatory to be set.")
                                continue

                            # Checking only digits
                            if not quantity.isdigit():
                                print_error("Quantity must contain only digits.")
                                continue

                            # Checking if quantity is greater than available quantity
                            if int(quantity) > items[2]:
                                print_error("Quantity must be less than or equal to available quantity.")
                                continue
                            else:
                                # Adjust total price and quantity
                                new_quantity = items[2] - int(quantity)

                                total_price = items[4] - (int(quantity) * items[3])

                                # Now we subtract quantity from user_id table and make that update in table
                                self.cursor.execute("USE store")
                                query = f"UPDATE {self.user_id} SET quantity=%s, total_price=%s WHERE product_id=%s"
                                self.cursor.execute(query, (new_quantity, total_price, product_id))
                                self.conn.commit()

                                # Now we add that quantity back to the category table
                                self.cursor.execute("USE store")
                                table_name = items[7]
                                query = f"UPDATE {table_name} SET quantity=quantity+%s WHERE product_id=%s"
                                self.cursor.execute(query, (int(quantity), product_id))
                                self.conn.commit()

                                print(f"\n\033[92mQuantity Deleted From Cart Successfully...\033[0m\n")
                                if new_quantity==0:
                                    self.cursor.execute("USE store")
                                    self.cursor.execute(f"DELETE FROM {self.user_id} where product_id={product_id}")
                                    self.conn.commit()
                                return
                    
                    if not product_found:
                        print_error("Product Id Not Found. Please Enter Correct Product-Id.")
                        continue
                else:
                    print_error("No Products Found.")
                    return
            else:
                print_error("No Products Found In Cart.")
                return

    # Overload the less than (<) operator.
    def __lt__(self,other):
        return self.rating < other

    # Overload the greater than (>) opertor.
    def __gt__(self,other):
        return self.rating > other
    
    # Overload the equal to (==) operator.
    def __eq__(self,other):
        return self.rating == other
    
    def feedback(self):
        # Initializes rating to a default value of 3.
        self.rating=3
        while True:
            # Displays a star rating system.
            print("★★★★★ - 5 stars\n★★★★☆ - 4 stars\n★★★☆☆ - 3 stars\n★★☆☆☆ - 2 stars\n★☆☆☆☆ - 1 star")
            try :
                # Prompts the user for input.
                user_rating=int(input("How many stars you want to give us ? (enter 0 to go back) : "))

                # If empty, ask again.
                if user_rating == "":
                    print_error("Field can't be empty.")
                    continue

                # If user want to go back.
                if user_rating=="0":
                    return
    
                # If rating entered by user is not in b/w 1 to 5, will ask again.
                if (user_rating) > 5 or (user_rating) < 1:
                    print_error("Rating must be in between 1 to 5.")
                    continue

                # Operator overloading method (gt) to compare self.rating with user_rating and provides appropriate feedback messages
                if (user_rating) < self.rating:
                    print("Thanks for your feedback. Seems like you are disappointed") # kia yaha pr pooche k usse kia acha nhi laga?? @ahmedRaza
                    return True
                
                # Operator overloading methods (eq) to compare self.rating with user_rating and provides appropriate feedback messages
                elif user_rating == self.rating:
                    print("Thanks for your feedback.")
                    return True
                
                # Operator overloading methods (lt) to compare self.rating with user_rating and provides appropriate feedback messages
                elif (user_rating) > self.rating:
                    print("Thanks for your feedback. Seems like You are satisfied.\n")
                    return True
                break

                
            # If input is not digit, will ask again   
            except ValueError:
                print_error("Rating must be in digit.")
                continue
            

    # Method dummy to display 2 options for payment mode
    def payment_mode(self):
        """This method is to display 3 options for payment mode we use it in client's code
           we call all necessary interior methods here also we check if user is seller or customer."""
        
        while True:
            print("\n\t1.Cash On Delivery.")
            print("\t2.Credit Card.")
            print("\t3.Back From Payment Method.\n")

            # Taking choice by user
            choice=input("Enter Your Choice For Payment Mode:").strip()

            # handle the choices

            # Cash on delivery
            if choice=="1":
                print("\nCash On Delivery Selected.\n")
                return "Cash On Delivery"
            
            # Credit card
            elif choice=="2":
                print("\nCredit Card Selected.\n")
                while True:
                    credit_no=input("Enter Your Credit Card Number (enter 0 to back):").strip()

                    # if want to go back
                    if credit_no=="0":
                        return

                    #if length is not 10
                    if  not len(credit_no)==10:
                       print_error("Please Enter Correct Credit card Number.")
                       continue

                    # if it enter empty
                    if credit_no=="":
                        print_error("Required Field Must Not Be Empty.")
                        continue
                    else:
                    #return "credit card"
                        while True:
                            pin=input('Enter 4 digit pin (enter 0 to go back) : ')
                            
                            # if user wants to go back
                            if pin=='0':
                                return
                            
                            # if all conditions met, return True
                            if pin.isdigit() and len(pin)==4:
                                return "credit card"
                            
                            # if length of pin is not equal to standard length
                            if len(pin)!=4:
                                print_error("Pin must be of 4 digits.")
                                continue

                            # if user enter empty
                            if pin=="":
                                print_error("Required field can't be empty")
                                continue
                        
                
            # Back from area
            elif choice=="3":
                print("\nBack From Payment Process.")
                return
            
            # For invalid choice.
            else:
                print_error("Invalid Choice.Please Enter Correct Choice.")
    

    # Method to checkout abstract method
    def checkout(self):
        """This method is to checkout of customer we use extract data from user_id table to get all products and display them.It is abstract method."""
        
        # calling parent class method to extract data from user_id table
        data=self.extract_data_from_user_id_table()

        # checking if data or not
        if data:
          if self.display_cart():
            # calling method to get payment mode
            payment_mode=self.payment_mode()

            # if payment mode is not none then we update status to paid
            if payment_mode:
                # ask him to confirm checkout in loop
                while True:
                    print("Do You Want To Confirm Checkout?")
                    print("1.Yes")
                    print("2.No\n")

                    # Taking choice by user
                    choice=input("Enter Your Choice:").strip()

                    # if he want to confirm checkout
                    if choice=="1":
                        # we update from user table that status is paid
                        self.cursor.execute("USE store")
                        query=f"UPDATE {self.user_id} SET status=%s WHERE status=%s"
                        self.cursor.execute(query,("paid","pending"))
                        self.conn.commit()

                        # Calculate total bill
                        total_bill=0
                        for items in data:
                            if items[6]=="pending": 
                                total_bill+=int(items[4])
                        
                        print(f"Total Bill is {total_bill}.\n")
                        if payment_mode=="credit card":
                            print(f"Your Payment Mode is {payment_mode}.You must pay {total_bill}.")
                            print(f"Amount {total_bill}PKR is credited from your number")
                            print("\n\033[92mCheckout Successfully.Thanks For Shopping...\033[0m\n")
                            return

                        elif payment_mode=="Cash On Delivery":
                            print(f"Your Payment Mode is {payment_mode}.You must pay {total_bill}.")
                            print("You Must pay the amount at the time of delievery.\n")
                            print("\n\033[92mCheckout Successfully.Thanks For Shopping...\033[0m\n")
                            return

                      
                    
                    else:
                        print_error("Checkout Failed.Please Try Again.")
                        return
          else:
              print_error("For checkout your cart must not be empty.")       

    def delete_pending_orders(self):
        """This method deletes rows from the user_id table where status is pending.
        It also updates the quantity in the respective category table.
        """
        
        try:
            # Select pending orders from the user's table
            self.cursor.execute("USE store")
            query = f"SELECT product_id, quantity, cataegory FROM {self.user_id} WHERE status=%s"
            self.cursor.execute(query, ("pending",))
            data = self.cursor.fetchall()

            # Update quantities in the respective category tables
            for product_id, quantity, category in data:
                update_query = f"UPDATE {category} SET quantity = quantity + %s WHERE product_id = %s"
                self.cursor.execute(update_query, (quantity, product_id))
                self.conn.commit()

            # Delete pending orders from the user's table
            delete_query = f"DELETE FROM {self.user_id} WHERE status=%s"
            self.cursor.execute(delete_query, ("pending",))
            self.conn.commit()
            
            print("\n\033[92mPending Orders Deleted Successfully...\033[0m\n")

        except mysql.connector.Error as e:
            print_error(f"Error in deletion of pending orders: {e}.")
            exit()



    
    # Method to check if in user table there is any pending order or not if any pending then display him his cart and say him that you have pending orders and ask him to delete or not
    def check_pending_orders(self):
        """This method is to check if in user table there is any pending order or not we use it in client's code
           we call all necessary interior methods here also we check if user is seller or customer."""
        
        # calling parent class method to extract data from user_id table
        data=self.extract_data_from_user_id_table()

        # checking if data or not
        if data:
            for items in data:
                if items[6]=="pending":
                    print("You Have Pending Orders In Your Cart.\n")
                    self.display_cart()
                    while True:
                        print("Do You Want To Delete Pending Orders?")
                        print("1.Yes")
                        print("2.No\n")

                        # Taking choice by user
                        choice=input("Enter Your Choice:").strip()

                        # if he want to delete pending orders
                        if choice=="1":
                            self.delete_pending_orders()
                            break
                        
                        # if he don't want to delete pending orders
                        elif choice=="2":
                            break
                        
                        # For invalid choice.
                        else:
                            print_error("Invalid Choice. Please Enter Correct Choice.")
                    
                    break
    

    # customer main page
    def customer_main_page(self):
        """This method is to control the flow of customer we use it in client's code
           we call all necessary interior methods here also we check if user is seller or customer."""
 

        self.check_pending_orders()

        while True:
            print("\t1.Add Products In Cart.")
            print("\t2.Display Cart.")
            print("\t3.Delete Product From Cart.")
            print("\t4.Checkout.")
            print("\t5.View History.")
            print("\t6.Feedback.")
            print("\t7.Back From Customer.\n")

            # Taking choice by user
            choice=input("Enter Your Choice In Customer Area:").strip()
            
            # handle the choices

            # Add products in cart
            if choice=="1":
                # calling respective methods
                self.adding_products_procedure()
            
            # Display cart
            elif choice=="2":
                # calling respective methods
                self.display_cart()
            
            # Delete product from cart
            elif choice=="3":
                # calling respective methods
                self.delete_product_from_cart()
            
            # Checkout
            elif choice=="4":
                # calling respective methods
                self.checkout()
            
            # View history
            elif choice=="5":
                # calling respective methods
                self.view_history()
        
            # Feedback
            elif choice == "6":
                self.feedback()

            # If he want to come back from customer
            elif choice=="7":
                print("\nBack From Customer..\n")
                return
            
            # For invalid choice.
            else:
                print_error("Invalid Choice. Please Enter Correct Choice.")