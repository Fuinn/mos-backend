.. _api:

.. role:: bash(code)
	  :language: bash

***************
REST API
***************

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
REST API Design Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
While the MOS Interface Python and Julia packages enable access to the MOS REST API, the REST API may also be accessed directly.

[Link] contains a more detailed specification, while here we outline the main components.

Information is supplied to, or received from, a request in JSON form.


Commands relating to the creation, deletion, running of models have urls commencing with the form ``/api/model/``.

Commands relating to particular model components, for example a variable, have urls with the form ``/api/variable/``. Inputs can be passed to a model through associated commands around ``interface objects`` and ``interface files``, whereas information on the solution may be extracted from associated commands around such components as ``variable``, ``constraint``, ``problem``, and ``solver``.
