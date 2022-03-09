.. _overview:

********
Overview
********

`Open MOS Backend` provides a server that allows an optimization model
be accessible via a REST API.



^^^^^^^^^^^^^^^  
Functional overview
^^^^^^^^^^^^^^^  

An optimization model, contained in a single file in one of the
supported modeling languages, is parsed, allowing the structure of the
optimization model to be recognized.
The components that comprise this structure are then made accessible
to view and modify by a generated REST API.
Furthermore, from the information provided, a model recipe is prepared
which the `MOS Compute` capability can be called to execute and
solve the associated optimization model.



^^^^^^^^^^^^^^^  
Technology overview
^^^^^^^^^^^^^^^  


`Open MOS Backend` is written in Python and built on the `Django` Web framework.
