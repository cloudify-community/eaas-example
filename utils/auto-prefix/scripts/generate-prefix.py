from string import ascii_lowercase

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.utils import id_generator

ctx.instance.runtime_properties['prefix'] = \
    inputs['prefix'] if inputs['prefix'] else id_generator(size=6, chars=ascii_lowercase)