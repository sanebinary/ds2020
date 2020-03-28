from datetime import  datetime
import argparse
import xmlrpc.client
import sys
import os

############################################PARSING ARGUMENTS##############################################
parser = argparse.ArgumentParser(description="Python RPC client")
subparsers = parser.add_subparsers(required=True,help='subcommands', dest='subparsers')

# create the parser for the "setFileName" command
parser_a = subparsers.add_parser('setFileName', help='change filename')
parser_a.add_argument('-i', metavar='<INPUTNAME>',type=str, help='current file name', required=True)
parser_a.add_argument('-o', metavar='<OUTPUTNAME>', type=str, help='new file name', required= True)

# create the parser for the "appendContent" command
parser_b = subparsers.add_parser('appendContent', help='append content to a file on server')
parser_b.add_argument('-src', type=str, required= True, help='a local file to append data to server file')
parser_b.add_argument('-dest', type=str, required= True, help='server file to append to')

# create the parser for the "setCreationTime" command
parser_c = subparsers.add_parser('setCreationTime', help='add creation time to file')
parser_c.add_argument('-file', required = True, type = str, help="filename to set creation time for")
parser_c.add_argument('-manual', type = str, help='add creation time manually')
parser_c.add_argument('-auto', help="let's the server get time", action='store_true')

parser_d = subparsers.add_parser('upload', help='upload file to server')
parser_d.add_argument('-f', required= True, type=str, metavar='filename', help='filename')

parser_e = subparsers.add_parser('download', help='download file from server')
parser_e.add_argument('-f', required= True, type=str, metavar='filename', help='filename')

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
    elif ((args.manual != None) and (args.auto != False)):
        parser.error('setCreationTime only supports either -manual or -auto.')

############################################################################################################

#Read 1mb of data each time
#1 MB = 1024KB and 1 KB = 1024B so 1 MB has 1024 x 1024 = 1,048,576 bytes. That's 1,048,576 characters
def bytes_from_file(filename, chunksize=1048576):
    with open(filename, "r") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                yield from chunk
            else:
                break

with xmlrpc.client.ServerProxy("http://localhost:12345/") as server:
    #setFileName
    if (args.subparsers == 'setFileName'):
        print(server.setFileName(args.i,args.o))
        exit(1)

    #appendContent from local file to server
    elif (args.subparsers == 'appendContent'):
        with open(args.src, "rb") as f:
            data = f.read(1024*1024)
            while data:
                print(server.appendContent(args.dest,data))
                data = f.read(1024*1024)

    #setCreationTime:
    elif (args.subparsers == 'setCreationTime'):
        if (args.manual):
            print(server.setCreationTime(args.file, args.manual))    
        if (args.auto):
            timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            print(server.setCreationTime(args.file, timestampStr))

    #upload:
    elif (args.subparsers == 'upload'):
        filepath = os.path.join(os.getcwd(),args.f)
        if (os.path.exists(filepath)):
            with open(filepath, "rb") as f:
                data = xmlrpc.client.Binary(f.read())
                server.upload(args.f, data)
        else:
            print('The file ' + filepath + ' does not exist')

    #download
    elif (args.subparsers == 'download'):
        with open(args.f, "wb") as f:
            data = server.download(args.f).data
            f.write(data)
