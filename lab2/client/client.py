from datetime import  datetime
import argparse
import xmlrpc.client
import sys
import os

############################################PARSING ARGUMENTS##############################################
parser = argparse.ArgumentParser(description="Python RPC client")
subparsers = parser.add_subparsers(required= True, help='subcommands', dest='subparsers')

# create the parser for the "setFileName" command
parser_a = subparsers.add_parser('setFileName', help='change filename')
parser_a.add_argument('-i', metavar='<INPUTNAME>',type=str, help='current file name', required=True)
parser_a.add_argument('-o', metavar='<OUTPUTNAME>', type=str, help='new file name', required= True)

# create the parser for the "appendContent" command
parser_b = subparsers.add_parser('appendContent', help='append content to a file on server')
parser_b.add_argument('-i', type=str, required= True, help='get a file on server')
parser_b.add_argument('-a', type=str, required= True, help='local file content to append to server file')

# create the parser for the "setCreationTime" command
parser_c = subparsers.add_parser('setCreationTime', help='add creation time to file')
parser_c.add_argument('-manual', type = str, help='add creation time manually')
parser_c.add_argument('-auto', type = str, help="let's the server get time")

# Print help if no commands are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# parsing arguments
args = parser.parse_args()

# If command is setCreationTime without arguments or more than the required argument, show error
if (args.subparsers == 'setCreationTime'):
    if (args.manual is None and args.auto is None):
        parser.error('No argument requested, add -manual or -auto')
    elif ((args.manual != None) and (args.auto != None)):
        parser.error('setCreationTime only supports one argument.')

############################################################################################################
'''
with xmlrpc.client.ServerProxy("http://localhost:12345/") as server:
    #upload files
    if sysarg[1] != 'setFileName':
        setFileName()

    else: 
        server.setFileName(sys.argv[2])
        server.setCreationTime(fileName,datetime.now())
        with open(sys.argv[3], 'rb') as f:
            data = f.read(1048576)
            while (data != ''):
                server.appendContent(fileName, data)
            f.close()
    
    
    #download from server
    exit(1)
'''