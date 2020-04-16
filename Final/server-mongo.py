import pymongo
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import bcrypt
import re
import sys
import json
'''Create a MongoClient to the running mongod instance and get the wanted collection'''
try:     
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/?replicaSet=kvstore&readPreference=primaryPreferred')  # Making a connection with MongoClient
    database = client["kvstore"]  # Getting (or Creating) a database
    userpass = database["userpass"]  # Create/Get a collection
except pymongo.errors.PyMongoError:
    print("Can't connect to the server. Something is wrong.")

# Password hash function
def hashPass(password):
    
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(str.encode(password), salt)
    return hash

#Sanitize $ character
def sanitize(input):
    input = re.sub(r'\$', '&#36;', input)
    return input

# verify entered password
# Do not register this function in the XMLRPC!

def verifyPassword(username, password):
    # sanitize username input (only needs to remove $ to prevent possible future NoSQL injection):
    # This is for my peace of mind later on if more functionalities are added. Currently i see no possible attack vectors
    sanitize(username)
    
    # If this information is returned to the user, nosql injection should be considered
    user_doc = userpass.find_one({"username": username})
    if (user_doc == None):
        return False
    else:
        hash = user_doc["password"]
        password = str.encode(password)
        if ((bcrypt.checkpw(password, hash)) == False):
            return False
        else:
            return user_doc

def getNote(username, password):
    print ("Getting user's notes: %s" % username)
    user_doc = verifyPassword(username, password)
    if (user_doc == False):
        return "Username or password is incorrect"
    else:
        if (user_doc["note"]):
            data = json.dumps(user_doc["note"])
            return('Your note is: \n%s' % (data))
        else:
            return("Your note is empty")


def setNote(username, password, newnote):

    user_doc = verifyPassword(username, password)
    if (user_doc == False):
        return "Username or password is incorrect."
    elif (len(newnote) <= 1 or len(newnote) > 500):
        return "Note length must be between 1 and 500."
    else:
        # Filter $ to prevent nosql injection
        newnote = json.loads(sanitize(newnote))
        key = list(newnote)[0]
        value = newnote[key]
        update_key = "note." + str(key)
        userpass.update_one({"username": username},{"$set":{update_key: value}})
        return "You have added new content to the note."


def register(username, password):
    print ("Registering new user: %s" % username)
    if (len(username) <= 0 or len(username) > 50):
        return "The minimum length for username is 1 and the maximum length is 0"
    if not re.match('^[a-zA-Z0-9_]+$', username):
        return "Only letters, digits, and underscores (_) are allowed in the username"
    user_doc = userpass.find_one({"username": username})
    if (user_doc != None):
        return ("The username already exists")
    else:
        userpass.insert_one({"username": username, "password": hashPass(password),"note": {}})
        return("Registered successfully")
    return("Function run")

def changePassword(username, oldPass, newPass):
    print ("Changing user's password : %s" % username)
    user_doc = verifyPassword(username, oldPass)
    if (user_doc == None):
        return "Username or password is incorrect"
    else:
        user_doc["password"] = hashPass(newPass)
        return "Your password has been updated"

with SimpleXMLRPCServer(("192.168.1.10", 12345), logRequests=False, allow_none=True) as server:
    #upload files 
    print("Listening on port 12345")
    server.register_function(register,"register")
    server.register_function(getNote, "getNote")
    server.register_function(setNote, "setNote")
    server.register_function(changePassword,"changePass")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)