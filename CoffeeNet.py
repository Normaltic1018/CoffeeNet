#!/usr/bin/env python3

from coffee_lib.interface import message
from coffee_lib.interface import consultant
from coffee_lib.interface import coffee_util as util
import os
import sys

if __name__ == "__main__":
    #message.title()

    consul = consultant.Consultant("test")

    consul.main_menu()
    sys.exit()
    
