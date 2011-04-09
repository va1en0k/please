"""Pyplease is a simple command-line configurator

please [module] [action...]"""

import sys

from pyplease.modules import get_module, get_module_list

def print_help():
    print __doc__
    print
    print 'Avaiable modules list: '
    print 

    for m in get_module_list():
        print '    ', m

    
def main(argv=None):
    argv = argv or sys.argv
    
    if len(argv) < 2:
        print_help()

        return
    
    vocative = sys.argv[1]
    action = sys.argv[2:]

    action_module = get_module(vocative)
    action_module.act(action)

if __name__ == '__main__':
    main()
