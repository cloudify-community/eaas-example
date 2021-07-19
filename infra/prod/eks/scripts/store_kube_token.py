import base64

from cloudify.state import ctx_parameters as inputs
from cloudify import ctx


ctx.instance.runtime_properties['kube_token'] = base64.b64decode(inputs['kube_token']).decode('utf-8').replace("'", '"')