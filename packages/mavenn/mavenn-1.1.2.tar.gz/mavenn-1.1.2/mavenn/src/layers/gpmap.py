"""gpmap.py: Defines layers representing G-P maps."""
# Standard imports
import numpy as np
from collections.abc import Iterable
import re

# Tensorflow imports
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.initializers import Constant
from tensorflow.keras.layers import Layer, Dense

# This is the kind of variable to test for
from keras.src.backend import Variable

# MAVE-NN imports
from mavenn.src.error_handling import check, handle_errors
from mavenn.src.validate import validate_alphabet

class GPMapLayer(Layer):
    """
    Represents a general genotype-phenotype map.

    Specific functional forms for G-P maps should be
    represented by derived classes of this layer.
    """

    @handle_errors
    def __init__(self,
                 L,
                 alphabet,
                 theta_regularization):
        """Construct layer instance."""
        # Set sequence length
        self.L = L
        self.alphabet = validate_alphabet(alphabet)
        # Set alphabet length
        self.C = len(alphabet)

        # Set regularization contribution
        self.theta_regularization = theta_regularization

        # Set regularizer
        self.regularizer = tf.keras.regularizers.L2(self.theta_regularization)

        # Initialize mask dict
        self.mask_dict = {}

        # Define regular expression for theta parameters
        self.theta_pattern = re.compile('^theta.*')

        # Call superclass constructor
        super().__init__()

    @handle_errors
    def get_config(self):
        """Return configuration dictionary."""
        base_config = super(Layer, self).get_config()
        return {'L': self.L,
                'C': self.C,
                'theta_regularization': self.theta_regularization,
                **base_config}

    @handle_errors
    def set_params(self, **kwargs):
        """Set values of layer parameters."""

        # Iterate over kwargs
        for k, v in kwargs.items():

            # Get current parameter object
            check(k in self.__dict__,
                  f'Keyword argument "{k}" is not the name of a parameter')
            check(bool(self.theta_pattern.match(k)),
                  f'Keyword argument "{k}" does not match a theta parameter')
            self_param = self.__dict__[k]

            # Type and shape v as needed
            v = np.array(v).astype(np.float32).reshape(self_param.shape)

            # Mask meaningless values with zeros
            no_mask = np.full(v.shape, True, dtype=bool)
            mask = self.mask_dict.get(k, no_mask)
            v[~mask] = 0.0

            # Assign to self_param values
            self_param.assign(v)

    @handle_errors
    def get_params(self,
                   squeeze=True,
                   pop=True,
                   mask_with_nans=True):

        # Get theta_dict
        theta_dict = {k: v for (k, v) in self.__dict__.items()
                      if self.theta_pattern.match(k)
                      and isinstance(v, Variable)}  
        # 25.01.21 Changed from tf.Variable to Variable
        # to fix breaking problem with get_params

        # Modify dict values as requested
        for k, v in theta_dict.items():

            # Convert to numpy array
            v = v.numpy()

            # Mask meaningless values with nans
            if mask_with_nans:
                no_mask = np.full(v.shape, True, dtype=bool)
                mask = self.mask_dict.get(k, no_mask)
                v[~mask] = np.nan

            # Squeeze out singleton dimensions
            # Pop out values form singleton arrays
            if squeeze:
                v = v.squeeze()

            if pop and v.size == 1:
                v = v.item()

            # Save modified value
            theta_dict[k] = v

        return theta_dict

    ### The following methods must be fully overridden ###

    @handle_errors
    def build(self, input_shape):
        # Call superclass build
        super().build(input_shape)

    @handle_errors
    def call(self, inputs):
        """Process layer input and return output."""
        assert False


class AdditiveGPMapLayer(GPMapLayer):
    """Represents an additive G-P map."""

    @handle_errors
    def __init__(self, *args, **kwargs):
        """Construct layer instance."""

        # Call superclass constructor
        super().__init__(*args, **kwargs)

        """Build layer."""
        # Define theta_0
        self.theta_0 = self.add_weight(name='theta_0',
                                       shape=(1,),
                                       initializer=Constant(0.),
                                       trainable=True,
                                       regularizer=self.regularizer)

        # Define theta_lc parameters
        theta_lc_shape = (1, self.L, self.C)
        theta_lc_init = np.random.randn(*theta_lc_shape)/np.sqrt(self.L)
        self.theta_lc = self.add_weight(name='theta_lc',
                                        shape=theta_lc_shape,
                                        initializer=Constant(theta_lc_init),
                                        trainable=True,
                                        regularizer=self.regularizer)

    def call(self, x_lc):
        """Process layer input and return output."""
        # Shape input
        x_lc = tf.reshape(x_lc, [-1, self.L, self.C])

        phi = self.theta_0 + \
              tf.reshape(K.sum(self.theta_lc * x_lc, axis=[1, 2]),
                         shape=[-1, 1])

        return phi


