Introduction
==================


netmiko_balabit is an out of tree netmiko driver for the balabit shell control box.


Installation
------------

Install jinjamator by running:

    pip3 install netmiko_balabit

Usage
-----

.. code-block:: python

    from netmiko import ConnectHandler
    import  netmiko_balabit

    target = {
        'device_type': 'balabit_scb',
        'target_device_type': 'linux',
        'ip': ssh_host, # ip of balabit gateway
        'username': ssh_username, # gu=<balabit_username>@<target_username>@<target_ip>
        'password': [ssh_gw_password,ssh_password], # password list [<balabit_password>,<target_password>]
        'port': 22,
    }

    ssh = ConnectHandler(**target)
    print(ssh.send_command("ls /"))


Contribute
----------

- Issue Tracker: https://github.com/jinjamator/netmiko_balabit/issues
- Source Code: https://github.com/jinjamator/netmiko_balabit

License
-----------------

This project is licensed under the Apache License Version 2.0