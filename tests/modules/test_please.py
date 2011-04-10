import mox
import ConfigParser
import os

from .. import m

import pyplease

# mocked:

from pyplease import files
from pyplease import interaction

# everything else:

from pyplease.modules import please

BRC = '/tmp/bashrc'
CFG = '/tmp/pyplease'


def testAddRemove():
    if os.path.exists(CFG):
        os.remove(CFG)
    m.ResetAll()

    # add

    interaction.ask_path(mox.StrContains('config'),
                         default='~/.pyplease').AndReturn(CFG)

    files.backup(CFG)

    interaction.ask(mox.StrContains('name'), default=None).AndReturn('omg_module')
    interaction.ask(mox.StrContains('package'), default=None).AndReturn('superomg')

    # remove
    
    interaction.ask_path(mox.StrContains('config'),
                         default='~/.pyplease').AndReturn(CFG)

    files.backup(CFG)

    interaction.ask(mox.StrContains('name'), default=None).AndReturn('omg_module')
    
    m.ReplayAll()

    assert not please.Module('please').add()

    config = ConfigParser.ConfigParser()
    
    config.read([CFG])

    assert config.get('modules', 'omg_module') == 'superomg'

    assert not please.Module('please').remove()

    config = ConfigParser.ConfigParser()
    
    config.read([CFG])

    assert not config.has_option('modules', 'omg_module')
    

    os.remove(CFG)
    
    m.VerifyAll()

def testDefaults():
    if os.path.exists(CFG):
        os.remove(CFG)
        
    m.ResetAll()
    
    interaction.ask_path(mox.StrContains('config'),
                         default='~/.pyplease').AndReturn(CFG)

    files.backup(CFG)

    interaction.confirm('Install "ssh"?').AndReturn(True)
    interaction.confirm('Install "git"?').AndReturn(False)
    interaction.confirm('Install "github"?').AndReturn(False)
    
    m.ReplayAll()
    
    assert not please.Module('please').defaults()
    
    config = ConfigParser.ConfigParser()
    
    config.read([CFG])

    assert config.has_option('modules', 'ssh')
    assert not config.has_option('modules', 'git')
    assert not config.has_option('modules', 'github')

    os.remove(CFG)
    
    m.VerifyAll()

def testAutocompleteSuccess():
    m.ResetAll()
    
    TMP = '/tmp/.bashrc'
    
    interaction.ask_path(mox.StrContains('Path'),
                         default='~/.bashrc').AndReturn(TMP)
    
    files.has_line(TMP, please.AUTOCOMPLETE_CMD).AndReturn(False)

    files.backup(TMP)

    files.append(TMP, mox.StrContains(please.AUTOCOMPLETE_CMD))
    
    m.ReplayAll()

    assert not please.Module('please').autocomplete()
    
    m.VerifyAll()

def testAutocompleteFailure():
    m.ResetAll()
    
    TMP = '/tmp/.bashrc'
    
    interaction.ask_path(mox.StrContains('Path'),
                         default='~/.bashrc').AndReturn(TMP)
    
    files.has_line(TMP, please.AUTOCOMPLETE_CMD).AndReturn(True)

    interaction.failure('Autocomplete seems already enabled')
    
    m.ReplayAll()

    assert please.Module('please').autocomplete()
    
    m.VerifyAll()
