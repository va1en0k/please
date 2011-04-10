"""Direct interaction with user"""

import sys

from pyplease.colors import colored
from pyplease import utils, files, validators

#from pyplease.interaction import console as backend

MOODS = {'question': '???',
         'success': ':-)',
         'failure': ':-(',
         'warn': ':-('}

def output(format_string, p_type, **kwargs):
    pt = format_string.format(**kwargs)
    
    pt = '[{mood}] {pt}'.format(mood=MOODS.get(p_type, ':-|'),
                                pt=pt)
    
    return colored(pt, p_type)


def ask(text, default=None, variants=None, validate=None, tries=3):
    """Asks user for a string-value
    
    text - the text of question
    default - if not None, the default value, used if answer is blank
    variants - a list of variants (don't use with validate) (deprecated!)
    validate - a validation object (see pyplease.interaction.validate)
    or a function (str -> bool)
    tries - a number of tries (if validate is not None)

    {text} ({variant1/variant2/...}) [{default}] """

    variants_prompt = default_prompt = ''
    
    if variants:
        variants_prompt = ' (%s)' % ('/'.join(variants))
        
        validate = validators.variants(variants)
        
        
    if default:
        default_prompt = ' [%s]' % default

    pt = output('{text}{variants_prompt}{default_prompt} ',
                'question',
                text=text,
                default_prompt=default_prompt,
                variants_prompt=variants_prompt)
    
    value = raw_input(pt)

    if default is not None and not value:
        return default

    if validate is not None and not validate(value):
        
        try:
            msg = validate.error_message
        except AttributeError:
            msg = ("Invalid value. Please ask module maintainer "
                   "to use a better error message :-)")

        warn(msg)
        
        if tries > 1:
            return ask(text=text,
                       variants=variants,
                       default=default,
                       validate=validate,
                       tries=tries - 1)
        
        raise ValueError('Invalid input!')
    
    return value

def confirm(text):
    """Confirms ((yes/no) -> bool)"""
    return 'y' == ask(text,
                      variants=('y', 'n'),
                      default='y').lower()

def success(text):
    print output(text, 'success')

def failure(text):
    print >>sys.stderr, output(text, 'failure')

def note(text):
    print output(text, 'note')

def warn(text):
    print >>sys.stderr, output(text, 'warn')

def ask_path(text, **kwargs):
    path = ask(text, **kwargs)

    return files.normalize_path(path)


class InteractionMixin(object):
    # INPUT
    def ask(self, text, default=None, **kwargs):
        return ask(text, default=default, **kwargs)
    
    def ask_path(self, text, default=None, **kwargs):
        return ask_path(text, default=default)
    
    def confirm(self, text):
        return confirm(text)

    # OUTPUT
    def success(self, value):
        success(value)
        return 0

    def failure(self, value):
        failure(value)
        return 1

    def note(self, value):
        note(value)
    
    def warn(self, value):
        warn(value)


