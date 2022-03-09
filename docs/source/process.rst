.. _process:


---------------
 Process
---------------

***************
 Annotating a Model File
***************


For MOS to recognize the structural components of a model in an optimization model
file, each component may be tagged by a keyword. The keyword is the
name as each component defined in the `model abstraction
<abstraction.html>`_ section of the documentation, e.g.
::
   #@ Variable: x


An optional Description keyword may follow, e.g.
::
   #@ Variable: x
   #@ Description: x=1 location selected, x=0 otherwise

There is a choice in what model components are shown to the user, or
made available through the API, subject to any language specific issues outlined **here**.



***************
Model Languages
***************

There are some limitations on structure of the programs using the
modeling languages for seamless integration with MOS.

To view the code that sets out the rules for parsing files in each
modeling language see ``./mos/backend/io/``

^^^^^^^^^^^^^^^^^^^
 CVXPY
^^^^^^^^^^^^^^^^^^^

* Necessity to import json
* ``mos_labels`` is a dictionary object to allow labeling of keys,
  with form
  ``\{'item name' : 'label'\}``.

^^^^^^^^^^^^^^^^^^^
 GAMS
^^^^^^^^^^^^^^^^^^^

Input objects are restricted to being scalars, with Scalar capitalized in the GAMS definition.

At present, the MOS function structure does not work with GAMS. Thus, it is required to be define a variable to maximized/minimized, and with a constraint setting that variable equal to the objective function.

A parameter named 'solver' is required, with some GAMS solver outputs populated as per examples.

^^^^^^^^^^^^^^^^^^^
 Julia / JuMP
^^^^^^^^^^^^^^^^^^^

No specific restrictions.

^^^^^^^^^^^^^^^^^^^
 OPTMOD
^^^^^^^^^^^^^^^^^^^

No specific restrictions.


***************
Annotation Example
***************

Extract from an annotated optimization model file describing a Lasso
regression problem formulated in CVXPY:
::
   #@ Model: Lasso
   #@ Description: Machine Learning: Lasso Regression

   import cvxpy as cp
   import numpy as np
   import json

   np.random.seed(1)

   #@ Helper Object: m
   #@ Description: number of data points
   m = 100

   #@ Helper Object: n
   #@ Description: number of features
   n = 20

   #@ Helper Object: sigma
   #@ Description: $$\sigma$$ parameter for generating random dataset
   sigma = 5

   #@ Helper Object: density
   #@ Description: density parameter for generating random dataset
   density = 0.2

   #@ Helper Object: X
   #@ Description: data matrix X
   bs=np.random.randn(n)
   idxs = np.random.choice(range(n), int((1-density)*n), replace=False)
   X = np.random.randn(m,n)


   #@ Helper Object: Y
   #@ Description: observations Y
   beta_star = np.random.randn(n)
   idxs = np.random.choice(range(n), int((1-density)*n), replace=False)
   for idx in idxs:
       beta_star[idx] = 0
   Y = X.dot(beta_star) + np.random.normal(0, sigma, size=m)

   #@ Helper Object: X_train
   #@ Description: training data
   X_train = X[:50, :]

   #@ Helper Object: Y_train
   #@ Description: training observations
   Y_train = Y[:50]

   #@ Helper Object: X_test
   #@ Description: test data
   X_test = X[50:, :]
   
   #@ Helper Object: Y_test
   #@ Description: test observations
   Y_test = Y[50:]

   #@ Input Object: lambd
   #@ Description: $$\lambda$$: regularization parameter
   lambd = .1

   #@ Variable: beta
   #@ Description: $$\beta$$: regression coefficients
   beta = cp.Variable(n)

   #@ Function: loss_fn
   #@ Description: loss function $$\beta X_{train} - Y_{train}$$
   loss_fn = cp.norm2(X_train @ beta - Y_train)**2

   #@ Function: regularizer
   #@ Description: regularization component of objective function $$||\beta||$$
   regularizer = cp.norm1(beta)

   #@ Function: objectivefn
   #@ Description: objective function $$loss_{fn}+\lambda||\beta||$$
   objectivefn = loss_fn + lambd * regularizer

   #@ Problem: problem
   problem = cp.Problem(cp.Minimize(objectivefn))

   #@ Solver: solver
   solver = "ECOS"

   problem.solve(solver=solver, verbose=True)

