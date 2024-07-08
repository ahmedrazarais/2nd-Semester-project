import mysql.connector   # Importing mysql.connector

# importing database password host from sqlconnection file
from sqlconnection import database_host,database_user,database_password

def print_error(message):
    """This is function which will print error message in red"""
    
    # changing error message to red
    print("\n\033[91mERROR:" + message + "\033[0m\n")


class Connection:
    """This class is designed to connect with mysql in this class in initiator we match the variables of database details to make
        secure connection also in the class method to close the connection."""

    def __init__(self):
        try:    # use try except to avoid program from crush
            self.conn=mysql.connector.connect(
                host=database_host,   
                password=database_password,
                user=database_user,        
        )   
            # making pointer for use later 
            self.cursor=self.conn.cursor()
            return 


        # if getting error in connection
        except mysql.connector.Error as e:

            print_error(f"In Connection {e}.")
            print_error("Please check your database details in sqlconnection.py file and try again.")
            self.close_connection()  # close the connection when getting error in setup
            exit()   # use exit to close program immediately if connection not successfull.




    # method for closing connection
    def close_connection(self):
           
           """This method is make to close the connection to database 
              for security purpose"""

           try:    # use try excpet to avoid conficts

            # checking if cursor assigned then close it
            if self.cursor:
                self.cursor.close()
        

            # if connection there then close it
            if self.conn.is_connected():
                self.conn.close()
                

           # if getting error in closing connection
           except mysql.connector.Error as e:
              print_error(f"In closing connection {e}.")

connection=Connection()
