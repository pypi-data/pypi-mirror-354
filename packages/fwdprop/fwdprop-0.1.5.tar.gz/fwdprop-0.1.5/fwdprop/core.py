import numpy as np
from .activations import sigmoid, relu, identity

class Layer:
    def __init__(self, weights, bias, activation='sigmoid'):
        self.weights = np.array(weights)
        self.bias = np.array(bias)
        if activation == 'sigmoid':
            self.activation_fn = sigmoid
        elif activation == 'relu':
            self.activation_fn = relu
        elif activation == 'identity':
            self.activation_fn = identity
        else:
            raise ValueError(f"Unsupported activation: {activation}")

    def forward(self, inputs):
        z = np.dot(self.weights, inputs) + self.bias
        return self.activation_fn(z)

class NeuralNetwork:
    def __init__(self, layers_config=None, weights=None, bias=None, activation=None):
        self.layers = []

        # Case 1: layers_config format
        if layers_config is not None:
            for config in layers_config:
                layer = Layer(
                    weights=config["weights"],
                    bias=config["bias"],
                    activation=config.get("activation", "sigmoid")
                )
                self.layers.append(layer)

        # Case 2: single-layer shortcut
        elif weights is not None and bias is not None:
            layer = Layer(
                weights=weights,
                bias=bias,
                activation=activation or "sigmoid"
            )
            self.layers.append(layer)
        else:
            raise ValueError("Invalid NeuralNetwork init args: Provide either `layers_config` or `weights`, `bias`.")

    def forward(self, inputs):
        a = np.array(inputs)
        for layer in self.layers:
            a = layer.forward(a)
        return a
