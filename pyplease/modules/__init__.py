import sys
import shutil

import pyplease

from pyplease.config import CONFIG

MODULES = dict(CONFIG.items('modules'))

def get_module(name):
    module = MODULES[name]
    
    m = __import__(module)
    
    attrs = module.split('.')

    for a in attrs[1:]:
        m = getattr(m, a)

    return m.Module(name)

def get_module_list():
    return MODULES.keys()
        

def action(args, description):
    def _decorator(func):
        func.action_name = func.func_name
        func.action_args = args
        func.action_description = description
        return func
    
    return _decorator

class Module(object):    
    # External API
    def __init__(self, module_name):
        self.module_name = module_name
    
    def act(self, values):
        if len(values) < 1:
            self.default()
            return

        act = values[0]

        getattr(self, act)(values[1:])

    def default(self):
        print pyplease.__doc__.replace('[module]', self.module_name)
        print
        print self.__doc__ or 'The author of this module did not write a docstring'
        print
        print 'Avaiable actions:'
        print

        for action in self.avaiable_actions():
            act = ' '.join(action[:2])
            print '    {0:20s} - {1}'.format(act, action[2])

    def avaiable_actions(self):
        for method in dir(self):
            try:
                m = getattr(self, method)
                if m.action_name:
                    yield m.action_name, m.action_args, m.action_description
            except AttributeError:
                pass

    # User interaction
    def ask(self, text, default=None):
        if default:
            text += ' [%s]' % default

        text = '[???] %s ' % text
            
        value = raw_input(text)

        if not value:
            return default

        return value

    # Output
    def success(self, value):
        print '[:-)]', value

    def failure(self, value):
        self.warn(value)

    def note(self, value):
        print '[:-|]', value
    
    def warn(self, value):
        print >>sys.stderr, '[:-(]', value
        
    def extra_params(self, values):
        if values:
            self.warn("I don't know what to do with '%s'" % ' '.join(values))

    # File API
    def backup(self, filename):
        backup_filename = '%s~' % filename

        shutil.copyfile(filename, backup_filename)
