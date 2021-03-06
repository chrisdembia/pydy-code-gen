PyDy Code Generation
====================

This distribution provides some code generation facilities for PyDy. For now,
it generates functions that can evaluate the right hand side of the ordinary
differential equations generated with sympy.physics.mechanics with three
different backends: SymPy's lambdify_, Theano_, and Cython_.

.. _lambdify: http://docs.sympy.org/latest/modules/utilities/lambdify.html#sympy.utilities.lambdify.lambdify
.. _Theano: http://deeplearning.net/software/theano/
.. _Cython: http://cython.org/

Dependencies
============

- Python: 2.7
- setuptools
- NumPy: >=1.6.1
- SymPy: HEAD of master (>0.7.3)
- SciPy: >=0.9
- Cython: >=0.15.1
- Theano: HEAD of master (>0.6.0rc3)

Installation
============

For now, download the source and install manually. Make sure your environment
has all the dependencies met. Here is one option::

   $ git clone git@github.com:PythonDynamics/pydy-code-gen.git
   $ cd pydy-code-gen
   $ python setup.py install

Usage
=====

This is an example of a simple 1 degree of freedom system: a mass, spring,
damper system under the influence of gravity and a force::


   / / / / / / / / /
   -----------------
     |    |     |   | g
     \   | |    |   V
   k /   --- c  |
     |    |     | x, v
    --------    V
    |  m   | -----
    --------
       | F
       V

Derive the system::

   from sympy import symbols
   import sympy.physics.mechanics as me

   mass, stiffness, damping, gravity = symbols('m, k, c, g')

   position, speed = me.dynamicsymbols('x v')
   positiond = me.dynamicsymbols('x', 1)
   force = me.dynamicsymbols('F')

   ceiling = me.ReferenceFrame('N')

   origin = me.Point('origin')
   origin.set_vel(ceiling, 0)

   center = origin.locatenew('center', position * ceiling.x)
   center.set_vel(ceiling, speed * ceiling.x)

   block = me.Particle('block', center, mass)

   kinematic_equations = [speed - positiond]

   force_magnitude = mass * gravity - stiffness * position - damping * speed + force
   forces = [(center, force_magnitude * ceiling.x)]

   particles = [block]

   kane = me.KanesMethod(ceiling, q_ind=[position], u_ind=[speed],
                        kd_eqs=kinematic_equations)
   kane.kanes_equations(forces, particles)

Store the expressions and symbols in sequences for the code generation::

   mass_matrix = kane.mass_matrix_full
   forcing_vector = kane.forcing_full
   constants = (mass, stiffness, damping, gravity)
   coordinates = (position,)
   speeds = (speed,)
   specified = (force,)

Now generate the function needed for numerical evaluation of the ODEs. The
generator can use various back ends: ``lambdify``, ``theano``, or ``cython``::

   from pydy_code_gen.code import numeric_right_hand_side

   right_hand_side = numeric_right_hand_side(mass_matrix, forcing_vector,
       constants, coordinates, speeds, specified, generator='cython')

Integrate the equations of motion::

   from numpy import array, linspace
   from scipy.integrate import odeint

   x0 = array([0.1, -1.0])
   args = {'constants': array([1.0, 1.0, 0.2, 9.8]),
           'specified': array([1.0]),
           'num_coordinates': 1}
   t = linspace(0.0, 10.0, 1000)

   y = odeint(right_hand_side, x0, t, args=(args,))

Plot the results::

   import matplotlib.pyplot as plt

   plt.plot(t, y)
   plt.legend((str(position), str(speed)))
   plt.show()

Development Environment
=======================

Additional Development Dependencies
-----------------------------------

- pip
- nose: 1.3.0
- matplotlib: >0.99 (only for benchmark script)

Installation
------------

The following installation assumes you have virtualenv wrapper and all the
dependencies needed to build the packages::

   $ mkvirtualenv pydy-dev
   (pydy-dev)$ pip install numpy scipy cython nose
   (pydy-dev)$ pip install matplotlib # make sure to do this after numpy
   (pydy-dev)$ pip install git+git://github.com/Theano/Theano.git
   (pydy-dev)$ pip install git+git://github.com/sympy/sympy.git
   (pydy-dev)$ git clone git@github.com:PythonDynamics/pydy-code-gen.git
   (pydy-dev)$ cd pydy-code-gen
   (pydy-dev)$ python setup.py develop

Run the tests::

   (pydy-dev)$ nosetests

Run the benchmark to test the n-link pendulum problem.::

   (pydy-dev)$ python bin/benchmark.py <max # of links> <# of time steps>

