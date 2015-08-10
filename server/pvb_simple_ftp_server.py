#!/usr/bin/python
# encoding: utf-8
# @File: file_name.py
# @Description: Simple ftp server opened on local host and accept
# connections for test_user
# @Author: Shashaankar Komirelly, shashaankar61@gmail.com 
# Copyright (c) 2015. All rights reserved.


## sys imports
import os
from optparse import OptionParser
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5  # Python < 2.5

## local imports
import pvb_utils

# Global configuration
g_pvb_server_ip = '127.0.0.1'
g_pvb_max_connections = 512
g_pvb_max_cli_per_ip = 10
g_pvb_ftp_port = 6161
g_pvb_banner = "PyVibhu ftpd server ready..."
g_pvb_test_user = 'test_user'
g_pvb_test_user_pwd = 'test_user'
g_pvb_uinfo_uri = os.environ["PYVIBHU_UINFO"]
g_authorizer = 0# global authorizer for ftp users
options = 0 # global optins object
# Global cfg end 


class DummyMD5Authorizer(DummyAuthorizer):

    # Overwrite authentication routine to use hashed values
    def validate_authentication(self, username, password, handler):
        hash = md5(password).hexdigest()
        return self.user_table[username]['pwd'] == hash


# @Description: Initlaizes user account cfg read from a static file.
# Creates an md5authorizer object which contains all user account info
# to authoorize the users
def _userInit():

    global options

    # create dummy users for now
    # TODO: accept connections and store user, pwd in database, invoke
    # as a separate thread
    try:

        user_info = {'sha':'827ccb0eea8a706c4c34a16891f84e7b'}
        ret = pvb_utils.pvb_writeObject(user_info, g_pvb_uinfo_uri, "a")
        if ret != 0:
            logging.error("python object write failed")
            exit()
        if options.verbose:
            print "dummy user:", user_info

        logging.info("sha user created from db")

    except Exception, e:
        logging.exception(e)

    # TODO: Read user info from DB and build the authorizer. For now we
    # consider a python dictionary based user and pwd hash file, stored while
    # user account creation phase. Read from userinfo.db to create
    # md5authorizer
    global g_authorizer
    try:
        # Create an authorizer object
        g_authorizer = DummyMD5Authorizer()

        # Read user DB and add to authorizer
        user_data = pvb_utils.pvb_readObject(g_pvb_uinfo_uri, "r")
        if user_data == None:
            logging.error("userInit: Error in reading user data")
            exit()

        if options.verbose:
            print user_data

        # user data should be a dictionary with user name and hash pwd's
        for user, pwd in user_data.items():
            user_directory = os.getcwd()
            g_authorizer.add_user(user, pwd, user_directory, perm='elradfmw')

        g_authorizer.add_anonymous(os.getcwd())

    except Exception, e:
        logging.error("userInit: Error in opening userinfo file")
        logging.exception(e)


def main():

    # Command line arguments parsing. TODO: _procArgs()
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

    global options
    (options, args) = parser.parse_args()
    # Restrict fo other valid modes 
    """
    if options.mode != 'novice':
        if len(args) != 1:
            parser.error("incorrect number of arguments")

        if options.verbose:
            print "reading %s..." % options.filename
    """

    # logging enable
    logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(levelname)s %(message)s',\
                filename='./dbg.log', filemode='w') 



    # Vibhu system init
    _userInit()
    global g_authorizer
    
    if options.mode != 'intermediate':
        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()
    else:
        # use global authorizer created from registered users
        authorizer = g_authorizer


    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(g_pvb_test_user, g_pvb_test_user_pwd, '.', perm='elradfmwM')
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
