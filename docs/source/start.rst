.. _start:

.. role:: bash(code)
	  :language: bash

***************
Getting Started
***************

The following steps get `Open MOS Backend` server up and running.



^^^^^^^^^^^^^^^  
 Pre-requisites
^^^^^^^^^^^^^^^  

* `Open MOS Backend` should work with any UNIX based operating system.
  It has been extensively tested with `Ubuntu 18.04` as a local environment.
* Install `postgresql`, `redis-server`, and `rabbitmq-server` services
  (all available from "apt" package manager if using Ubuntu for example).  
* Environment variables configuration is necessary [more].
  
^^^^^^^^^^^^^^^  
 Dependencies
^^^^^^^^^^^^^^^  

Install dependencies with :bash:`sudo pip3 install -r requirements.txt`. 

^^^^^^^^^^^^^^^
 Launching
^^^^^^^^^^^^^^^

Launch the `mos.backend` server by executing the command:

:bash:`./manage.py run_mos_backend`

Then, the REST API is available at :bash:`localhost:8000/api`.



