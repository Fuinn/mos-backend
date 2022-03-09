.. _abstraction:

***************
Abstraction
***************

That optimization models have a common structure is harnessed
to yield the abstraction that `Open MOS Backend` is built upon.



---------------
 Components
---------------

The components of an optimization model that MOS recognizes (and that
may be accessed and modified through the REST API):

* **Model:** Name of model. The model may be accessed by API by its name.
* **Input File:** Input file to be uploaded via API.
* **Input Object:**  Numerical or text input to model, required to be specified by user before running model. Text is required to be bracketed by "".
* **Helper Object:** Numerical or text item, either hard-coded or calculated based on inputs. No
  direct access to modify this object through the API. Helper objects
  defined in code before the solve statement are tagged with 'Pre-opt', and helper objects defined after the solve statement are represented in the 'Post-opt' tab.
* **Variable:** A model variable
* **Constraint:** A model constraint
* **Function:** A function comprising model variables, for example the
  objective function of a problem, or part of a constraint.
* **Problem:** Problem definition, bringing the model functions, variables, and constraints together.
* **Solver:** Solver definition
* **Output File:** Output file (contents defined in code), accessible
  via API.





