import xmlrpc.client
import argparse
import sys
import json
###########################################################################################################

parser = argparse.ArgumentParser(description="Python RPC client")
subparsers = parser.add_subparsers(help='subcommands', dest='subparsers')

# create the parser for the "register" command
parser_a = subparsers.add_parser('register', help='register your account')
parser_a.add_argument('-u', metavar='<USERNAME>',type=str, help='Your username', required=True)
parser_a.add_argument('-p', metavar='<PASSWORD>', type=str, help='your password', required= True)

# create the parser for the "setNote" command
parser_b = subparsers.add_parser('setNote', help='add your note')
parser_b.add_argument('-u', metavar='<USERNAME>',type=str, help='Your username', required=True)
parser_b.add_argument('-p', metavar='<PASSWORD>', type=str, help='your password', required= True)
parser_b.add_argument('-t', metavar='<TITLE>',type=str, help='Your note title', required=True)
parser_b.add_argument('-c', metavar="<CONTENT>", type=str, help='Your note content', required=True)

# create the parser for the "getNote" command
parser_c = subparsers.add_parser('getNote', help='get your note')
parser_c.add_argument('-u', metavar='<USERNAME>',type=str, help='Your username', required=True)
parser_c.add_argument('-p', metavar='<PASSWORD>', type=str, help='your password', required= True)

parser_d = subparsers.add_parser('changePass', help='change your password')
parser_d.add_argument('-u', metavar='<USERNAME>',type=str, help='Your username', required=True)
parser_d.add_argument('-o', metavar='<OLD_PASSWORD>', type=str, help='your old password', required= True)
parser_d.add_argument('-n', metavar='<NEW_PASSWORD>', type=str, help='your new password', required = True)



# Print help if no commands are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# parsing arguments
args = parser.parse_args()

with xmlrpc.client.ServerProxy("http://113.190.48.143:12345/") as server:

    if (args.subparsers == 'register'):
        print(server.register(args.u,args.p))
        exit(1)

    #getNote    
    elif (args.subparsers == 'getNote'):
        print(server.getNote(args.u, args.p))
        exit(1)

    #setNote:
    elif (args.subparsers == 'setNote'):
        note = {args.t:args.c}
        print(server.setNote(args.u,args.p, json.dumps(note,separators=(',',':'))))  
        exit(1)
        
    elif (args.subparsers == 'changePass'):
        print(server.changePass(args.u, args.o, args.n))
        exit(1)
