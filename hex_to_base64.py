#!/usr/bin/python
import sys
import base64

hex_str = sys.argv[1]
plain_str = hex_str.decode("hex")
base64_str = base64.b64encode(plain_str)

print base64_str
