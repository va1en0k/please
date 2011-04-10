import sys
import shutil
import os
import subprocess

import pyplease

from pyplease.config import CONFIG
from pyplease.interaction import InteractionMixin
from pyplease import utils

DEFAULTS = [('ssh', 'pyplease.modules.ssh'),
            ('git', 'pyplease.modules.git'),
            ('github', 'pyplease.modules.github')]

try:
    MODULES = dict(CONFIG.items('modules'))
except:
    MODULES = dict()
    
MODULES['please'] = 'pyplease.modules.please' # always!

def get_module(name):
    module = MODULES[name]
    
    m = __import__(module)
    
    attrs = module.split('.')

    for a in attrs[1:]:
        m = getattr(m, a)

    return m.Module(name)

def get_module_list():
    return MODULES.keys()
        

def action(args='', description=None):
    def _decorator(func):
        func.action_name = func.func_name
        func.action_args = args
        func.action_description = description or func.__doc__
        return func

    if callable(args):
        func = args
        args = ''
        return _decorator(func)
    
    return _decorator

def check_output(args):
    try:
        # 2.7
        return subprocess.check_output(args)
    except AttributeError:
        pass

    p = subprocess.Popen(args, stdout=subprocess.PIPE)

    ret = p.communicate()[0]

    return ret.rstrip()


class Module(InteractionMixin):
    # External API
    def __init__(self, module_name):
        self.module_name = module_name
    
    def act(self, values):
        if len(values) < 1:
            self.default()
            return

        act = values[0]

        try:
            action = getattr(self, act)
            
            self.note('%s %s: %s'
                      % (self.module_name,
                         action.action_name,
                         action.action_description))
        except AttributeError:
            self.failure('No such action: %s!' % act)
            return

        return action()

    def default(self):
        print pyplease.__doc__.replace('[module]', self.module_name)
        print
        print self.__doc__ or 'The author of this module did not write a docstring'
        print
        print 'Available actions:'
        print

        for action in self.avaiable_actions():
            act = ' '.join(action[:2])
            print '    {0:24s} - {1}'.format(act, action[2])

    def avaiable_actions(self):
        for method in dir(self):
            try:
                m = getattr(self, method)
                if m.action_name:
                    yield m.action_name, m.action_args, m.action_description
            except AttributeError:
                pass

    def completion(self, prefix, argv):
        if len(argv) == 0 or (len(argv) == 1 and prefix):
            for name, args, description in self.avaiable_actions():
                if name.startswith(prefix):
                    print name
            

    # Output
        
    def extra_params(self, values):
        if values:
            self.warn("I don't know what to do with '%s'" % ' '.join(values))

