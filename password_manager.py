"""password_manager.py: Stores user password in encrypted format."""

__author__ = "Shantanu Mishra @ "
__email__ = "shantanu.mishra@usask.ca"

from cryptography.fernet import Fernet
import csv
from pathlib import Path
import pandas as pd

print(dir(Fernet))
"""Password Manager

Its a Python program to store and manage the passwords by storing them in and CVS. 
Program ask user to add, view and remove passwords. Passwords are stored in encrypted format in csv. 


library uses
1. cryptography.fernet is used to encrypt and decrypt the password 
2. csv to write and create a csv file 
3. Panadas to perform actions like delete a user name record from csv 
4. Path is used to check if the starter files already exists or not
"""

# Initialize constants
PASSWORD_CSV_PATH = "passwords.csv"
Secret_Key_PATH = "key.key"


def removerow_csv(username):
    """
    Parameters
    -----------------------
    username: str
         the user name of account for which password is stored

    Precond
    -----------------------
    1. User Name should be a non empty string
    2. User name should available in passwords.csv file

    PostCond
    If username is found all the rows with that user name are deleted.
    Also, if user name is not found then programs prompts the failure

    -----------------------
    """
    df = pd.read_csv(PASSWORD_CSV_PATH)
    # check if user name is stored in csv file
    if (df.UserName == username).any():
        df = df[df.UserName != username]
        df.to_csv(PASSWORD_CSV_PATH, index=False)
        print("Removed: ", username)
    else:
        print("User name not found, please try again")


def writerow_csv(line):
    """
     Parameters
     -----------------------
     line: str
           line which is to be written in csv
           line is in a format of [Usernamae,Userpassword]

     Precond
     -----------------------
     1. Line should be non empty
     2. Line should be in format of [Usernamae,Userpassword]

     PostCond
     Line is appened to the passwords.csv file

     -----------------------
     """
    with open(PASSWORD_CSV_PATH, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(line)
        csv_file.close()


def remove_password():
    """
       Usage
       ----------------------
        Selected user name record is deleted if it is availble on the csv,
        else program reports that user not found

        -----------------------
        """

    print("Please select a user from list below to remove from the password manager")

    view_users()
    # prompt user to select a user
    selectedUserName = input("User name to remove: ")

    if (selectedUserName and not selectedUserName.isspace()):
        removerow_csv(selectedUserName)
    else:
        print("Please try again, as user name can not be an empty string")


def add_password():
    """
           Usage
           ----------------------
           User name and user password are added to cvs file
           """
    # prompt user for user name and password
    userName = input("Please enter the user name of the account for which password needs to be stored:")
    userPassword = input("Please enter the password to be stored:")

    if ((userName and not userName.isspace()) and (userPassword and not userPassword.isspace())):
        encryptPass = encrypt_password(userPassword)

        writerow_csv([userName, encryptPass])
    else:
        print("Please try again, as user name or password can not be an empty string")


def view_users():
    """
             Usage
              ----------------------
             Display list of user accounts in the csv file
             """
    # read the password.csv file to check the total row count
    with open(PASSWORD_CSV_PATH, 'r') as csv_file_temp:

        rowCount = len(list(csv_file_temp))
        csv_file_temp.close()

    with open(PASSWORD_CSV_PATH, 'r') as csv_file:

        # skip the first row as its the header
        next(csv_file)
        # check Csv has any user name or not
        if(rowCount > 1):
            for line in csv_file.readlines():
                data = line.rstrip()
                if(len(data.split(",")) == 2):
                    user, password = data.split(",")
                    # decrypt the password back to org string
                    orgPass = decrypt_password(password)
                    print("User:", user, " : ", "Password: ", orgPass)
        else:
            print("Password Manager is empty!")
        csv_file.close()

def load_key():
    """
            Usage
            ----------------------
            Loads the secret key from key.key  to encrypt and decrypt the password

            :return encryption key
             """
    # read the key file
    file = open(Secret_Key_PATH, "rb")
    key = file.read()
    file.close()
    return key


def encrypt_password(password):
    """
             Parameters
             -----------------------
             password: str
                      String password entered by the user

             Precond
             -----------------------
             Password should be non-empty str

             PostCond
             password is encrypted using the secret key
             -----------------------
             """
    # encode the org string password
    passEncoded = password.encode()
    # load the key
    secretKey = Fernet(load_key())
    # encode the org pass then encrypt it
    encryptedPass = secretKey.encrypt(passEncoded)
    # decode the encrypted password into regular string from bytes
    return encryptedPass.decode()


def decrypt_password(encryptedPass):
    """
             Parameters
             -----------------------
             encryptedPass: str
                             encrypted string

             Precond
             -----------------------
             non empty encrypted string which was encrypted using the secret key

             PostCond

              encrypted string  is converted back to  decrypted string
             -----------------------
             """
    # load the key
    secrectKey = Fernet(load_key())

    # encode the encrypted pass then decrypt it
    decryptPass = secrectKey.decrypt(encryptedPass.encode())

    # decode the password into regular string from bytes
    return decryptPass.decode()


def init_starterfiles():
    """
              Usage
              ----------------------
              Checks if the starter files already exists, if not would program initalizes them

              """
    # check if PASSWORD_CSV exists, if not then create a file
    if not Path(PASSWORD_CSV_PATH).is_file():
        # create the csv file
        with open(PASSWORD_CSV_PATH, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            # added username and password as headers
            writer.writerow(["UserName", "UserPassword"])
            csv_file.close()
    # check if Secret_Key exists, if not then create a file
    if not Path(Secret_Key_PATH).is_file():
        # generate a secret key
        key = Fernet.generate_key()
        # create the file
        file = open(Secret_Key_PATH, 'wb')
        # write the key into the file
        file.write(key)
        file.close()


def main():
    """
              Usage
              ----------------------
              Infinite loop is started in which user is asked to enter a selection to
              perform actions like add, remove, view passwords. If user entered quit loop ends with a retru value of 0

              :exit 0
              -----------------------
              """
    init_starterfiles()
    while True:
        print("Choose an action form the list below to continue")

        # ask user input to select the operation
        userSelection = input("1. View a password from password manager - 'view' \n"
                              "2. Add a new password in password manager - 'add'\n"
                              "3. Remove a password from password manager - 'remove'\n"
                              "4. quit\n").lower()

        if userSelection == "quit":
            break
        elif userSelection == "view":
            view_users()
        elif userSelection == "add":
            add_password()
        elif userSelection == "remove":
            remove_password()
        else:
            # user entered invalid input
            print("Invalid input please type a right selection from the menu")
    exit(0)


if __name__ == "__main__":
    main()
