import os
import subprocess

from pyplease import modules

def check_output(args):
    try:
        # 2.7
        return subprocess.check_output(args)
    except AttributeError:
        pass

    p = subprocess.Popen(args, stdout=subprocess.PIPE)

    ret = p.communicate()[0]

    return ret.rstrip()

class Module(modules.Module):
    """Git configurator

    Configures git by using Git's command line API,
    not by raw config handling"""

    @modules.action
    def configure(self, values):
        """configures several important parameters"""
        self.extra_params(values)

        self.username()
        
        self.email()

    @modules.action('[username]')
    def username(self, values=[]):
        """sets username""" 
        current = self.query('user.name')
        
        username = (values and values[0]) or self.ask('Your username?', current)
        
        self.set('user.name', username)
        
        self.success('Your git username is %s from now on'
                     % self.query('user.name'))

        
    @modules.action('[email]')
    def email(self, values=[]):
        """sets email"""
        current = self.query('user.email')
        
        username = (values and values[0]) or self.ask('Your email?', current)
        
        self.set('user.email', username)
        
        self.success('Your git email is %s from now on'
                     % self.query('user.email'))



    def query(self, name):
        return check_output(['git', 'config', name])

    def set(self, name, value):
        subprocess.call(['git', 'config', name, value])
