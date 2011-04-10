import shutil
import os

def normalize_path(path):
    """Returns absolute path

    expands all ~"""
    
    return os.path.abspath(os.path.expanduser(path))

def backup(filename):
    """Backups file, if it's present"""

    path = normalize_path(filename)
    
    if os.path.exists(path):
        backup_filename = '%s~' % path

        shutil.copyfile(path, backup_filename)

        
def has_line(filename, fil):
    """Has file a line which satisifies predicate?

    If fil is not callable, just compares it with all lines"""
    
    if not callable(fil):
        _f = lambda l: l.strip() == fil
    else:
        _f = line
        
    try:
        f = open(normalize_path(filename))
        return any(_f(l) for l in f)
    finally:
        f.close()


def remove_lines(filename, fil):
    """Removes all lines which satisfy predicate

    If fil is not callable, just compares it with all lines"""
    
    if not callable(fil):
        _f = lambda l: l.strip() == fil
    else:
        _f = line

    path = normalize_path(filename)

    lines = [l for l in open(path) if not _f(l)]

    f = open(path, 'w')
    for l in lines:
        f.write(l)
    f.close()

    

def append(filename, text):
    """Append text to file"""
    
    f = open(normalize_path(filename), 'a')
    f.write(text)
    f.close()

