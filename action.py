from pykube.objects import NamespacedAPIObject

class Action(NamespacedAPIObject):
    version = "core.opdemo.net/v1"
    endpoint = "actions"
    kind = "Action"
