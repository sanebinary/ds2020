#A script to populate mongoDB with a key value database of usernames and passwords#

import pymongo
import string
import random
import bcrypt

"""Generate a random pass of provided length """


def randomPass(samplelist, stringLength=10):
    return ''.join(random.sample(samplelist, stringLength))


"""Generate a random note of fixed length """


def randomNote(samplelist, stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# None of these 3 commands have actually performed any operations
# Collections and databases are created when the first document is inserted into them

# Making a connection with MongoClient
client = pymongo.MongoClient('localhost', 27017)
database = client["kvstore"]  # Getting (or Creating) a database
userpass = database["userpass"]  # Create a collection

# Specify allowed character for passwords
passwords_f = string.digits + string.ascii_letters + string.punctuation
secret_f = string.digits + string.ascii_letters + string.punctuation

# Populate collection with 100 salt hashed random password generated from passwords_f
with open("names.txt", "r") as f:
    for i in range(0, 100):
        passwd = str.encode(randomPass(passwords_f, random.randrange(8, 50)))
        note = randomNote(secret_f, random.randrange(1, 200))
        salt = bcrypt.gensalt()
        passwd_hashed = bcrypt.hashpw(passwd, salt)
        userpass.insert_one(
            {"username": f.readline().rstrip(), "password": passwd_hashed, "note": note})

# create a test account
username = 'test'
passwd = b'test'
note = 'This is a test account'
salt = bcrypt.gensalt()
passwd_hashed = bcrypt.hashpw(passwd, salt)
userpass.insert_one(
    {"username": username, "password": passwd_hashed, "note": note})

