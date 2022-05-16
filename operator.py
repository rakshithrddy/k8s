import os
import kopf
import pykube
import logging

from datetime import datetime
from action import Action
import time

# init logger
logger = logging.getLogger(os.path.basename(__file__))

# Documentation of Kopf Framework: https://kopf.readthedocs.io/en/stable/
# For simplicity this is a local operator running on the local machine.

# some helpers


def getApi() -> pykube.HTTPClient:
    config = pykube.KubeConfig.from_file("~/.kube/config")
    return pykube.HTTPClient(config)


# sample get and patch via pykube
def pykubeSampleGetAction(namespace, name) -> Action:
    return Action.objects(getApi(), namespace=namespace).get_by_name(name)


def pykubeSamplePatchAction(ac: Action, patch: dict, subresource) -> Action:
    ac.patch(patch, subresource=subresource)


@kopf.on.login()
def on_login(**kwargs):
    # operator uses local kube-config for connection to the cluster
    return kopf.login_with_kubeconfig(**kwargs)


@kopf.on.update('action')
def action_update(name, namespace, patch, diff, spec, **_):
    logger.info(f"on update: name:{name} diff:{diff}")
    delay = 0
    if spec.get('delay'):
        delay = spec.get('delay')
    
    timestamps = []
    for phase in spec.get('phases'):
        timestamps.append({phase: str(datetime.now())})
        time.sleep(delay)

    patch['status'] = {'timestamps': timestamps}
    

@kopf.on.delete('action')
def action_delete(name, namespace, **_):
    logger.info(f"on delete: name:{name}")
    if _.get('status'):
        _.pop('status')


@kopf.on.create('action')
def action_create(name, namespace, patch, spec, **_):
    logger.info(f"on create: name:{name}")
    # "patch" parameter may be used to give a patch of the resource to kopf once the handler is finished.
    # Here for example we set a fixed delay for every new "Action" that is created, overwriting whatever may be set.
    patch['spec'] = {'delay': 5}
    if not spec.get('phases'):
        raise kopf.PermanentError("No phases found")
    
    status = {}
    for phase in spec.get('phases'):
        status[phase] = {'phase': phase, 'created_on': str(datetime.now())}
    
    patch['status'] = status


@kopf.on.field('core.opdemo.net', 'v1', 'action', field='status')
def action_status_change(name, namespace, diff, **_):
    logger.info(f"on status change: name:{name} diff:{diff}")
    # ac = pykubeSampleGetAction(namespace, name)
    # pykubeSamplePatchAction(ac, {'status': {'iam': 'allwayshere'}}, subresource='status')
