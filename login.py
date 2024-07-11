from registration import *

# Making Class Login That Inherits From registration class

class Login(Registration):
    """This class continue multilevel inheritance Instance Attribute : user id . We created several methods
       that handle different cases for login procedure. 
       Key feature: Captcha and forgot password, ask security question and then change password access."""
    
    def __init__(self):
        self.user_id=""   # initial it as empty later changed it with user_id input
        super().__init__()   # Calling parent constructor
    

    # Method to take user_id input for login 
    # Disclaimer: Method overriding here 
    def get_usér_id(self):
        """This is the method to take user-id input from user to check its credentials for login
           also here method overriding performs as the same name method also exist in parent class
           that is regirstation method name get_user_id."""
        
        while True:
            # calling here parent class method to extract accounts data
            data=super().extract_data_from_accounts_table()

            # Taking user id input
            user_id=input("Enter User-id to login (enter 0 to back):").strip()

            # if he want to go back
            if user_id=="0":
                return
            
            # check in database that user id exist or not
            for items in data:
                if user_id==items[4]:
                    
                    # change self.user_id to user_id
                    self.user_id=user_id
                    # if user id found return 
                    return user_id  
                
            # if not id found
            else:
                if user_id!=items[4]:
                    print_error("User-Id not found. You should Signup first.")
                    while True:
                        ask = input('Want to signup (y/n) ? ').lower()
                        if ask=='y':
                            # Calling registration main page
                            self.registration_main_page()
                          
                            return
                        elif ask=='n':
                            break
                        else:
                            print_error("Enter valid choice.")
                    
      

            

    #Method to take password input
    def get_passwórd(self):
        """This method is to take password input for login.checking in database if password matches or not
            also here method overriding performs that in parent class same method exist"""
        
        # Taking input in loop
        while True:
            # calling parent class method to extract data from accounts table
            data=super().extract_data_from_accounts_table()

            print("Enter your password (enter 0 to back):", end="", flush=True)
            password = ""
            while True:

                # Get a single character input from the user
                char = msvcrt.getch().decode('utf-8')

                # If Enter key is pressed, exit the inner loop
                if char == "\r" or char == "\n":
                    print()
                    break

                # If Backspace key is pressed, remove the last character from password
                if char == "\x08":  
                    if len(password) > 0:
                        password = password[:-1]
                        # Erase the last character from the terminal
                        sys.stdout.write("\b \b")  
                        sys.stdout.flush()
                else:
                    # Append the character to the password and display '*' instead of the actual character
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    # Adjust delay time as needed (e.g., 0.3 seconds)
                    time.sleep(0.1)
                    # This combination moves the cursor back one position (\b) and then replaces the visible character with '*'.
                    sys.stdout.write("\b*")  
                    sys.stdout.flush()
                    password += char
                   
            
            # if user want to go back
            if password=="0":
                return
            
            # checking in row where user_id is self.user_id password matches or not
            for items in data:
                # checking if user id and password matches
                if self.user_id==items[4]:
                    if password==items[5]:
                        print("\n\033[92mPassword Matched...\033[0m\n")
                        return password
                    else:
                        print_error("Password Not Matched. Please Enter Correct Password.")
                        # if password not matched then ask if he forgot password or not
                        # if he say yes to forgot password check if he corrrectly answer secuyrity question then give acces to update password
                        # if he say no then ask for password again
                        while True:
                            print("Do You Forgot Password?")
                            print("1.Yes")
                            print("2.No\n")

                            # Taking choice by user
                            choice=input("Enter Your Choice:").strip()

                            # if he forgot password
                            if choice=="1":
                                sec_ans=self.get_sécurity_answer()
                                if sec_ans:
                                    new_password=self.change_password()
                                    if new_password:
                                        print("\nLogin Successfull..\n")
                                        return
                                    else:
                                        print_error("Not Getting Valid Input. Back From The Area.")
                                else:
                                    print_error("Not Getting Valid Input. Back From The Area.")
                            elif choice=="2":
                                break
                            else:
                                print_error("Invalid Choice.Please Enter Correct Choice.")
                        break

            else:
                print_error("Password Not Matched. Please Enter Correct Password.")
                continue

    # Method to take security answer input and check if it matches with user_id
    def get_sécurity_answer(self):
        """This method is to take security answer input from user and check if it matches with user_id
           if matches then allow user to change password otherwise not."""
        
        while True:
            # calling parent class method to extract data from accounts table
            data=super().extract_data_from_accounts_table()

            # Taking security answer input
            sec_ans=input("What Is Your Favourite Pet Animal (enter 0 to back):").strip()

            # if he want to go back
            if sec_ans=="0":
                return
            
            # checking in database if security answer matches with user_id
            for items in data:
                if self.user_id==items[4]:
                    if sec_ans==items[6]:
                        print("\n\033[92mSecurity Answer Matched...\033[0m\n")
                        return sec_ans
                    else:
                        print_error("Security Answer Not Matched. Please Enter Correct Security Answer.")
                        continue
            


    # Method to change password
    def change_password(self):
        """This method is to change password after getting all inputs from user
           we update the password in accounts table in database."""
        
        while True:
            # calling parent class method to extract data from accounts table
            data=super().extract_data_from_accounts_table()
            
            # Taking new password input from user
            new_password=super().get_password()
            
            # checking in database if user_id matches with user_id
            for items in data:
                if self.user_id==items[4]:
                    # update the password in accounts table
                    query="UPDATE accounts_info SET password=%s WHERE user_id=%s"
                    self.cursor.execute(query,(new_password,self.user_id))
                    self.conn.commit()
                    print("\n\033[92mPassword Updated Successfully...\033[0m\n")
                    return new_password
            else:
                print_error("Password Not Updated. Please Enter Correct Password.")
                continue

    # Method for verification code dummy code is abc
    def verify_captcha(self):
        """This method is to verify the captcha by user."""
        
        captcha = self.captcha()
        if captcha:
            return captcha

    
    # Method to login main page
    def login_main_page(self):
        """This method is to control the flow of login procedure we use it in client's code
           we call all necessary interior methods here also we check if user is seller or customer."""
        
        while True:
            print("\t1.Login As Seller.")
            print("\t2.Login As Customer.")
            print("\t3.Back From Login.\n")

            # Taking choice by user
            choice=input("Enter Your Choice In Login Process:").strip()
            
            # handle the choices

            # Seller one
            if choice=="1":
                # calling respective methods
                user_id=self.get_usér_id()
                # Checking here that account_type is seller or not
                data=super().extract_data_from_accounts_table()

                for items in data:
                    # checking if user_id matches with user_id and account type is seller
                    if user_id==items[4] and items[7]=="seller":
                        # calling password method
                        password=self.get_passwórd()
                        if password:
                            captcha=self.verify_captcha()
                            if captcha:
                                print("\n\033[92mLogin Successful...\033[0m\n")
                                # import Seller class from seller.py
                                from seller import Seller
                                # Pass the user_id to the Seller class
                                seller = Seller(self.user_id)
                                seller.seller_main_page()
                                return
                
                    

            # for customer area
            elif choice=="2":
                

                # calling respective methods
                user_id=self.get_usér_id()

                # Checking here that account_type is customer or not
                data=super().extract_data_from_accounts_table()

                # checking in database if user_id matches with user_id and account type is customer
                for items in data:
                    if user_id==items[4] and items[7]=="customer":
                        # calling password method
                        password=self.get_passwórd()
                        if password:
                            captcha=self.verify_captcha()
                            if captcha:
                                print("\n\033[92mLogin Successful...\033[0m\n")
                                # import Customer class from customer
                                from customer import Customer
                                customer = Customer(user_id)
                                customer.customer_main_page()
                                return
                
    

            # If he want to come back from registration
            elif choice=="3":
                print("\nBack From Login..\n")
                return
            
            # For invalid choice.
            else:
                print_error("Invalid Choice. Please Enter Correct Choice.")