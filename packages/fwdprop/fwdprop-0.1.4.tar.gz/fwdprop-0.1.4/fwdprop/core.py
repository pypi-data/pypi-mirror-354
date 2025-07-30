import numpy as np
from .activations import sigmoid, relu, identity

class ForwardPropagator:
    def __init__(self, weights, bias, activation='sigmoid'):
        self.weights = np.array(weights)
        self.bias = bias

        if activation == 'sigmoid':
            self.activation_fn = sigmoid
        elif activation == 'relu':
            self.activation_fn = relu
        elif activation == 'identity':
            self.activation_fn = identity
        else:
            raise ValueError("Unsupported activation")

    def propagate(self, inputs):
        inputs = np.array(inputs)
        z = np.dot(self.weights, inputs) + self.bias
        a = self.activation_fn(z)
        return a

class NeuralNetwork:
    def __init__(self, weights, bias, activation='sigmoid'):
        self.propagator = ForwardPropagator(weights, bias, activation)

    def forward(self, inputs):
        return self.propagator.propagate(inputs)
