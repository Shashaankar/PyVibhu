#!/usr/bin/python
# encoding: utf-8
# @File: file_name.py
# @Description: 
# @Author: Shashaankar Komirelly, shashaankar61@gmail.com
# Copyright (c) 2015. All rights reserved. 


import os
from os.path import expanduser
from pyftpdlib.authorizers import DummyAuthorizer
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5  # Python < 2.5

# Global cfg 
g_pvb_server_home = expanduser("~")
# Gloabl cfg end

class DummyMD5Authorizer(DummyAuthorizer):

    def validate_authentication(self, username, password, handler):
        hash = md5(password).hexdigest()
        return self.user_table[username]['pwd'] == hash



def _createUserAccount():

    # TODO: Create a server socket and accept connections from client,
    # client sends user name, pwd and configuration details for creating
    # user repositories.

    try:
        # Create direoctry
        user_path=os.path.join(os.path.expanduser("~/vibhu_repos/"), "user1")
        os.mkdir(os.path.expanduser(user_path))
    except:
        print "Error: user repo creation"

        user_pwd_hash = md5('user1').hexdigest()
        authorizer = DummyMD5Authorizer()
        # TODO: 
        authorizer.add_user('user1', hash, os.getcwd(), perm='elradfmw')
        authorizer.add_anonymous(os.getcwd())


