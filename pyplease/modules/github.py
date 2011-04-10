try:
    import github2.client
except ImportError:
    import sys
    print >>sys.stderr, 'Please install github2 api library: $ sudo pip install github2'
    sys.exit(1)

import os
import subprocess
    
from pyplease import modules

from pyplease.modules.git import git_option_query, git_option_set

class Module(modules.Module):
    """Github modules

    better integration"""
    username = None

    @modules.action
    def startproject(self, values):
        """creates new project, uploads current git repository to github"""
        self.ensure_client()

        origin = self.get_current_origin()

        if origin:
            self.note('Your origin is "%s"' % origin)
            self.failure('It seems like your project already has an origin')

            return

        project_dir = self.get_working_dir()

        if not project_dir:
            self.failure('You haven\'t done "git init" yet!')
            if self.confirm('Init repository in this directory?'):
                subprocess.call(['git', 'init'])

                project_dir = self.get_working_dir()
            else:
                self.failure('Init repository and commit something, then we\'ll talk!')
                return

        self.note('Working dir: %s' % project_dir)

        project_name = os.path.basename(project_dir)
        

        project_name = self.ask('Project name?', project_name)
        public = self.confirm('Public?')
        description = self.ask('Description?')
        homepage = self.ask('Homepage?')

        self.note('Creating a repo...')
        self.client.repos.create(project_name,
                                 description,
                                 homepage,
                                 public)
        
        self.note('Querying it back...')
        new_repo = self.client.repos.show('%s/%s' % (self.username,
                                                     project_name))

        self.success('Repository %s was created!' % new_repo.name)

        origin = 'git@github.com:%s/%s.git' % (self.username, project_name)
        
        self.note('Setting origin to "%s"' % origin)

        subprocess.call(['git', 'remote', 'add', 'origin', origin])

        self.note('The first push!')

        subprocess.call(['git', 'push', 'origin', 'master'])

        self.success('Looks good? Take a look at %s' % new_repo.url)

        self.note('If it says "error", then maybe you had no commits. '
                  'Please commit something and run "git push origin master"')

        self.success("Please don't forget README or README.markdown!")
        self.success("You can use 'git push' from now on.")

                  

    def get_current_origin(self):
        origin = git_option_query('remote.origin.url')

        return origin


    def get_working_dir(self):
        return modules.check_output(['git', 'rev-parse', '--show-toplevel'])
        
        

    def get_username(self, reask=False):
        if self.username:
            return self.username
        
        username = git_option_query('github.username')

        if not username:
            git_username = git_option_query('user.name')

        if not username or reask:
            username = self.ask('Your github username?', username or git_username)
            
        git_option_set('github.username', username)
        self.username = username

        return username

    def get_token(self, reask=False):
        token = git_option_query('github.token')
        
        if not token or\
                (reask and
                 not self.confirm('We have a token in your git config, use it?')):
                
            self.note('Please give me an api token from https://github.com/account/admin')

            token = self.ask('Token?')

            git_option_set('github.token', token)

        return token
        
    def ensure_client(self, retry=False):
        username = self.get_username(reask=retry)
        self.note('Using "%s" as your github username' % username)

        token = self.get_token(reask=retry)
        self.note('We have github token for %s' % username)

        
        self.client = github2.client.Github(username=username,
                                            api_token=token)

        # try it
        self.note('Trying out connection...')
        
        try:
            user = self.client.users.show(username)
        except Exception: # that was RuntimeError but I think they gonna change it
            self.failure('Does not seem like your token is valid!')

            if self.confirm('Try again?'):
                return self.ensure_client(retry=True)

        self.success('Your name is %s. Seems like connection is okay' % user.name)

        
        
        

        
