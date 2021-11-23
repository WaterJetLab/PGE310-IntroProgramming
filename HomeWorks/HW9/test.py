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

import skimage
import skimage.measure
import skimage.transform
import cv2
import warnings

import seaborn as sns; sns.set();
import matplotlib.pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

import numpy as np

with open("assignment9.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment9.py", "w") as f:
    f.write(python_file)


from assignment9 import KozenyCarmen


class TestSolution(unittest.TestCase):

    def test_transform(self):

        kc = KozenyCarmen('poro_perm.csv')
        kc.add_kc_model_to_df()

        np.testing.assert_allclose(kc.df['kc model'].values[0:10], 
                                   np.array([0.00144518, 0.00144518, 0.00178167, 
                                             0.00073352, 0.0035369, 0.00123457, 
                                             0.00194181, 0.00199742, 0.0022314, 
                                             0.00205417]), atol=0.0001)
        
        
        
    def test_plot(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            p = KozenyCarmen('poro_perm.csv')
            
            fig, ax = plt.subplots(figsize=(8, 6))
            p.plot(ax=ax)
            ax.set_xlabel(r'$\frac{\phi^3}{(1 - \phi)^2}$')
            ax.set_ylabel(r'$\kappa$ (mD)')
            ax.set_xlim([0, 0.0125]);
            plt.savefig('poro_perm.png')

            gold_image = cv2.imread('images/poro_perm_gold.png')
            test_image = cv2.imread('poro_perm.png')

            test_image_resized = skimage.transform.resize(test_image, 
                                                          (gold_image.shape[0], gold_image.shape[1]), 
                                                          mode='constant')

            ssim = skimage.measure.compare_ssim(skimage.img_as_float(gold_image), test_image_resized, multichannel=True)
            assert ssim >= 0.75
        
if __name__ == '__main__':
    unittest.main()

