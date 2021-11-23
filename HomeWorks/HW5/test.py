#!/usr/bin/env python

# Copyright 2020 John T. Foster
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
import os

import numpy as np

with open("assignment5.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment5.py", "w") as f:
    f.write(python_file)


from assignment5 import *

sum = None

class TestSolution(unittest.TestCase):
    
    def test_list_sum_1(self):
        
        ans = list_sum([1, 3, 5, 8])

        self.assertAlmostEqual(ans, 17, places=4)
        
        
    def test_list_sum_2(self):
        
        ans = list_sum([1, 6, 5, 18])

        self.assertAlmostEqual(ans, 30, places=4)
        
    def test_list_sum_private(self):
        
        ans = list_sum([1, 22, 99, 5, 18])

        self.assertAlmostEqual(ans, 145, places=4)
        
 
    def test_cumulative_sum_1(self):
        
        ans = cumulative_sum([1, 3, 5, 8])

        np.testing.assert_almost_equal(ans, [1, 4, 9, 17], decimal=4) 
        
    def test_cumulative_sum_2(self):
        
        ans = cumulative_sum([1, 6, 5, 18])

        np.testing.assert_almost_equal(ans, [1, 7, 12, 30], decimal=4)
        
    def test_cumulative_sum_private(self):
        
        ans = cumulative_sum([1, 22, 99, 5, 18])

        np.testing.assert_almost_equal(ans, [1, 23, 122, 127, 145], decimal=4)
        
        



if __name__ == "__main__":
    unittest.main()
