import sys
import shutil

from pyplease.config import CONFIG

MODULES = dict(CONFIG.items('modules'))

def get_module(name):
    module = MODULES[name]
    
    m = __import__(module)
    
    attrs = module.split('.')

    for a in attrs[1:]:
        m = getattr(m, a)

    return m.Module()


class Module(object):
    # External API
    def act(self, values):
        if len(values) < 0:
            self.default()

        act = values[0]

        getattr(self, act)(values[1:])

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

    def note(self, value):
        print '[:-|]', value
    
    def warn(self, value):
        print >>sys.stderr, '[:-(]', value
        
    def extra_params(self, values):
        self.warn("I don't know what to do with '%s'" % ' '.join(values))

    # File API
    def backup(self, filename):
        backup_filename = '%s~' % filename

        shutil.copyfile(filename, backup_filename)
