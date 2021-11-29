from string import ascii_lowercase

from cloudify import ctx
from cloudify.utils import id_generator

predefined_value = ctx.node.properties.get('predefined_value', None)
ctx.instance.runtime_properties['value'] = \
    predefined_value if predefined_value else id_generator(size=6, chars=ascii_lowercase)