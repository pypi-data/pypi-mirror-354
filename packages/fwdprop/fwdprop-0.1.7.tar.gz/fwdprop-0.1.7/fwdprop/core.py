import numpy as np
from .activations import sigmoid, relu, identity


# Layer class: Handles weights, bias, and activation for a single layer
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


# NeuralNetwork class: Can handle either single-layer or multi-layer network
class NeuralNetwork:
    def __init__(self, layers_config=None, weights=None, bias=None, activation=None):
        self.layers = []

        if layers_config is not None:
            # Multi-layer config
            for config in layers_config:
                self.layers.append(
                    Layer(
                        weights=config["weights"],
                        bias=config["bias"],
                        activation=config.get("activation", "sigmoid")
                    )
                )
        elif weights is not None and bias is not None:
            # Single-layer config
            self.layers.append(
                Layer(
                    weights=weights,
                    bias=bias,
                    activation=activation or "sigmoid"
                )
            )
        else:
            raise ValueError("Invalid NeuralNetwork init args. Provide either `layers_config` or (`weights`, `bias`).")

    def forward(self, inputs):
        a = np.array(inputs)
        for layer in self.layers:
            a = layer.forward(a)
        return a
