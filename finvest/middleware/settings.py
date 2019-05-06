# -*- coding: utf-8 -*-
import os


################
# Project Configuration
################

# Path to project
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# Path to source data or called input data
SOURCE_DATA = BASE_PATH + '/srcData/'

# Path to destination data or called output data
DST_DATA = BASE_PATH + '/dstData/'

# Path to static files such as stopwords
STATIC_DIR = BASE_PATH + '/static/'