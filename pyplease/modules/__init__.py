import sys
import shutil
import os

import pyplease

from pyplease.config import CONFIG

DEFAULTS = [('git', 'pyplease.modules.git')]

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

class Module(object):    
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

            
        action(values[1:])

    def default(self):
        print pyplease.__doc__.replace('[module]', self.module_name)
        print
        print self.__doc__ or 'The author of this module did not write a docstring'
        print
        print 'Avaiable actions:'
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
            

    # User interaction
    def ask(self, text, default=None, variants=None, tries=3):
        prompt = text
        
        validate = None
        
        if variants:
            prompt += ' (%s)' % ('/'.join(variants))
                
            validate = lambda v: v.lower() in variants
                
                
        if default:
            prompt += ' [%s]' % default

        prompt = '\033[94m[???] %s \033[0m' % prompt
            
        value = raw_input(prompt)

        if not value:
            return default

        if validate and not validate(value):
            self.warn('Invalid value. Please select one of: %s'
                      % ', '.join(variants))
            
            if tries > 1:
                return self.ask(text, variants, default, tries=tries - 1)
                
            raise ValueError('Invalid input!')
        
        return value

    def confirm(self, text):
        return 'y' == self.ask(text, variants=('y', 'n'), default='y')
        
    
    # Output
    def success(self, value):
        print '\033[92m[:-)]', value, '\033[0m'

    def failure(self, value):
        self.warn(value)

    def note(self, value):
        print '[:-|]', value
    
    def warn(self, value):
        print >>sys.stderr, '\033[93m[:-(]', value, '\033[0m'
        
    def extra_params(self, values):
        if values:
            self.warn("I don't know what to do with '%s'" % ' '.join(values))

    # File API
    def backup(self, filename):
        if os.path.exists(filename):
            backup_filename = '%s~' % filename

            shutil.copyfile(filename, backup_filename)

    def normalize_path(self, path):
        return os.path.abspath(os.path.expanduser(path))

    def has_line(self, filename, line):
        return any(l.strip() == line for l in open(filename))

    def append(self, filename, text):
        f = open(filename, 'a')
        f.write(text)
        f.close()

