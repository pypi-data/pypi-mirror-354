"""
This module contains the diabatic functions.

Functions
---------
- :func:`harmonic_oscillator`: Computes the harmonic oscillator potential.
- :func:`general_quartic_potential`: Computes the general quartic potential.
- :func:`general_morse_tf`: Computes the general Morse potential.

Variables
---------
- ``potential_functions``: Dictionary of potential functions.
- ``n_var``: Dictionary of the number of variables for each function.
- ``initial_guesses``: Dictionary of initial guesses for each potential type.
- ``kappa_compatible``: Dictionary indicating compatibility with the kappa function.
"""

import numpy as np
import tensorflow as tf

@tf.function
def harmonic_oscillator(q: tf.Tensor, omega: tf.Tensor, params: list) -> tf.Tensor:
    """
    Compute the harmonic oscillator potential.

    Parameters
    ----------
    q : tf.Tensor
        Tensor of displacements.
    omega : tf.Tensor
        Tensor representing the frequency of the mode.
    params : list
        List containing additional parameters. The first element is used as a force
        constant (k1) in this potential.

    Returns
    -------
    tf.Tensor
        Tensor of potential values.
    """
    k1 = params[0]
    q = tf.cast(q, tf.float32)
    omega = tf.cast(omega, tf.float32)
    k1 = tf.cast(k1, tf.float32)
    HALF = tf.constant(0.5, dtype=tf.float32)
    return HALF * omega * tf.math.square(q) + HALF * k1 * tf.math.square(q)

@tf.function
def general_quartic_potential(q: tf.Tensor, omega: tf.Tensor, params: list) -> tf.Tensor:
    """
    Compute the general quartic potential.

    Parameters
    ----------
    q : tf.Tensor
        Tensor of displacements.
    omega : tf.Tensor
        Tensor representing the frequency of the mode.
    params : list
        List containing the quadratic coefficient (k2) and quartic coefficient (k3).

    Returns
    -------
    tf.Tensor
        Tensor of potential values.
    """
    k2, k3 = params[0], params[1]
    q = tf.cast(q, tf.float32)
    omega = tf.cast(omega, tf.float32)
    k2 = tf.cast(k2, tf.float32)
    k3 = tf.cast(k3, tf.float32)
    HALF = tf.constant(0.5, dtype=tf.float32)
    ONE_OVER_24 = tf.constant(1.0 / 24.0, dtype=tf.float32)
    return (
        HALF * omega * tf.math.square(q)
        + HALF * k2 * tf.math.square(q)
        + ONE_OVER_24 * k3 * tf.math.pow(q, 4)
    )

@tf.function
def general_morse(q: tf.Tensor, params: list) -> tf.Tensor:
    """
    Compute the general Morse potential using TensorFlow.

    Parameters
    ----------
    q : tf.Tensor
        Tensor of displacements.
    params : list
        List containing additional parameters. Dissociation energy (De), 
        range parameter (alpha), and equilibrium bond distance (q0).

    Returns
    -------
    tf.Tensor
        Tensor of potential values.
    """
    De, alpha, q0 = params[0], params[1], params[2]
    q = tf.cast(q, tf.float32)
    De = tf.cast(De, tf.float32)
    alpha = tf.cast(alpha, tf.float32)
    q0 = tf.cast(q0, tf.float32)
    ONE = tf.constant(1.0, dtype=tf.float32)

    # Compute the vertical offset at q=0
    offset = De * tf.math.square(tf.exp(alpha * q0) - ONE)

    morse = De * tf.math.square(tf.exp(-alpha * (q - q0)) - ONE)
    return morse - offset

@tf.function
def general_morse_gs(q: tf.Tensor, params: list) -> tf.Tensor:
    """
    Compute the general Morse potential using TensorFlow.

    Parameters
    ----------
    q : tf.Tensor
        Tensor of displacements.
    params : list
        List containing additional parameters. Dissociation energy (De), 
        range parameter (alpha), and equilibrium bond distance (q0).

    Returns
    -------
    tf.Tensor
        Tensor of potential values.
    """
    De, alpha, q0 = params[0], params[1], params[2]
    q = tf.cast(q, tf.float32)
    De = tf.cast(De, tf.float32)
    alpha = tf.cast(alpha, tf.float32)
    q0 = tf.cast(0.0, tf.float32)
    ONE = tf.constant(1.0, dtype=tf.float32)

    # Compute the vertical offset at q=0
    offset = De * tf.math.square(tf.exp(alpha * q0) - ONE)

    morse = De * tf.math.square(tf.exp(-alpha * (q - q0)) - ONE)
    return morse - offset


# Potential Functions Dictionary
potential_functions = {
    "ho": harmonic_oscillator,
    "morse": general_morse,
    "antimorse": general_morse,
    "quartic": general_quartic_potential,
}

# Number of Variables for Each Function
n_var = {
    "ho": 1,
    "morse": 3,
    "antimorse": 3,
    "quartic": 2,
}

# Initial Guesses for Each Potential Type
initial_guesses = {
    "ho": np.array([0.5]),
    "morse": np.array([5.0, 0.5, 0.0]),
    "antimorse": np.array([5.0, -0.5, 0.0]),
    "quartic": np.array([0.0, 0.0005]),
}

# Kappa Compatibility (those functions that could be used together with kappa)
kappa_compatible = {
    "ho": True,
    "morse": False,      # Morse potential has in its definition q - q0
    "antimorse": False,  # Morse potential has in its definition q - q0
    "quartic": True,
}