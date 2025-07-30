Modules
=======

The **pyVCHAM** library is modularly designed to provide comprehensive functionalities.

.. toctree::
   :maxdepth: 2
   :caption: Core Modules

   constants
   couplingfunct
   diabfunct
   lvc
   opt_diag

.. toctree::
   :maxdepth: 2
   :caption: Utility Modules

   symm_vcham
   utils

Core Modules
------------

Each core module handles essential aspects of the **pyVCHAM** tool:

- **constants**: Defines fundamental constants.
- **couplingfunct**: Manages coupling functions for the off-diagonals elements of the Hamiltonian.
- **diabfunct**: Handles diabatic functions for defining diagonal matrix elements of the Hamiltonian.
- **lvc**: Implements linear vibronic coupling model.
- **opt_diag**: Facilitates the optimization providing an initial guess.

Utility Modules
---------------

Utility modules provide supporting functionalities that enhance the core operations:

- **symm_vcham**: Provides tools for handling symmetry operations within vibronic coupling models.
- **utils**: Contains miscellaneous utility functions that aid in various computational tasks throughout the library.

