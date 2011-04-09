import os
import subprocess

from pyplease import modules

class Module(modules.Module):
    """Ssh configurator

    Useful for generating keys etc."""

    @modules.action
    def generate_key(self, args):
        """generates a keypair"""

        self.extra_params(args)
        
        self.prepare_folder()

        if os.path.exists(self.normalize_path('~/.ssh/id_dsa')):
            return self.failure('~/.ssh/id_dsa key already exists!')

        p = subprocess.Popen(['ssh-keygen', '-t', 'dsa']).wait()

        if not p:
            self.success('Seems like the key was generated!')
        else:
            self.failure('Exit code: %s' % p)




    def prepare_folder(self):
        ssh = self.normalize_path('~/.ssh')
        
        if not os.path.isdir(ssh):
            self.note('Creating ~/.ssh (%s), chmod 700' % ssh)
            
            os.mkdir(ssh, 0700)


