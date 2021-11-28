# Password-Manager
Program name: Password Manager
Author: Shantanu Mishra

Usage: Its a Python program to store and manage the passwords by storing them in and CVS.
Program ask user to add, view and remove passwords. Passwords are stored in encrypted format in csv.

python library Dependencies: 1. Python 3.8
              2. cryptography.fernet 35.0.0
              3. csv
              3. pathlib
              4. pandas 1.3.3

How to Run:

1. Install all the dependencies
2. Run password_manager.py
   a. On the initialization password.csv and key.key is created if they are not available in the current directory
3. User will be prompt to select one of view, remove, add or quit
   to perform the action

   a. Add
      i. User will be asked to provide a user name
      ii. User will be asked to provide a password
      iii. Password is encrypted and stored in csv
   b. Remove
      i. User is show the available user names
      ii. user can enter one of the user name to remove from csv
      iii. name is remove if its found in csv
   c. View
      Displays list of available user names and their passwords in csv

   d. Quit
      Terminates the program
