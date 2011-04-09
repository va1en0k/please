import os
import ConfigParser

from pyplease import modules


class Module(modules.Module):

    def get_config(self):
        try:
            return self.config
        except AttributeError:
            pass

        self.config = ConfigParser.ConfigParser()
        
        path = self.ask('Path to the config?', '~/.pyplease')

        path = os.path.abspath(os.path.expanduser(path))

        self.note('Using "%s" as config' % path)

        self.config.read([path])
        self.config_path = path

        return self.config


    def add_module(self, values):
        module_name = values[0]
        
        if values[1:]:
            self.extra_params(values[1:])

        config = self.get_config()
            
        try:
            path = config.get('modules', module_name)
        except Exception:
            path = None

        path = self.ask('Path to the module?', path)

        self.backup(self.config_path)

        config.set('modules', module_name, path)

        config.write(open(self.config_path, 'wb'))

        self.success('Registered "%s" as "%s"' % (module_name, path))
    
    def add(self, values):
        what = values[0]

        action = 'add_%s' % what

        getattr(self, action)(values[1:])
