from database import *
import msvcrt
import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random
from datetime import datetime



# Making a class For Registration That Inherits FRom Database_Creation Class To Use Its Methods and continue
# Multilevel Inheritance

class Registration(Database_Creation):
    """This class continues multilivel inherits direct inherits from database class and database_creation class
       Instance Attributes: first name, gmail, otp, phone_number. We created  several methods required for registration."""
    
    def __init__(self):
        self.first_name=""   # initial it empty change it when uuser enter his name.
        self.gmail='' # initial it empty change it when user enter his gmail
        self.otp = ""  
        self.phone_number = ""       # Initialize empty, will store the generated OTP
        super().__init__()   # calling parent constructor
    


    def generate_code(self):
        """Generate a 5-digit verification code."""
        return str(random.randint(10000, 99999))

    def send_email(self, sender_email, receiver_email, password, subject, message):
        """Send an email with the specified subject and message."""


        email = MIMEMultipart()
        # sender email from which we send email
        email["From"] = sender_email
        # reciever email to whom we are sending
        email["To"] = receiver_email

        # subject for mail
        email["Subject"] = subject

        # Atttach message with otp
        email.attach(MIMEText(message, "plain"))



        context = ssl.create_default_context()

        try:  # use try except to avoid from crash
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, email.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print("An error occurred:", e)


    def send_otp(self):
        """Generate and send an OTP to the user's gmail."""

        # calling otp method to get otp
        self.otp = self.generate_code()

        # checking if gmail is not empty
        if self.gmail!="":
            # subject for gmail
            subject = "Your Verification Code"
            message = f"Your verification code is: {self.otp}"
            # Replace with actual sender email and password from config
            sender_email = "storeary.com@gmail.com"
            password ="pelt xahr clkk nchy"
            self.send_email(sender_email, self.gmail, password, subject, message)
            print("OTP sent successfully.\n")
            verify=self.verify_otp()
            if verify:
                return True
            
        # if phone number registration
        elif self.phone_number!="":
            # then calling captcha
            robot_check=self.captcha()
            if robot_check:
                return True
        


    def verify_otp(self):
        """Verify the OTP entered by the user within 60 seconds."""

        # calll time module 
        start_time = time.time()
        while True:
            otp = input("Enter your OTP (or 0 to exit): ").strip()
            if otp == "0":
                return False  # User chose to exit
            
            # calculating exit timeout
            elapsed_time = time.time() - start_time

            # if time is up
            if elapsed_time > 60:
                print("Time is up!")
                regenerate = input("Do you want to regenerate OTP? (y/n): ").strip().lower()
                if regenerate == "y":
                    print("\nLoading.....\n")
                    start_time = time.time()
                    send=self.send_otp()
                    if send:
                        return True
                      # Reset the timer after sending a new OTP
                elif regenerate == "n":
                    return False  # User does not want to continue
                else:
                    print("Invalid choice. Exiting.")
                    return False
            if otp == self.otp and elapsed_time<=60:
                print("OTP verified successfully!")
                return True
            else:   # if getting not valid otp
                print("Incorrect OTP. Please try again.")
                continue

    def captcha(self):
        """This method is to generate random captcha we use it when user want to register via mobile number then we generate
            captcha and ask him to enter captcha returns true if captcha enter correct"""
        
        # introdcing alphabets lowercase uppercase numbers and special characters
        alpha_upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alpha_lower="abcdefghijklmnopqrstuvwxyz"
        numbers="0123456789"
        spc="!#$&*"
        
        # using random.choice to generate random characters for captcha

        # foe uppercase alphabets
        alpha1=random.choice(alpha_upper)
        alpha2=random.choice(alpha_upper)
        alpha3=random.choice(alpha_upper)

        # for lowercase characters
        alpha4=random.choice(alpha_lower)
        alpha5=random.choice(alpha_lower)
        alpha6=random.choice(alpha_lower)

        # for special characters 
        sc1=random.choice(spc)
        sc2=random.choice(spc)  

        #  For numbers 
        num1=random.choice(numbers)
        num2=random.choice(numbers)

        # logic for creating captcha
        final1=alpha1+ " "*3 + alpha4 + " "*2 +num1
        final2=" "*2 +alpha3+ " "*3 + sc1 + " "*2 + alpha2
        final3=num2 + " "*3 + alpha5 + " "*2 + sc2 + " "*3 +alpha6
        
        # concatecate to make single string
        final=final1+final2+final3

        # removing spaces from generated captcha to see whether user enter corrected captcha or not
        final=final.replace(" ","")

        # Taking input by user in loop give him edge enter 0 to go back
        while True:
            # Displaying captcha
            print("\tGenerated Captcha:\n")
            print(f"{final1}\n{final2}\n{final3}")

            captcha=input("Enter Captcha (enter 0 to back):").strip()

            # if want to go back
            if captcha=="0":
                return
            
            # checking for correct captcha
            if captcha==final:
                return True
            
            else:
                print_error("Invalid captcha please Enter correct captcha.")

    # Method To take first name input in which if he enetr all alphabets alright if he want to enter name with spaces alright other than it no other things allowed
    def get_first_name(self):
        """This method take first name input from user and check if he enter all alphabets
           alright if he want to enter name with spaces alright other than it no other things allowed
           It return first name if all conditions are true"""
        
        # Take input in loop
        while True:
            name=input(f"Enter Your First Name (enter 0 to back):").strip()

            # check if user want to go back
            if name=="0":
                return

            # check if name is empty
            if name=="":
                print_error("Name can't be empty. Please Enter Your Name.")

           
            # check if name contain only aplhabets and spaces
            elif not name.replace(" ","").isalpha():
                print_error("Name can only contain alphabets and spaces. Please Enter Correct Name.")
       
            # if all conditions are true then return name
            else:
                # assign the instance variable to name
                self.first_name=name
                return self.first_name
            


    


    # Method to take last name input make it optional if user want to enter
    def get_last_name(self):
        """This method take input of user's last name but we make it optional if user want to enter
           otherwise he can skip this step"""
        
        # Take input just for first time
        name=input(f"Enter Your Last Name:").strip()
        
        # if user want to go back
        if name=="0":
            return
        # checking if name is empty so assign it with null
        if name=="":
            return "Null"
        

        return name
    

    # Method to take address input from user everything allowed in address
    def get_address(self):
        """This method take input of user's address and everything allowed in address
           like spaces ,numbers ,alphabets etc.It return address if all conditions are true"""
        
        # Take input in loop
        while True:
            address=input(f"Enter Your Address (enter 0 to back):").strip()

            #if he want to go back
            if address=="0":
                return

            # check if address is empty
            if address=="":
                print_error("Address can't be empty. Please Enter Your Address.")
                continue
            
            # if all conditions are true then return address
            else:
                return address
            


    # Method To Take Gmail Input From User And Check If It Is Valid Gmail
    def get_gmail(self):
        """This method take input of user's gmail and check if it is valid gmail
           or not if not then ask user to enter correct gmail"""
        
        # Take input in loop
        while True:
            gmail=input(f"Enter Your Gmail (enter 0 to back):").strip()

            # check if user want to go back
            if gmail=="0":
                return
            
            # checking for typo mistake
            if gmail.endswith("@GMAIL.COM"):
                print_error("It might be typo Mistake. You have to enter '@gmail.com'.")
                continue

            # checking that @ must not in start.
            if gmail.startswith("@"):
                print_error("Please Enter Correct Gmail. '@gmail.com' must not in start.")
                continue

            #check for having any input before @gmail.com
            if gmail.startswith("@gmail.com") or gmail.startswith("@GMAIL.Com"):
                print_error("Please Enter Correct Gmail. '@gmail.com' must not in start.")
                continue

            # check if gmail is empty
            if gmail=="":
                print_error("Gmail can't be empty. Please Enter Your Gmail.")
                continue
            
            # checking that somethings is before @ and after @
            if not "@" in gmail:
                print_error("Please Enter Valid Gmail. '@' must in gmail.")
                continue

            # check if gmail is valid
            if not gmail.endswith("@gmail.com"):
                print_error("Please Enter Valid Gmail. Gmail must endswith '@gmail.com'.")
                continue

            self.gmail=gmail
            # if all conditions are true then return gmail
            return self.gmail
    




    # Method to take Mobile No input by user
    def get_mobile_no(self):
        """This method is to take input for mobile number check validity if all conditions
           met then it return mobile number"""
        
        # Taking input in loop
        while True:
            phone_number=input("Enter Your Mobile-Number (enter 0 to go back):").strip()

            # if he want to go back
            if phone_number=="0":
                return
            

            # checking for empty input
            if phone_number=="":
                print_error("This Field is mandatory to filled for registartion.")

            # Checking conditions for valid number
            elif phone_number.isdigit():
                if len(phone_number)==11:
                    self.phone_number=phone_number
                    return self.phone_number
                else:
                    print_error("Mobile-Number Must contain 11 digits.")
                        
            else:
                print_error("Mobile-Number Must contain 11 digits.")
    
    

    # Method to take register process
    def register_info(self):
        """This method is to ask user that he want to create account via gmail or mobile
           then according to it we adjust our loop."""
        
        while True:
            print("\t1.Register Via Gmail Address")
            print("\t2.Register Via Mobile Number.")
            print("\t3.Back From Area.\n")

            # Taking choice by user
            get_choice=input("Enter Your Choice:").strip()

            if get_choice=="1":
                # call gmail procedure method
                gmail=self.get_gmail()
                if gmail:
                   return gmail
            
            elif get_choice=="2":
                # call mobile numbere method
                number=self.get_mobile_no()
                return number
            
            elif get_choice=="3":
                print("\nBack From This Area.\n")
                return
            
            # If invalid choice
            else:
                print_error("Invalid Choice.Please Enter Correct choice.")


     # method to ask for user id input that must be unique
    def get_user_id(self):
        """This method we ask for user-id input we check in account_info table that user id
            must be unique for every user.In This Method first we call extract data method to
            check user id in it"""
        
        while True:
            # calling method to get data from table
            data=self.extract_data_from_accounts_table()

            # taking input in loop
            user_id=input("Enter Your User-id (enter 0 to go back):").strip()

            # convert into lower case to check in database
            user_id_lower=user_id.lower()

            first = f"{user_id[0:3]}{str(random.randint(10,90))}{user_id[3:]}"

            second = f"{user_id[0:2]}{user_id[3:5]}{str(random.randint(100,900))}"
            

            # checking if he want to go back
            if user_id=="0":
                return
            

            
            # checking for empty case
            if user_id=="":
                print_error("User-id is mandatory to set.")
                continue

            # checking not even a single spcecial characters allowedd
            if any(not char.isalnum() for char in user_id):
                print_error("User-id Must contain only alphabets and digits.")
                continue


            # check if having data in table mean it not be first user
            if data:
                # now unpacking that list/data  matching 4th index wiith user id
                for items in data:

                    # checking user id matches also he is seller
                    if user_id_lower==items[4] and items[7]=='seller':
                        print_error("This User-Id Already Taken By Seller. Select another or login as a seller.")

                        # checking that generated random id is not equals to user id 
                        if items[4]!=first:
                            print(f"1. {first}")
                        
                        # checking that if generated random id is equals to user id 
                        if items[4]==first:
                            first = f"{user_id[0:3]}{str(random.randint(10,90))}{user_id[3:]}"
                            print(f"1.{first}")

                        # checking that generated random id is not equals to user id 
                        if items[4]!=second:
                            print(f"2. {second}")

                        # checking that if generated random id is equals to user id 
                        if items[4]==second:
                            second=second = f"{user_id[0:2]}{user_id[3:5]}{str(random.randint(100,900))}"
                            print(f"2.{second}")
                        
                        # giving two more options to users
                        print("3. Login to your account.")
                        print("4. Enter your own User-Id.")
                        while True:

                            # taking user choice in loop
                            choice=input('Enter your choice : ')

                            # Handle user choice
                            if choice=='1':
                                user_id=first
                                return user_id
                            elif choice=='2':
                                user_id=second
                                return user_id
                            
                            elif choice=='3':
                                # import Login from login
                                from login import Login
                                Login.login_main_page(self)
                                return
                            
                            elif choice=='4':
                                break

                            else:
                                print_error("Enter from given choices.")
                        break

                    # checking user id matches also he is customer
                    elif user_id_lower==items[4] and items[7]=='customer':
                        print_error('User-Id has been taken by customer. Select another or login as a customer.')


                        # checking that generated random id is not equals to user id 
                        if items[4]!=first:
                            print(f"1. {first}")

                          # checking that if generated random id is equals to user id 
                        if items[4]==first:
                            first = f"{user_id[0:3]}{str(random.randint(10,90))}{user_id[3:]}"
                            print(f"1.{first}")

                          # checking that generated random id is not equals to user id 
                        if items[4]!=second:
                            print(f"2. {second}")

                          # checking that if generated random id is equals to user id 
                        if items[4]==second:
                            second=second = f"{user_id[0:2]}{user_id[3:5]}{str(random.randint(100,900))}"
                            print(f"2.{second}")

                        # giving two more options
                        print("3.Login to your account.")
                        print("4.Enter your own User-Id.")
                        while True:

                            # taking choice
                            choice=input('Enter your choice : ')

                            # Handle user choice
                            if choice=='1':
                                user_id=first
                                return user_id
                            elif choice=='2':
                                user_id=second
                                return user_id
                            elif choice=='3':

                                 # import login from main.py
                                from main import login
                                login.login_main_page()   # calling login method
                                return
                            
                            # when decide to enter own id
                            elif choice=='4':
                                break

                            # if not getting valid choice
                            else:
                                print_error("Enter from given choices.")
                        break
                        
      
                else:
                    return user_id
            # return after valid input          
            else:
                return user_id
            
            
            

    # Method to take password input
    def get_password(self):
        """This method is to take password input check all validity after all
           conditions it return password."""
        
        while True:
            print("Enter your password (enter 0 to back) : ", end="", flush=True)
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
            if password == '0':
                break

            # checking for length condition
            if not (8 <= len(password) <= 20):
                print_error("Password must be between 8 and 20 characters long.")
                continue

            # checking for alphabets
            if not any(char.isalpha() for char in password):
                print_error("Password must contain at least one alphabet.")
                continue

            # checking for digits
            if not any(char.isdigit() for char in password):
                print_error("Password must contain at least one digit.")
                continue

            # Checking for special characters
            if not any(not char.isalnum() for char in password):
                print_error("Password must contain at least one special character.")
                continue

            # when all conditions are met simply return password
            return password

    # Method to ask security question
    def get_security_answer(self):
        """This method is made to ask security answer by user which can be used in login procedure
           in that case if he forgot password."""
        
        while True:
            sec_ans=input("What Is Your Favourite Pet Animal (enter 0 to back):").strip()

            # if he want to go back
            if sec_ans=="0":
                return
            
            # checking if getting empty input
            if sec_ans=="":
                print_error("This is mandatory to answer for security purpose.")
                continue
            

            # return security answer
            return sec_ans
        

    # Method to take cataegory input from seller
    def cataegory_input(self):
        """This method is made especially for sellers that they can make thier accounts
            and enter the cataegory in which they add thier product also we check in database
            that cataegory is not taken by anyone."""
        
        while True:
            # calling method extract data from accounts table
            data=self.extract_data_from_accounts_table()

            # Asking for cataegory name input
            cataegory=input("Enter The Cataegory You Want To Sell Products in (enter 0 to back):").strip().lower()
            

            # if want to go back
            if cataegory=="0":
                return
            
            # if null input
            if cataegory=="":
                print_error("Cataegory is mandatory to be set.")
                continue

            # Checking only alphabets allowed
            if not cataegory.isalpha():
                print_error("Cataegory Must contain only alphabets.")
                continue


            # checking if data or not
            if data:
                for item in data:
                    if cataegory==item[8]:
                        print_error("Cataegory Already Taken By someone else. Please select another.")
                        break

                else:
                    return cataegory
            
            # return cataegory if no data in table
            else:
                return cataegory



    
    # Method to ectract data from accounts_info table
    def extract_data_from_accounts_table(self):
        """This method is made to extract data from accounts table.we use sql queries to get data
        and we get data in 2d form a list and tuple."""

        #use try except to avoid conflicts
        try:
            # query to use store database
            self.cursor.execute("USE store")

            # wriittng query to fetch data from accounts info table
            get_data_query="SELECT * FROM accounts_info"

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


    # Method to insert data in accounts table 
    def insert_data_in_table(self,fst_name,lst_name,address,login_info,user_id,password,security,account_type,cataegory):
        """This method to insert data in accounts table after getting all inputs by user
           It takes argument and when we call this function we passed all required parameters"""

        # use try except to avoid conflicts

        try:
            # query to use store database
            self.cursor.execute("USE store")

            # query to insert data in accounts_info table
            query="""INSERT INTO accounts_info 
                (first_name,last_name,address,login_credential,user_id,password,security_question,account_type,cataegory)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            
            # execute that query
            self.cursor.execute(query,(fst_name,lst_name,address,login_info,user_id,password,security,account_type,cataegory))

            # commit the change
            self.conn.commit()

        except mysql.connector.Error as e:
            print_error(f"Error in insertion data yousuuf {e}.")

    
    # main page for signup
    def registration_main_page(self):
        """This is the main method which hanle the flow of registration we use it in client's code
           we call all necessary interior methods here also we make tables when registration is complete."""
        
        while True:
            print("\t1.Proceed As Seller.")
            print("\t2.Proceed As Customer.")
            print("\t3.Back From Registaration.\n")

            # Taking choice by user
            choice=input("Enter Your Choice In Registration Process:").strip()
            
            # handle the choices
            if choice=="1":
                # assign account type to seller 
                account_type="seller"
          

                # calling respective methods
                fst_name=self.get_first_name()
                if fst_name:
                        lst_name=self.get_last_name()
                        address=self.get_address()
                        if address:
                            register=self.register_info()
                            if register:
                                user_id=self.get_user_id()
                                if user_id:
                                    password=self.get_password()
                                    if password:
                                        security=self.get_security_answer()
                                        if security:
                                            cataegory=self.cataegory_input()
                                            if cataegory:
                                                print('\nLoading.....\n')
                                                send=self.send_otp()
                                                if send:
                                                    # call insert data method to write details in table
                                                    self.insert_data_in_table(fst_name,lst_name,address,register,user_id,password,security,account_type,cataegory)

                                                    # After creation of account call the methods which is in database class to create table of user baesd on thier cataegory
                                                    super().create_table_for_sellers(cataegory)

                                                    print("\n\033[92mAccount Created Successfully..\033[0m\n")
                                                    # import Seller class from seller.py
                                                    from seller import Seller
                                                    seller = Seller(user_id)
                                                    seller.seller_main_page()  # calling seller main page
                                                    return
                                   
           
            # for customer area
            elif choice=="2":
                # assign account type to customer and cataegory to null
                account_type="customer"
                cataegory="Null"

                # calling respective methods
                fst_name=self.get_first_name()
                if fst_name:
                        lst_name=self.get_last_name()
                        address=self.get_address()
                        if address:
                            register=self.register_info()
                            if register:
                                user_id=self.get_user_id()
                                if user_id:
                                    password=self.get_password()
                                    if password:
                                        security=self.get_security_answer()
                                        if security:
                                            print('\nLoading.....\n')
                                            send=self.send_otp()
                                            if send:
                                                # call insert data method to write details in table
                                                self.insert_data_in_table(fst_name,lst_name,address,register,user_id,password,security,account_type,cataegory)

                                                # After creation of account call the methods which is in database class to create table of user baesd on thier names
                                                super().create_table_for_users(user_id)
                                                print("\n\033[92mAccount Created Successfully..\033[0m\n")
                                                # import Customer class from customer.py
                                                from customer import Customer
                                                customer = Customer(user_id)
                                                customer.customer_main_page()  # calling customer main page

                                                
                                                return
                                       

            # If he want to come back from registration
            elif choice=="3":
                print("\nBack From Registration..\n")
                break
            
            # For invalid choice.
            else:
                print_error("Invalid Choice.Please Enter Correct Choice.")