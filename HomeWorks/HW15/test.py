#!/usr/bin/env python

# Copyright 2020-2021 John T. Foster
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import nbconvert
import numpy as np


with open("assignment15.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)

with open("assignment15.py", "w") as f:
    f.write(python_file)

from assignment15 import IterativeSolver


class TestSolution(unittest.TestCase):

    def test_solver(self):
        A = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
        b = np.array([1, 2, 3])
        solver = IterativeSolver(A, b)
        np.testing.assert_array_almost_equal(solver.gauss_seidel_solve(), np.array([2.5, 4., 3.5]), decimal=6)

    def test_solver_private(self):
        A = np.array([[0, -1, 0], [-1, 2, -1], [0, -1, 2]])
        b = np.array([1, 2, 3])
        solver = IterativeSolver(A, b)
        np.testing.assert_array_almost_equal(solver.gauss_seidel_solve(), np.array([-5, -1., 1.]), decimal=6)
#        
if __name__ == '__main__':
    unittest.main()
