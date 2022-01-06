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
import unittest.mock
import nbconvert
import os
import io

with open("assignment7.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment7.py", "w") as f:
    f.write(python_file)


import assignment7
from assignment7 import *

def get_class_that_defined_method(method):
    method_name = method.__name__
    if method.__self__:    
        classes = [method.__self__.__class__]
    else:
        #unbound method
        classes = [method.im_class]
    while classes:
        c = classes.pop()
        if method_name in c.__dict__:
            return c
        else:
            classes = list(c.__bases__) + classes
    return None


class TestSolution(unittest.TestCase):
    
    def setUp(self):
        
        self.vw = VerticalWell(depth = 5000)
        self.hw = HorizontalWell(depth = 5000, length = 15000)
    
    def test_class_str_function_1(self):
        
        ans = get_class_that_defined_method(self.vw.__str__)

        self.assertEqual(ans, assignment7.Well)
        
    def test_class_str_function_2(self):
        
        ans = get_class_that_defined_method(self.hw.__str__)

        self.assertEqual(ans, assignment7.Well)
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_1(self, mock_stdout):
        
        print(self.vw)
        self.assertEqual(mock_stdout.getvalue(), 'Well type: vertical\n')
        
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_2(self, mock_stdout):
        
        print(self.hw)
        self.assertEqual(mock_stdout.getvalue(), 'Well type: horizontal\n')
        
    def test_attributes(self):
        
        self.assertAlmostEqual(self.vw.depth, 5000, places=4)
        self.assertAlmostEqual(self.hw.depth, 5000, places=4)
        self.assertAlmostEqual(self.hw.length, 15000, places=4)
        
    def test_wellbore_volume(self):
        
        self.assertAlmostEqual(self.vw.compute_wellbore_volume(diameter = 0.5), 981.7477042468104, places=6)
        self.assertAlmostEqual(self.hw.compute_wellbore_volume(diameter = 0.5), 3926.9908169872415, places=6)


if __name__ == "__main__":
    unittest.main()
