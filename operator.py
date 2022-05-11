import os
import kopf
import pykube
import logging

from datetime import datetime
from action import Action

# init logger
logger = logging.getLogger(os.path.basename(__file__))

# Documentation of Kopf Framework: https://kopf.readthedocs.io/en/stable/
# For simplicity this is a local operator running on the local machine.

# some helpers 
def getApi() -> pykube.HTTPClient:
    config = pykube.KubeConfig.from_file("~/.kube/config")
    return  pykube.HTTPClient(config)


# sample get and patch via pykube
def pykubeSampleGetAction(namespace,name) -> Action:
    return Action.objects(getApi(), namespace=namespace).get_by_name(name)

def pykubeSamplePatchAction(ac:Action, patch: dict,subresource) -> Action:
    ac.patch(patch,subresource=subresource)


@kopf.on.login()
def on_login(**kwargs):
    # operator uses local kube-config for connection to the cluster
    return kopf.login_with_kubeconfig(**kwargs)

@kopf.on.update('action')
def action_update(name,namespace,patch,diff, **_):
    logger.info(f"on update: name:{name} diff:{diff}")
    patch['status']={'updatedAt': str(datetime.now()) }
    
@kopf.on.delete('action')
def action_delete(name,namespace, **_):
    logger.info(f"on delete: name:{name}")
    
@kopf.on.create('action')
def action_create(name,namespace,patch, **_):
    logger.info(f"on create: name:{name}")
    # "patch" parameter may be used to give a patch of the resource to kopf once the handler is finished.
    # Here for example we set a fixed delay for every new "Action" that is created, overwriting whatever may be set.
    patch['spec']={'delay': 5}

    
@kopf.on.field('core.opdemo.net', 'v1', 'action', field='status')
def action_status_change(name, namespace,diff, **_):
    logger.info(f"on status change: name:{name} diff:{diff}")
    ac = pykubeSampleGetAction(namespace,name)
    pykubeSamplePatchAction(ac,{'status':{'iam':'allwayshere'}},subresource='status')
