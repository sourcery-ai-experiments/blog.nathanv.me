import sys

import c

VAL = 20

print("The real value of c.func is: {}".format(c.func(VAL)))

# ideally, you would have never imported this module
sys.modules.pop("c")
# create reference to real import so we don't lose it
a_real_import = __import__("a")
a_fake_import = __import__("b")

# fake the import
sys.modules["a"] = a_fake_import
import c
# set it back to the real value
sys.modules["a"] = a_real_import

print("The fake value of c.func is: {}".format(c.func(VAL)))