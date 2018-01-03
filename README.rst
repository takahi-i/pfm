=====================================================
pfm -- a ssh port forward manager for data engineers
=====================================================


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