class PairwiseGPMapLayer(GPMapLayer):
    """Represents a pairwise G-P map."""

    @handle_errors
    def __init__(self, mask_type, *args, **kwargs):
        """Construct layer instance."""

        # Call superclass constructor
        super().__init__(*args, **kwargs)

        # Define theta_0
        self.theta_0 = self.add_weight(name='theta_0',
                                       shape=(1,),
                                       initializer=Constant(0.),
                                       trainable=True,
                                       regularizer=self.regularizer)

        # Define theta_lc parameters
        theta_lc_shape = (1, self.L, self.C)
        theta_lc_init = np.random.randn(*theta_lc_shape)/np.sqrt(self.L)
        self.theta_lc = self.add_weight(name='theta_lc',
                                        shape=theta_lc_shape,
                                        initializer=Constant(theta_lc_init),
                                        trainable=True,
                                        regularizer=self.regularizer)

        # Set mask type
        self.mask_type = mask_type
        check(self.mask_type in ['neighbor', 'pairwise'],
              f'self.mask_type={repr(self.mask_type)}; must be'
              f'one of ["neighbor","pairwise"]')

        # Create mask for theta_lclc
        ls = np.arange(self.L).astype(int)
        ls1 = np.tile(ls.reshape([1, self.L, 1, 1, 1]),
                      [1, 1, self.C, self.L, self.C])
        ls2 = np.tile(ls.reshape([1, 1, 1, self.L, 1]),
                      [1, self.L, self.C, 1, self.C])
        if self.mask_type == 'pairwise':
            mask = (ls2 - ls1 >= 1)
        elif self.mask_type == 'neighbor':
            mask = (ls2 - ls1 == 1)
        else:
            assert False, "This should not happen."
        self.mask_dict['theta_lclc'] = mask

        # Define theta_lclc parameters
        theta_lclc_shape = (1, self.L, self.C, self.L, self.C)
        theta_lclc_init = np.random.randn(*theta_lclc_shape)/np.sqrt(self.L**2)
        theta_lclc_init *= self.mask_dict['theta_lclc']
        self.theta_lclc = self.add_weight(name='theta_lclc',
                                          shape=theta_lclc_shape,
                                          initializer=Constant(theta_lclc_init),
                                          trainable=True,
                                          regularizer=self.regularizer)

    def call(self, x_lc):
        """Process layer input and return output."""

        # Compute phi
        phi = self.theta_0
        phi = phi + tf.reshape(K.sum(self.theta_lc *
                                     tf.reshape(x_lc, [-1, self.L, self.C]),
                                     axis=[1, 2]),
                               shape=[-1, 1])
        phi = phi + tf.reshape(K.sum(self.theta_lclc *
                                     self.mask_dict['theta_lclc'] *
                                     tf.reshape(x_lc,
                                         [-1, self.L, self.C, 1, 1]) *
                                     tf.reshape(x_lc,
                                         [-1, 1, 1, self.L, self.C]),
                                     axis=[1, 2, 3, 4]),
                               shape=[-1, 1])

        return phi

    @handle_errors
    def get_config(self):
        """Return configuration dictionary."""

        # Get base config of superclass
        base_config = super().get_config()

        # Add new param from __init__() to dict and return
        return {'mask_type': self.mask_type,
                **base_config}


