
from customer import *


# making object of class
register=Registration()
login=Login()



# Main method to run the store
def main():
        print("\t\tWelcome To ARY Store.")

        # Display options in loop 
        while True:
            print("\t1.proceed For Registration.")
            print("\t2.proceed For Login.")
            print("\t3.Exit From Store.\n")

            # Taking choice by user
            choice=input("Enter Your Choice In Store:").strip()

            # handle the choices
            if choice=="1":
                # calling registration main method
                register.registration_main_page()
           

            elif choice=="2":
                login.login_main_page()
          

            # if want to exit
            elif choice=="3":
                print("Exiting From ARY Store..See you Soon.\n")
                break

            # If getting invalid input
            else:
                print_error("Invalid Choice. Select From Given Choice")

main()   # callin the main





