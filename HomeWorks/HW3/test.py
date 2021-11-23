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

with open("assignment3.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment3.py", "w") as f:
    f.write(python_file)


from assignment3 import *


class TestSolution(unittest.TestCase):
 

    def test_is_evenly_divisible_1(self):
        
        ans = is_evenly_divisible(4, 2)

        self.assertEqual(ans, "4 is evenly divisible by 2!")
        
    def test_is_evenly_divisible_2(self):
        
        ans = is_evenly_divisible(5, 3)

        self.assertEqual(ans, "5 is not evenly divisible by 3. The remainder is 2.")
        
    def test_math_operation_1(self):
        
        ans = math_operation(4, 5, 'add')
        
        self.assertAlmostEqual(ans, 9, places=6)
        
    def test_math_operation_2(self):
        
        ans = math_operation(5, 4, 'subtract')
        
        self.assertAlmostEqual(ans, 1, places=6)
        
    def test_math_operation_3(self):
        
        ans = math_operation(5, 4, 'multiply')
        
        self.assertAlmostEqual(ans, 20, places=6)
        
    def test_math_operation_4(self):
        
        ans = math_operation(20, 4, 'divide')
        
        self.assertAlmostEqual(ans, 5, places=6)
        
    def test_math_operation_5(self):
        
        ans = math_operation(20, 4, 'plus')
        
        self.assertEqual(ans, 'Operation must be one of: ["add", "subtract", "multiply", "divide"]')
        



if __name__ == "__main__":
    unittest.main()
