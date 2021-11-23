#!/usr/bin/env python

import unittest

from unittest.mock import MagicMock

import nbconvert

import numpy as np


with open("assignment14.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)

with open("assignment14.py", "w") as f:
    f.write(python_file)

from assignment14 import LU


class TestSolution(unittest.TestCase):

    def test_lu(self):
        A = np.array([[0, 3, 4], [4, 6, 10], [22, 1, 7]])
        lu = LU(A)
        np.testing.assert_array_almost_equal(lu.P(), np.array([[0., 1., 0.], [1., 0., 0.], [0., 0., 1.]]), decimal=6)
        np.testing.assert_array_almost_equal(lu.L(), np.array([[1.,0.,0.],[0.,1.,0.],[5.5,-10.66666667,1.]]), decimal=6)
        np.testing.assert_array_almost_equal(lu.U(), np.array([[4.,6.,10.],[0.,3.,4.],[0.,0., -5.33333333]]), decimal=6)

    def test_lu_private(self):
        
        A = np.array([[1, 3, 4], [4, 6, 10], [12, 1, 7]])       
        lu = LU(A)
        np.testing.assert_array_almost_equal(lu.P(), np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]), decimal=6)
        np.testing.assert_array_almost_equal(lu.L(), np.array([[1.,0.,0.],[4.,1.,0.],[12.,5.83333333,1.]]), decimal=6)
        np.testing.assert_array_almost_equal(lu.U(), np.array([[1.,3.,4.],[0.,-6.,-6.], [0.,0.,-6.]]), decimal=6)

    def test_inverse(self):
        
        A = np.array([[0, 3, 4], [4, 6, 10], [22, 1, 7]])       
        lu = LU(A)
        Ainv = lu.inverse()
        np.testing.assert_array_almost_equal(Ainv, np.linalg.inv(A), decimal=6)

    def test_inverse_private(self):
        
        A = np.array([[1, 3, 4], [4, 6, 10], [12, 1, 7]])       
        lu = LU(A)
        Ainv = lu.inverse()
        np.testing.assert_array_almost_equal(Ainv, np.linalg.inv(A), decimal=6)

    def test_det(self):
        
        A = np.array([[0, 3, 4], [4, 6, 10], [22, 1, 7]])       
        lu = LU(A)
        detA = lu.det()
        np.testing.assert_array_almost_equal(detA, np.linalg.det(A), decimal=6)

    def test_det_private(self):
        
        A = np.array([[1, 3, 4], [4, 6, 10], [12, 1, 7]])       
        lu = LU(A)
        detA = lu.det()
        np.testing.assert_array_almost_equal(detA, np.linalg.det(A), decimal=6)
#        
if __name__ == '__main__':
    unittest.main()
