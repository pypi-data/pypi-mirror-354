import sys
import unittest
import random
from orangewidget.tests.base import WidgetTest
from Orange.data import Table
from PyQt5.QtTest import QTest
import numpy as np
import numpy.testing as npt

from orangecontrib.factoranalysis.widgets.owfactoranalysis import OWFactorAnalysis

class TestFactorAnalysisWidget(WidgetTest):
    def setUp(self):
        super().setUp()

        self.data = Table('iris')
        self.widget = self.create_widget(OWFactorAnalysis)
        # Get input signal names
        self.input_names = [signal.name for signal in self.widget.Inputs.__dict__.values() if hasattr(signal, 'name')]
        # Get output signal names
        self.output_names = [signal.name for signal in self.widget.Outputs.__dict__.values() if hasattr(signal, 'name')]

    def tearDown(self):
        self.widget.close()
        super().tearDown()

    def test_iris_nc2(self):
        self.send_signal(self.widget.Inputs.data, self.data)
        output = self.get_output(self.widget.Outputs.sample)
        while output is None:
            QTest.qWait(3000)
            output = self.get_output(self.widget.Outputs.sample, wait=3000)
        self.assertIsNotNone(output)
        expected = np.array(
            [
                [0.843, -0.464, 1.004, 0.946],
                [0.319, 0.883, 0.055, 0.091]
            ]
        )
        npt.assert_allclose(output.X, expected, rtol=1e-3, atol=1e-3)

    def test_iris_nc3(self):
        self.widget.n_components_spin.setValue(3)
        self.send_signal(self.widget.Inputs.data, self.data)
        output = self.get_output(self.widget.Outputs.sample)
        while output is None:
            QTest.qWait(3000)
            output = self.get_output(self.widget.Outputs.sample, wait=3000)
        self.assertIsNotNone(output)
        expected = np.array(
            [
                [ 0.901248, -0.376205,  0.995091,  0.967031],
                [ 0.382476,  0.657966, -0.068914, -0.029575],
                [-0.186443,  0.117847, -0.006907,  0.226714]
            ]
        )

        npt.assert_allclose(output.X, expected, rtol=1e-6, atol=1e-6)

    def test_iris_nc4(self):
        self.widget.n_components_spin.setValue(4)
        self.send_signal(self.widget.Inputs.data, self.data)
        output = self.get_output(self.widget.Outputs.sample)
        while output is None:
            QTest.qWait(3000)
            output = self.get_output(self.widget.Outputs.sample, wait=3000)
        self.assertIsNotNone(output)
        expected = np.array(
            [
                [ 0.901248, -0.376205,  0.995091,  0.967031],
                [ 0.382476,  0.657966, -0.068914, -0.029575],
                [-0.186443,  0.117847, -0.006907,  0.226714],
                [ 0.      ,  0.      ,  0.      ,  0.      ]
            ]
        )

        npt.assert_allclose(output.X, expected, rtol=1e-6, atol=1e-6)

if __name__ == "__main__":
    unittest.main()

