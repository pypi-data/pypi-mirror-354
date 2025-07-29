"""
Coupling Calculations Module
----------------------------

This module contains the coupling functions used in the vibronic coupling Hamiltonian.

Functions
---------
- :func:`linear_coupling`: Computes the linear coupling.

Variables
---------
- ``coupling_funct``: Dictionary of coupling functions.
- ``n_var``: Dictionary of the number of variables for each function.
- ``initial_guesses``: Dictionary of initial guesses for each potential type.
"""

import numpy as np
import tensorflow as tf

# Constants
INITIAL_GUESS = 1e-3  # Default initial guess for coupling constants


@tf.function
def linear_coupling(q: tf.Tensor, k1: tf.Tensor) -> tf.Tensor:
    """
    Compute the linear coupling function.

    Parameters
    ----------
    q : tf.Tensor
        Tensor of displacements with dtype tf.float32.
    k1 : tf.Tensor or float
        Tensor representing the coupling constant with dtype tf.float32.

    Returns
    -------
    tf.Tensor
        Tensor of linear coupling values with dtype tf.float32.
    """
    # Ensure inputs are float32
    q = tf.cast(q, tf.float32)
    k1 = tf.cast(k1, tf.float32)
    
    return tf.multiply(q, k1)


# List of types of coupling functions
COUPLING_TYPES = ["linear"]

# Coupling functions dictionary for use in other modules
coupling_funct = {
    "linear": linear_coupling
}

# Number of variables for each function
n_var = {
    "linear": 1
}

# Initial guesses for each potential type
initial_guesses = {
    "linear": INITIAL_GUESS
}