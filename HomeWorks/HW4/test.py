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

with open("assignment4.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment4.py", "w") as f:
    f.write(python_file)


from assignment4 import *


class TestSolution(unittest.TestCase):
 
    def test_get_2nd_element(self):
        
        ans = get_2nd_element([0, 20, 30, 40])

        self.assertEqual(ans, 20)
        
    
        
    
    def test_add_tuple_elements_1(self):
        
        ans = add_tuple_elements((9, 3))

        self.assertEqual(ans, 12)
        
    
    def test_add_tuple_elements_2(self):
        
        ans = add_tuple_elements((9, 3 , 4))

        self.assertEqual(ans, "Tuple must have exactly 2 elements!")
        
    
    def test_get_age_and_dob(self):
        
        adict = {'name': 'Romeo Montague', 'age': 32, 'DOB': '01/21/1594'}
        
        ans1, ans2 = get_age_and_dob(adict)

        self.assertEqual(ans1, 32)
        self.assertEqual(ans2, '01/21/1594')
        


if __name__ == "__main__":
    unittest.main()
