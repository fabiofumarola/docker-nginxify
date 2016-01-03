#!/usr/bin/env python

import crypt
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="nginx auth file generator")
parser.add_argument('--file', dest='dest_folder', default='./nginx/htpasswd/',
    help="the folder to save the new username:password pair")
parser.add_argument('--user', dest='user',
    help="the username for the new user")
parser.add_argument('--pwd', dest='pwd',
    help="the password for the new user")

args = parser.parse_args()

if args.user is None or args.pwd is None:
    print('specify a value for --user an --pwd')
    sys.exit(1)

if len(args.pwd) < 8:
    print('the password should have length greater than 8')
    sys.exit(1)

if not os.path.exists(args.dest_folder):
    os.makedirs(args.dest_folder)



crypted_pwd = crypt.crypt(args.pwd)
dest_file = args.dest_folder + "secure"
with open(dest_file, 'a') as f:
    f.write("%s:%s\n" % (args.user, crypted_pwd))

print('successufly generate password for user ', args.user)
