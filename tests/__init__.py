import mox

import pyplease

m = mox.Mox()

def mock_module(mod, dont=()):
    # no idea wtf
    
    for d in dir(mod):
        if not d[0] == '_' and d not in dont:
            a = getattr(mod, d)
            if callable(a):
                setattr(mod, d, m.CreateMock(a))

mock_module(pyplease.files)
mock_module(pyplease.interaction, ('note',
                                   'output',
                                   'success',
                                   'colored'))
