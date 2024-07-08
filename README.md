<div align="center">
  <h1>ARY Store</h1>
</div>

### ARY Store is a command-line interface (CLI) based application developed in Python for managing a versatile online store. It utilizes MySQL for data storage, providing robust functionality for both customers and sellers. This README.md aims to provide a detailed overview of the project, covering technical and non-technical aspects.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Project Developers](#project-developers)


# Introduction

### ARY Store is a CLI application designed to simulate an online store environment where customers can browse products, add them to the cart, proceed to checkout, and provide feedback. Sellers can manage their product inventory, view sales history, and update product information. The application ensures secure user authentication and utilizes MySQL databases for efficient data management.

# Features

## Customer Features:

1. **Registration and Login:**

   - Customers can register using their details or quickly sign up via Gmail or mobile phone numbers for seamless access to the store. Secure login ensures privacy and account protection.

2. **Product Browsing and Cart Management:**

   - Customers can explore a wide range of products categorized across various categories within the ARY Store. They can easily navigate through categories, view product details, add products to their cart, and manage cart contents. The cart details are securely saved, allowing customers to resume shopping from where they left off even after exiting the store.

3. **Checkout:**

   - The checkout process is streamlined for customer convenience. Upon confirming their cart items, customers are prompted to choose their preferred payment method. Options include Cash on Delivery for immediate payment upon product delivery or Credit Card, where customers securely enter their credit card details and a PIN for payment.

4. **Order Management:**

   - Customers have access to view their pending orders, facilitating the management of ongoing purchases. They can choose to delete pending orders if needed and also view their order history for past transactions.

5. **Feedback System:**

   - A star rating system allows customers to provide valuable feedback on their shopping experience. This feature helps the ARY Store team continuously improve services based on customer input.

6. **Persistent Cart Storage:**

   - The ARY Store ensures a seamless shopping experience with persistent cart storage. Customers' cart details are saved securely, allowing them to access and manage their cart at any time. Whether they want to add more products, remove items, or proceed to checkout, their cart remains intact across sessions.

7. **Accessibility and Convenience:**

   - Customers can shop conveniently from any device with internet access, making it easy to browse, shop, and manage their shopping experience on the go.

8. **Security and Privacy:**

   - The platform prioritizes security with robust measures to protect customer data and transactions, ensuring a safe and trustworthy shopping environment.

9. **Feedback and Communication:**

   - Customers can easily provide feedback about the store's products, services, and overall experience. This feedback loop helps maintain high standards of customer satisfaction and engagement.




## Seller Features:

1. **Login and Dashboard:**

   - Sellers can register using their details or quickly sign up via Gmail or mobile phone numbers for seamless access to the store. Secure login ensures privacy and account protection.

2. **Product Management:**

   - Allows sellers to add new products, update existing products, manage inventory, and categorize products into different categories.


3. **Inventory Management:**

   - Sellers can update product quantities, prices, and other details directly from the dashboard.

4. **Category Management:**

   - Sellers have the flexibility to add new product categories, manage existing categories, and assign products to specific categories.


5. **Security Features:**

   - Implements secure authentication and authorization mechanisms to protect seller accounts and data.

6. **Accessibility:**

   - Allows sellers to access and manage their store from any device with an internet connection.

7. **Scalability:**

    - Designed to handle a growing number of products, orders, and sellers while maintaining performance.

8. **Customization:**

    - Supports customization options for seller profiles, product displays, and store settings.

9. **Support:**

    - Provides assistance and documentation for sellers on using the platform effectively.


## Common Features:

1. **Security:**
   - Implements secure authentication mechanisms to protect user data and transactions.

2. **Data Storage:**
   - Utilizes MySQL database for storing customer information, product details, and transaction history.

3. **User Interface:**
   - CLI-based interface for intuitive interaction and navigation.

4. **Error Handling:**
   - Includes robust error handling to manage exceptions and provide informative error messages.

5. **Object-Oriented Programming:**
   - Implements object-oriented programming concepts with multi-level inheritance for efficient code organization. Uses Aggregation, Composition, operator overloading, method overriding, abstract classes, and abstract methods for enhanced modularity and flexibility.

## Additional Features:

1. **CAPTCHA and OTP Integration:**
   - Planned feature for enhanced security during registration and login processes.

2. **Mobile Registration and Gmail Integration:**
   - Enables users to register using mobile number and integrates with Gmail for notifications and alerts.

3. **Security In Password And Pin:**
   - Enables that we replace aesteriks with characters when user enter password and
   pin on terminal for betterment of security.

4. **Later Access To Cart:**
   - User has an access to use their cart later even when they exit from application
   when they came back their cart details remain in the cart till tahn they want to erase the details

5. **Displaying Errors:**
  - We are displaying any error in red colour on terminal and in every successfull
  message we use green colour for better interface.

6. **Flexible Flow For Registration:**
   - We make the flow flexible for users that they can move to login if they enter user-id that is already taken by someone else and vice versa.

7. **Suggestions For User-Ids:**
   - When user enter user-id that is already taken by someone we suggest him two user-ids if they want to choose and also give him option to login into his account
   or he can also enter his own user-id.

## Usage
- Before running the project make sure you must setup `sqlconnection.py` file
- Replace database credentials details according to your Database Details
- When setup finished, run the `main.py` file to start the project.

## Technologies Used

- **Programming Language:** Python
- **Database:** MySQL
- **Libraries:** MySQL Connector,random,datetime,smtplib,msvcrt,sys,ssl,email.mime.text,email.mime.multipart 

## Project Developers

- Muhammad Yousuf Mateen
  - Email: muhammadyousufmateen9@gmail.com
- Muhammad Ahmed Raza
  - Email: razarais28@gmail.com

- For any queries or support, please feel free to reach out to us via email.
