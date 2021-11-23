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
import os

import numpy as np

with open("assignment8.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment8.py", "w") as f:
    f.write(python_file)


from assignment8 import KozenyCarmen

class TestSolution(unittest.TestCase):

    def test_transform(self):

        kc = KozenyCarmen('poro_perm.csv')

        np.testing.assert_allclose(kc.kc_model()[0:10], 
                                   np.array([0.00144518, 0.00144518, 0.00178167, 
                                             0.00073352, 0.0035369, 0.00123457, 
                                             0.00194181, 0.00199742, 0.0022314, 
                                             0.00205417]), atol=0.0001)
        
if __name__ == '__main__':
    unittest.main()

