#!/usr/bin/python


import os
from optparse import OptionParser
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging

# Global configuration
g_pvb_server_ip = '127.0.0.1'
g_pvb_max_connections = 512
g_pvb_max_cli_per_ip = 10
g_pvb_ftp_port = 6161
g_pvb_banner = "PyVibhu ftpd server ready..."
g_pvb_test_user = 'test_user'
g_pvb_test_user_pwd = 'test_user'
# Global cfg end 

def main():
    usage = "usage: %prog [options] arg1 agr2"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename", help="read data\
            from FILENAME")
    parser.add_option("-o", "--out", action="store", type="string",\
            dest="output")
    parser.add_option("-v", "--verbose", action="store_true",\
            dest="verbose",default="False")
    parser.add_option("-q", "--quiet", action="store_false",\
            dest="verbose", default="True")
    parser.add_option("-m", "--mode", default="novice",\
            help="interaction mode: novice, intermediate, or expert\
            [default: %default]")

    (options, args) = parser.parse_args()
    # Restrict fo other valid modes 
    if options.mode != 'novice':
        if len(args) != 1:
            parser.error("incorrect number of arguments")

        if options.verbose:
            print "reading %s..." % options.filename

    # logging enable
    logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(levelname)s %(message)s',\
                filename='./dbg.log', filemode='w') 

    # Custom code
    
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(g_pvb_test_user, g_pvb_test_user_pwd, '.', perm='elradfmwM')
    authorizer.add_anonymous(os.getcwd())
    logging.info("PyVibhu: test_user created")

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = g_pvb_banner

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', g_pvb_ftp_port)
    server = FTPServer(address, handler)
    logging.info("PyVibhu: simple ftp server bind success")

    # set a limit for connections
    server.max_cons = g_pvb_max_connections
    server.max_cons_per_ip = g_pvb_max_cli_per_ip

    # start ftp server
    logging.info("PyVibhu: siple fp server start...")
    server.serve_forever()




if __name__ == "__main__":
    main() 
