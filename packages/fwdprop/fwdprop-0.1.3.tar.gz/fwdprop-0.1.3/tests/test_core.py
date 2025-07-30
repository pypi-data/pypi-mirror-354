import unittest
from fwdprop import ForwardPropagator

class TestForwardProp(unittest.TestCase):
    def test_sigmoid_output(self):
        fp = ForwardPropagator(weights=[0.5, 0.3, -0.2], bias=0.1)
        result = fp.propagate([1, 2, 3])
        self.assertTrue(0 <= result <= 1)

    def test_relu_output(self):
        fp = ForwardPropagator(weights=[1, 1, 1], bias=-100, activation='relu')
        result = fp.propagate([1, 1, 1])
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