class MultilayerPerceptronGPMap(GPMapLayer):
    """Represents an MLP G-P map."""

    @handle_errors
    def __init__(self,
                 *args,
                 hidden_layer_sizes=(10, 10, 10),
                 hidden_layer_activation='relu',
                 features='additive',
                 **kwargs):

        # Check and set hidden layer sizes
        check(isinstance(hidden_layer_sizes, Iterable),
              f'type(hidden_layer_sizes)={type(hidden_layer_sizes)}; '
              f'must be Iterable.')
        check(all([x >= 1 for x in hidden_layer_sizes]),
              f'all elements of hidden_layer_sizes={hidden_layer_sizes}'
              f'must be >= 1')
        check(all([isinstance(x, int) for x in hidden_layer_sizes]),
              f'all elements of hidden_layer_sizes={hidden_layer_sizes}'
              f'must be int.')
        self.hidden_layer_sizes = hidden_layer_sizes

        # Check and set features
        allowed_features = ['additive','neighbor','pairwise']
        check(features in allowed_features,
              f'features={repr(features)}; must be one of {allowed_features}.')
        self.features = features

        # Initialize array to hold layers
        self.layers = []

        # Set activation
        self.hidden_layer_activation = hidden_layer_activation
        super().__init__(*args, **kwargs)

    @handle_errors
    def build(self, input_shape):

        # Determine input shape
        L = self.L
        C = self.C
        if self.features == 'additive':
            self.num_features = L*C
        elif self.features == 'neighbor':
            self.num_features = L*C + (L-1)*(C**2)
        elif self.features == 'pairwise':
            self.num_features = L*C + L*(L-1)*(C**2)/2
        self.x_shape = (input_shape[0], int(self.num_features))

        # Create mask
        ls = np.arange(self.L).astype(int)
        ls1 = np.tile(ls.reshape([L, 1, 1, 1]),
                                 [1, C, L, C])
        ls2 = np.tile(ls.reshape([1, 1, L, 1]),
                                 [L, C, 1, C])
        if self.features in ['neighbor', 'pairwise']:
            if self.features == 'pairwise':
                mask_lclc = (ls2 - ls1 >= 1)
            else:
                mask_lclc = (ls2 - ls1 == 1)
            mask_vec = np.reshape(mask_lclc, L*C*L*C)
            self.mask_ints = np.arange(L*C*L*C, dtype=int)[mask_vec]
        elif self.features == 'additive':
            self.mask_ints = None
        else:
            assert False, "This should not work"

        # Make sure self.layers is empty
        self.layers = []

        if len(self.hidden_layer_sizes) >= 1:
            # Add hidden layer #1
            size = self.hidden_layer_sizes[0]
            self.layers.append(
                Dense(units=size,
                      activation=self.hidden_layer_activation,
                      kernel_regularizer=self.regularizer,
                      bias_regularizer=self.regularizer)
            )

            # Add rest of hidden layers
            for size in self.hidden_layer_sizes[1:]:
                self.layers.append(
                    Dense(units=size,
                          activation=self.hidden_layer_activation,
                          kernel_regularizer=self.regularizer,
                          bias_regularizer=self.regularizer)
                )

            # Add output layer
            self.layers.append(
                Dense(units=1,
                      activation='linear',
                      kernel_regularizer=self.regularizer,
                      bias_regularizer=self.regularizer)
            )
        elif len(self.hidden_layer_sizes) == 0:
            # Add single layer; no hidden nodes
            self.layers.append(
                Dense(units=1,
                      activation='linear',
                      kernel_regularizer=self.regularizer,
                      bias_regularizer=self.regularizer)
            )
        else:
            assert False, 'This should not happen.'

        # Build superclass
        super().build(input_shape)

        # Build all layers with the correct input shape
        x = tf.keras.Input(shape=self.x_shape[1:])
        for layer in self.layers:
            x = layer(x)

    def call(self, x_add):
        """Process layer input and return output."""

        # Create input features
        if self.features == 'additive':
            tensor = x_add
        elif self.features in ['neighbor', 'pairwise']:
            L = self.L
            C = self.C
            x___lc = tf.reshape(x_add, [-1, 1, 1, L, C])
            x_lc__ = tf.reshape(x_add, [-1, L, C, 1, 1])
            x_lclc = x___lc * x_lc__
            x_pair = tf.reshape(x_lclc, [-1, L*C*L*C])

            # Only use relevant columns
            x_2pt = tf.gather(x_pair, self.mask_ints, axis=1)

            # Make input tensor
            tensor = tf.concat([x_add, x_2pt], axis=1)

        # Run tensor through layers
        for layer in self.layers:
            tensor = layer(tensor)
        phi = tensor

        return phi

    @handle_errors
    def set_params(self, theta_0=None, theta_lc=None):
        """
        Does nothing for MultilayerPerceptronGPMap
        """
        print('Warning: MultilayerPerceptronGPMap.set_params() does nothing.')

    @handle_errors
    def get_params(self):
        """
        Get values of layer parameters.

        Parameters
        ----------
        None.

        Returns
        -------
        param_dict: (dict)
            Dictionary containing model parameters.
        """

        #  Fill param_dict
        param_dict = {}
        param_dict['theta_mlp'] = [layer.get_weights() for layer in self.layers]

        return param_dict
