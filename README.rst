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


``pfm add `` registers port forward settings.

::

    $ pfm add -n image-classification --local_port 9999 --host_port 8888 --ssh_server takahi-i-i.ml.aws.com --remote_host localhost


Generate ssh port forward parameters
-------------------------------------


After the registration of port forward settings with ``pfm add `` , we can generate ssh parameters with `pfm param`.

::

    $ ssh `pfm param image-classification`


List registered ssh ports
--------------------------

We can see the list of registered port forward settings.

::

    $ pfm list
    +----------------------+------------+------------+--------------------------------+------------+-----------------+--------------------------------+--------------+
    |         name         |    type    | local_port |          remote_host           | host_port  |   login_user    |           ssh_server           | server_port  |
    +======================+============+============+================================+============+=================+================================+==============+
    | image-processing     | L          | 9999       | localhost                      | 8888       | None            | my-ml-instance.aws.com         |              |
    +----------------------+------------+------------+--------------------------------+------------+-----------------+--------------------------------+--------------+
    | text-processing      | L          | 7777       | localhost                      | 8888       | None            | my-ml-instance-2.aws.com       |              |
    +----------------------+------------+------------+--------------------------------+------------+-----------------+--------------------------------+--------------+

Delete registerd forwarding element
-----------------------------------

When a port forward settings is not needed, we can remove the setting with ``pfm delete`` command

::

    $ pfm delete image-process


License
--------

* Free software: MIT license
