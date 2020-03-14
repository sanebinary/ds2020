from xmlrpc.server import SimpleXMLRPCServer
import sys


def connect():
    print('Serving RPC-FTP on localhost port 12345')
    return (
    '''
    ********** RPC SERVICE FOR FTP **********
    =========================================
    ''')


def setFileName(filename):
    open(filename, "r")
    print("File " + filename + " has been created.")


def appendContent(filename, data):
    with open(filename, 'a') as f:
        f.write(data)
        print("File has been created")

def setCreationTime(filename,createdTime):
    # In Unix systems, file has no creation time attribute (or it exists as some others debate but difficult to manually set it):
    # https://unix.stackexchange.com/questions/118577/changing-a-files-date-created-and-last-modified-attributes-to-another-file 
    # So I will just insert the date on top of the files :)
    with open(filename, 'wb') as f:
        f.write(createdTime)
        print("File is created at " + createdTime)


with SimpleXMLRPCServer(("localhost", 12345), logRequests=False) as server:
    #upload files
    server.register_introspection_functions()
    server.register_function(setFileName, "setFileName")
    server.register_function(appendContent, "appendContent")
    server.register_function(setCreationTime, "setCreationTime")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
