#! /usr/bin/python3.9.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/tomsmail/Documents/0SCHOOL/A-Level/Comp Sci/NEA/Code/')
from app import app as application
application.secret_key = 'hushitssecret'