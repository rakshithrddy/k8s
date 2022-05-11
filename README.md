# The Task:

Modyfy the operator that it acts as follows:

- If a Action resource is present and has a list of phases in its spec: 
    The operator shall walk throu the list of phases and set "{"status":{"phase":phase}}" to each of the phase listed in the spec until the last phase is reached.
    The delay between each phase shall be the value of "spec.delay".

- The process shall be event driven without the use of timers.

- Once the last phase is reached the resource is finished and can be deleted. Recreate it for a new run.

- The "status" of the resource shall contain a list of timestamps for each beginning of a phase
    {"status":{"timestamps":[{phase:starttime}]}}

- The code shall serve as an example only. Feel free to restructure it for your needs.


# Setup
This was tested on Ubuntu 20.04 but could as well work in Windows WSL

Install python3.8
    <depend on your distro>

Install required python packages

    pip3 install -r ./requirements.txt 

Set up minikube or get access to kubernetes cluster

Install kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

Create your kubectl configuration file in ~/.kube/config

Checking cluster conectivity

    kubectl config view
    kubectl cluster-info

Optional install Visual Studio Code: https://code.visualstudio.com/download#

Sample debugging config for VS-Code

    {
        "name": "kopf Framework",
        "type": "python",
        "request": "launch",
        "program": "../.local/bin/kopf",
        "args": [
            "run",
            "${file}",
            "--verbose",
            "--standalone",
            "--namespace=<your-namespace>"
        ],
        "env": {
            "YOUR_VARIABLE": "goes-here"
        },
        "console": "internalConsole",
        "justMyCode": true
    }

## How to run

source your settings

    cd operator-demo
    . ./.env

 Create the custom resource definition. This may require cluster-admin role
    kubectl apply -f crd.yaml

Run the operator locally and namespaced or use debugging mode in an IDE (see above)

    ~/.local/bin/kopf run operator.py --verbose --standalone --namespace=$NAMESPACE

Create a custom resource. 

    kubectl -n $NAMESPACE apply -f action.yaml

Alter the custom resource (change the delay value for instance.)

    kubectl -n $NAMESPACE edit action demo-action1
    

Hava a look at the resources

    kubectl -n $NAMESPACE get actions.core.opdemo.net -o yaml

Delete the custom resource

    kubectl -n $NAMESPACE delete action demo-action1

See the operator logs ...

# How to deliver solution
Fork this into your public repo, provide link to your repo with any additional instructions on how to test 



