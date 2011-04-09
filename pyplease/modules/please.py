import os
import ConfigParser

from pyplease import modules


class Module(modules.Module):
    """Please configurator"""

    @modules.action('[module_name]', 'adds/edits a module for Please')
    def add(self, values):
        module_name = self.get_module_name(values)
        
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

    @modules.action('[module_name]', 'removes a module from Please')
    def remove(self, values):
        module_name = self.get_module_name(values)

        self.extra_params(values[1:])

        config = self.get_config()
            
        try:
            path = config.get('modules', module_name)
        except Exception:
            self.failure("Can't find module '%s' in the config '%s'"
                         % (module_name, self.config_path))
            return

        config.remove_option('modules', module_name)

        config.write(open(self.config_path, 'wb'))

        self.success('Removed "%s" from "%s"' % (module_name, path))

    def get_module_name(self, values):
        if values:
            return values[0]
        else:
            return self.ask('Module name?')
        
    
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
