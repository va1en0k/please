import nose
import mox

from .. import m

import pyplease

# mocked:

from pyplease import files
from pyplease import interaction

# everything else:

from pyplease.modules import please


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
