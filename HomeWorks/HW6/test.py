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

with open("assignment6.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment6.py", "w") as f:
    f.write(python_file)


from assignment6 import *


class TestSolution(unittest.TestCase):
    
    def test_multiply_1(self):
        
        ans = multiply(x=22, y=4, z=32)

        self.assertEqual(ans, 'x * y * z = 2816')
        
    def test_multiply_2(self):
        
        ans = multiply(a=2, b=4, c=3)

        self.assertEqual(ans, 'a * b * c = 24')
        
    def test_multiply_private(self):
        
        ans = multiply(romeo=21, juliet=24)

        self.assertEqual(ans, 'romeo * juliet = 504')
        
    def test_create_lambda(self):
        
        ans = create_lambda()

        self.assertAlmostEqual(ans(1,2), 5, places=4)
        self.assertAlmostEqual(ans(2,3), 11, places=4)


if __name__ == "__main__":
    unittest.main()
