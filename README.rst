=====================================================
pfm -- a ssh port forward manager for data engineers
=====================================================

Local computers are not enough to handle large amount of data.
In addition, we launch one Jupyter Notebook server for each machine learning task.
Usually local computers are not enough to handle multiple machine learning tasks.
And therefore data scientists do their experiments with Jupyter Notebook
launched in remote hosts such as EC2

To connect Jupyter Notebook servers in remote hosts, we use ssh port forwarding.
Port forwarding is useful since using multiple servers, since we do not consume resources in local PC.

Unfortunately, when connecting multiple server in different hosts and ports numbers, we easily forget
the port or conflict the local port numbers.

pfm manager the remote hosts and port numbers used in port forwarding. Users understand which local
ports are used and which ports are not. Once users register the port forwarding information, pfm generates
ssh parameters any time specifying the task name.

Install
=======

::

    pip install pfm


Usage
=====

Register ssh port forwarding
-----------------------------

::

    $ pfm add -n image-classification --local_port 9999 --host_port 8888 --ssh_server takahi-i-i.ml.aws.com --remote_host localhost


Generate ssh port forward parameters
-------------------------------------

::

    $ ssh `pfm food-nonfood`


List registered ssh ports
--------------------------

::

    $ pfm list
    image-experiments my-ml-instance.ml.aws.com 6666 8888
    text-classification my-ml-instance.ml.aws.com 6666 8888

Delete registerd forwarding element
-----------------------------------

::

    $ pfm delete image-process


License
--------

* Free software: MIT license
