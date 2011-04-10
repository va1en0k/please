import os
import ConfigParser

from pyplease import modules, files

AUTOCOMPLETE_CMD = """complete -C 'please --complete "$COMP_LINE"' please || true"""    

class Module(modules.Module):
    """Please configurator"""

    @modules.action
    def add(self):
        """adds/edits a module for Please"""
        
        config = self.get_config()
        
        module_name = self.ask('Module name?')
        
        try:
            path = config.get('modules', module_name)
        except Exception:
            path = None

        path = self.ask('Python package?', path)

        files.backup(self.config_path)
        
        self.register(module_name, path)

        self.success('Registered "%s" as "%s"' % (module_name, path))

    @modules.action
    def remove(self):
        """removes a module from Please"""
        config = self.get_config()
        
        module_name = self.ask('Module name?')

        try:
            path = config.get('modules', module_name)
        except Exception:
            return self.failure("Can't find module '%s' in the config '%s'"
                                % (module_name, self.config_path))

        config.remove_option('modules', module_name)

        files.backup(self.config_path)

        config.write(open(self.config_path, 'wb'))

        self.success('Removed "%s" from "%s"' % (module_name, path))

    @modules.action
    def defaults(self):
        """registers default modules"""
        
        self.get_config() # before everything
        
        files.backup(self.config_path)
        
        for module_name, path in modules.DEFAULTS:
            install = self.confirm('Install "%s"?' % module_name)

            if install:
                self.register(module_name, path)
                self.success('Registered "%s"' % module_name)

    @modules.action
    def autocomplete_disable(self):
        
        bashrc = self.ask_path('Path to the bashrc file?', '~/.bashrc')

        self.note('Using "%s" as bashrc' % bashrc)

        files.backup(bashrc)
        files.remove_lines(bashrc, AUTOCOMPLETE_CMD)

        self.success('Autocomplete disabled!')



    @modules.action
    def autocomplete(self):
        """enables autocompetion (if you have bash-autocomplete)"""
        
        bashrc = self.ask_path('Path to the bashrc file?', '~/.bashrc')

        self.note('Using "%s" as bashrc' % bashrc)
        
        if files.has_line(bashrc, AUTOCOMPLETE_CMD):
            return self.failure('Autocomplete seems already enabled')
        
        files.backup(bashrc)
        
        files.append(bashrc, "\n%s\n\n" % AUTOCOMPLETE_CMD)
        
        return self.success('Autocomplete enabled! Please re-login or use `source ~/.bashrc`')

        
        
    @modules.action
    def configure(self, values):
        """configures everything: default modules and autocompletion"""
        
        self.defaults()
        self.autocomplete()
        

    def register(self, module_name, path):
        config = self.get_config()
        
        if not config.has_section('modules'):
            config.add_section('modules')

        config.set('modules', module_name, path)

        config.write(open(self.config_path, 'wb'))
    
    def get_config(self):
        try:
            return self.config
        except AttributeError:
            pass

        self.config = ConfigParser.ConfigParser()
        
        path = self.ask_path('Path to the config?', '~/.pyplease')

        self.note('Using "%s" as config' % path)

        self.config.read([path])
        self.config_path = path

        return self.config
