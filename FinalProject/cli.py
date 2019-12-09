from inspect   import getfullargspec
from functools import wraps
import sys
import re


class CommandLineInterface:

    functions = {}

    def command(self, f):
        #print(f'f={f.__name__}')
        if f.__name__ not in self.functions:
            #print("add it")
            self.functions[f.__name__] = f
        @wraps(f)
        def wrapper(*args, **kwargs):
            #print(f'f={f.__name__}')
            return f(*args, **kwargs)

        return wrapper

    def main(self):
        command = ""
        key_val = ""

        command = '|'.join(repr(func_name) for func_name, func in self.functions.items())
        USAGE_MESSAGE = f'USAGE: python {sys.argv[0]} {command} {key_val}'
        
        #print(sys.argv)
        if len(sys.argv) <= 2:
            print(USAGE_MESSAGE)
            exit(1)

        func = sys.argv[1]
        if (func not in self.functions):
            print(USAGE_MESSAGE)
            exit(1)
            
        args = sys.argv[2:]
        func_fullargspec = getfullargspec(self.functions[func])
        func_args        = func_fullargspec.args
        exp_arg_count    = len(func_args)

        

        key_val = " ".join(f'{arg}=value' for arg in args)
        command = func
        USAGE_MESSAGE = f'USAGE: python {sys.argv[0]} {command} {key_val}'

        if (exp_arg_count != len(args)):
            print(USAGE_MESSAGE)
            exit(1)

        arg_dict = {}
        for arg in args:
            #print(arg)
            if not re.match("[a-zA-z_]{1}[a-zA-z0-9_]*=[a-zA-z0-9_]+", arg):
                print(USAGE_MESSAGE)
                exit(1)
            parsed_arg = arg.split('=')
            arg_name   = parsed_arg[0]
            arg_value  = parsed_arg[1]
            
            arg_dict[arg_name] = arg_value

            if arg_name not in func_args: 
                print(USAGE_MESSAGE)
                exit(1)

        self.functions[func](**arg_dict)
        exit(0)
                
        

