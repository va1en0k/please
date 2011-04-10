"""Pyplease is a simple command-line configurator

please [module] [action...]"""

import sys
import shlex

def init_readline():
    from pyplease.files import normalize_path

    HISTORY_FILE = normalize_path('~/.pleasehistory')

    try:
        import readline
        readline.read_history_file(HISTORY_FILE)
    except:
        pass

def end_readline():
    from pyplease.files import normalize_path

    HISTORY_FILE = normalize_path('~/.pleasehistory')
    
    try:
        import readline
        readline.write_history_file(HISTORY_FILE)
    except:
        pass

def print_help():
    from pyplease.modules import get_module, get_module_list
    
    print __doc__
    print
    print 'Avaiable modules list: '
    print 

    for m in get_module_list():
        print '    ', m

def completion(argv):
    from pyplease.modules import get_module, get_module_list

    line, cmd, prefix, last_word = argv

    t_argv = shlex.split(line)
    
    if len(t_argv) == 1 or (len(t_argv) == 2 and prefix):
        # module
    
        for m in get_module_list():
            if m.startswith(prefix):
                print m


    else:
        try:
            m = get_module(t_argv[1])
            m.completion(prefix, t_argv[2:])
        except:
            pass

def run_argv(argv):
    from pyplease.modules import get_module
    
    vocative = argv[1]
    action = argv[2:]
    
    action_module = get_module(vocative)
    
    return action_module.act(action)



    
def main(argv=None):

    
    argv = argv or sys.argv
    
    if len(argv) < 2:
        print_help()

        return

    if argv[1] == '--complete':
        completion(argv[2:])
        return

    try:
        init_readline()

        code = run_argv(argv)

        end_readline()

        
    except Exception:
        print >>sys.stderr, "\n\n[:-(] Please run with as few as possible arguments to see help"
        raise

if __name__ == '__main__':
    main()
