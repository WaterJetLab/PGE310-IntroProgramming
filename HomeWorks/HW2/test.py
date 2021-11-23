#!/usr/bin/env python

# Copyright 2020-1 John T. Foster
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

with open("assignment2.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment2.py", "w") as f:
    f.write(python_file)


from assignment2 import *


class TestSolution(unittest.TestCase):
 

    def test_quadratic_equation_1(self):
        
        ans1, ans2 = quadratic_equation(1, 6, 3)

        self.assertAlmostEqual(ans1, -0.5505102572168221, places=6)
        self.assertAlmostEqual(ans2, -5.449489742783178, places=6)
        
    def test_quadratic_equation_2(self):
        
        ans1, ans2 = quadratic_equation(8, 22, 1)

        self.assertAlmostEqual(ans1, -0.04623177340816875, places=6)
        self.assertAlmostEqual(ans2, -2.7037682265918312, places=6)
        
    def test_quadratic_equation_private(self):
        
        ans1, ans2 = quadratic_equation(3, 4, 1)

        self.assertAlmostEqual(ans1, -0.3333333333333333, places=6)
        self.assertAlmostEqual(ans2, -1.0, places=1)
        
    def test_hello_world_with_name(self):
        
        ans1 = hello_world_with_name("Romeo")
        ans2 = hello_world_with_name("Juliet")
        
        self.assertEqual(ans1, "Hello, World! My name is Romeo!")
        self.assertEqual(ans2, "Hello, World! My name is Juliet!")
        
        
    def test_hello_world_with_name_private(self):
        
        ans1 = hello_world_with_name("Jack")
        ans2 = hello_world_with_name("Kate")
        
        self.assertEqual(ans1, "Hello, World! My name is Jack!")
        self.assertEqual(ans2, "Hello, World! My name is Kate!")


if __name__ == "__main__":
    unittest.main()
