#!/usr/bin/python
# encoding: utf-8
# @File: pvb_utils.py
# @Description: Utilities for PyVibhu
# @Author: Shashaankar Komirelly, shashaankar61@gmail.com
# Copyright (c) 2015. All rights reserved. 

import os
import pickle
import logging



"""
@Brief: write data passed onto file_name.
data can be a any python object, default mode is append.
@return: 0 for success, -1 for failure
"""
def pvb_writeObject(data, file_name, mode):

    try:
        # default mode is append
        if mode == None:
            mode = "a"

        with open(file_name, mode) as f_handle:
            pickle.dump(data, f_handle)
    except Exception, e:
        logging.exeption("pvb_utils: Error in writing Pyobject to file")
        return -1

    # Success case
    return 0


"""
@Brief: read python object from file_name.
default mode is read only.
return: Python object if success, else None
"""
def pvb_readObject(file_name, mode):

    try:
        # default mode is read
        if mode == None:
            mode = "r"

        with open(file_name, mode) as f_handle:
            data = pickle.loads(f_handle.read())

    except:
        logging.exception("pvb_utils: Error in reading Pyobject from file")
        return None


    # return data as python object format
    return data


