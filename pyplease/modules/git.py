import os
import subprocess

from pyplease import modules

def git_option_query(option):
    return modules.check_output(['git', 'config', option])

def git_option_set(option, value):
    subprocess.call(['git', 'config', '--global', option, value])

def git_option_unset(option):
    subprocess.call(['git', 'config', '--global', '--unset', option])

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
        return git_option_query(name)

    def set(self, name, value):
        return git_option_set(name, value)
