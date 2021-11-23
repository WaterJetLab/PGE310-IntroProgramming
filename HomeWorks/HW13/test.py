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

from unittest.mock import MagicMock

import nbconvert

import numpy as np



with open("assignment13.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)

with open("assignment13.py", "w") as f:
    f.write(python_file)

from assignment13 import LinearSystem

try:
    from assignment12 import Matrix
except:
    pass

try:
    from assignment13 import Matrix
except:
    pass

class TestSolution(unittest.TestCase):
    
    def test_is_derived_from_Matrix(self):
        
        self.assertTrue(issubclass(LinearSystem, Matrix))
        
    def test_row_swap_called(self):
        
        A = np.array([[1, 2], [4, 3]])
        ls = LinearSystem(A)
        ls.row_swap = MagicMock()
        ls.row_echelon()
        assert ls.row_swap.called
        
    def test_row_combine_called(self):
        
        A = np.array([[1, 2], [4, 3]])
        ls = LinearSystem(A)
        ls.row_combine = MagicMock()
        ls.row_echelon()
        assert ls.row_combine.called
        
    def test_row_echelon(self):
        
        A = np.array([[1, 3, 4],[5, 4, 2],[1, 7, 9]])
        ls = LinearSystem(A)
        ls.row_echelon() 
        np.testing.assert_array_almost_equal(ls.mat, 
                                             np.array([[ 5., 4., 2.],
                                                       [0., 6.2, 8.6],
                                                       [ 0., 0., 0.5483871]]),                                                      decimal=6)
        
    def test_back_substitute(self):
        
        A = np.array([[1, 3, 5],[5, 2, 2],[1, 7, 1]])
        b = np.array([1, 3, 4])
        ls = LinearSystem(A, b)
        ls.row_echelon()
        np.testing.assert_array_almost_equal(ls.back_substitute(),
                                             np.linalg.solve(A, b),
                                             decimal=6)
        
    def test_gauss_solve(self):
        
        A = np.array([[1, 3, 5],[5, 2, 2],[1, 7, 1]])
        b = np.array([1, 3, 4])
        ls = LinearSystem(A, b)
        np.testing.assert_array_almost_equal(ls.gauss_solve(),
                                             np.linalg.solve(A, b),
                                             decimal=6)
        
    def test_reduced_row_echelon(self):
        
        A = np.array([[1, 3, 5],[5, 2, 2],[1, 7, 1]])
        b = np.array([1, 3, 4])
        ls = LinearSystem(A, b)
        ls.reduced_row_echelon()
        np.testing.assert_array_almost_equal(ls.mat[:,-1],
                                             np.linalg.solve(A, b),
                                             decimal=6)
        
    def test_inverse(self):
        
        A = np.array([[1, 2, 5],[5, 22, 17],[11, 7, 1]])
        ls = LinearSystem(A)
        np.testing.assert_array_almost_equal(ls.inverse(),
                                             np.linalg.inv(A),
                                             decimal=6)
        
    def test_row_echelon_private(self):
        
        A = np.array([[1, 3, 5],[5, 2, 2],[1, 7, 1]])
        ls = LinearSystem(A)
        ls.row_echelon() 
        np.testing.assert_array_almost_equal(ls.mat, 
                                             np.array([[5., 2., 2.],
                                                       [0., 6.6, 0.6],
                                                       [0., 0., 4.36363636]]),                                                      decimal=6)
        
    def test_back_substitute_private(self):
        
        A = np.array([[1, 2, 5],[5, 2, 17],[1, 7, 1]])
        b = np.array([1, 3, 12])
        ls = LinearSystem(A, b)
        ls.row_echelon()
        np.testing.assert_array_almost_equal(ls.back_substitute(),
                                             np.linalg.solve(A, b),
                                             decimal=6)
        
    def test_gauss_solve_private(self):
        
        A = np.array([[1, 2, 5],[5, 2, 17],[1, 7, 1]])
        b = np.array([1, 3, 12])
        ls = LinearSystem(A, b)
        np.testing.assert_array_almost_equal(ls.gauss_solve(),
                                             np.linalg.solve(A, b),
                                             decimal=6)
        
    def test_reduced_row_echelon_private(self):
        
        A = np.array([[1, 2, 5],[5, 2, 17],[1, 7, 1]])
        b = np.array([1, 3, 12])
        ls = LinearSystem(A, b)
        ls.reduced_row_echelon()
        np.testing.assert_array_almost_equal(ls.mat[:,-1],
                                             np.linalg.solve(A, b),
                                             decimal=6)
        
    def test_inverse_private(self):
        
        A = np.array([[11, 2, 5],[51, 22, 17],[11, 7, 1]])
        ls = LinearSystem(A)
        np.testing.assert_array_almost_equal(ls.inverse(),
                                             np.linalg.inv(A),
                                             decimal=6)


if __name__ == '__main__':
    unittest.main()
