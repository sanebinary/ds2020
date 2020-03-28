from xmlrpc.server import SimpleXMLRPCServer
import sys
import os
import socket

def connect():
    print('Serving RPC-FTP on localhost port 12345:')
    return (
    '''
    ********** RPC SERVICE FOR FTP **********
    =========================================
    Ctrl + C to escape
    ''')


def setFileName(src,dest):
    src = os.path.join(os.getcwd(),src)
    dest = os.path.join(os.getcwd(),dest)
    os.rename(src,dest)
    return('File ' + src + ' has been renamed to ' + dest)

def appendContent(dest, arg):
    with open(dest, 'ab') as f:
        f.write(arg.data)
    return(dest + ' has been appended with contents from local file')

def setCreationTime(filename,createdTime):
    # In Unix systems, file has no creation time attribute (or it exists as some others debate but difficult to manually set it):
    # https://unix.stackexchange.com/questions/118577/changing-a-files-date-created-and-last-modified-attributes-to-another-file 
    # So I will just append the time to the file
    
    with open(filename, 'a') as f:
        f.write("//Creation Date: " + createdTime)
        return(filename + " is created at " + createdTime)

def upload(filename, arg):
    with open(filename,"wb") as f:
        f.write(arg.data)


with SimpleXMLRPCServer(("localhost", 12345), logRequests=False, allow_none=True) as server:
    #upload files
    server.register_function(connect, "connect")
    server.register_function(setFileName, "setFileName")
    server.register_function(appendContent, "appendContent")
    server.register_function(setCreationTime, "setCreationTime")
    server.register_function(upload, "upload")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
