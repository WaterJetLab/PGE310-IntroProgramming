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


with open("assignment11.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)

with open("assignment11.py", "w") as f:
    f.write(python_file)

from assignment11 import WellPlot

class TestSolution(unittest.TestCase):

    def test_plot(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            p = WellPlot('eog_wells_in_nd.csv')
            p.save_plot()

            gold_image = cv2.imread('images/eog_wells_in_nd_gold.png')
            test_image = cv2.imread('eog_wells_in_nd.png')

            test_image_resized = skimage.transform.resize(test_image,
                                                          (gold_image.shape[0], gold_image.shape[1]),
                                                          mode='constant')

            ssim = skimage.measure.compare_ssim(skimage.img_as_float(gold_image),
                                                test_image_resized, multichannel=True)
            assert ssim >= 0.75


if __name__ == '__main__':
    unittest.main()
