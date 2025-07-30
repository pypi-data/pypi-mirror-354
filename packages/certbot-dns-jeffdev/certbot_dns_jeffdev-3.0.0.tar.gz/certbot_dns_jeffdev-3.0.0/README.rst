Jeffdev DNS DNS Authenticator Plugin for Certbot
==============================================

Installation
------------

This package can be installed with pip

.. code:: bash

    pip install certbot-dns-jeffdev

and can be upgraded using the ``--upgrade`` flag

.. code:: bash

    pip install --upgrade certbot-dns-jeffdev

Credentials
-----------

.. code:: ini
   :name: certbot_jeffdev_token.ini

   # Jeffdev DNS API token used by Certbot
   dns_jeffdev_api_key = a65e8ebd-45ab-44d2-a542-40d4d009e3bf

Examples
--------

.. code:: bash

   certbot certonly \
     --authenticator dns-jeffdev \
     --dns-jeffdev-credentials ~/.secrets/certbot/jeffdev.ini \
     -d example.com

.. code:: bash

   certbot certonly \
     --authenticator dns-jeffdev \
     --dns-jeffdev-credentials ~/.secrets/certbot/jeffdev.ini \
     -d example.com \
     -d www.example.com

.. code:: bash

   certbot certonly \
     --authenticator dns-jeffdev \
     --dns-jeffdev-credentials ~/.secrets/certbot/jeffdev.ini \
     --dns-jeffdev-propagation-seconds 60 \
     -d example.com
