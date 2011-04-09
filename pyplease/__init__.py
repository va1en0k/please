import sys


from pyplease.modules import get_module

def print_help():
    import pyplease
    
    help(pyplease)


    
def main(argv=None):
    argv = argv or sys.argv
    
    if len(argv) < 2:
        print_help()

        return
    
    vocative = sys.argv[1]
    action = sys.argv[2:]

    action_module = get_module(vocative)
    action_module.act(action)
