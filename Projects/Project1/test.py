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

import pandas as pd


with open("project1.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)

with open("project1.py", "w") as f:
    f.write(python_file)

from project1 import NDWellProductionPlot

class TestSolution(unittest.TestCase):

    def setUp(self):

        self.df = NDWellProductionPlot('eog').well_df
        if 'api' in list(self.df):
            self.df.set_index(['api'])


        return

    def test_oil_production_values(self):

        gold_df = pd.Series({'33061025220000': 1077759.0, '33061018290000': 876378.0,
                             '33053040060000': 853484.0, '33061026450000': 829105.0,
                             '33061027160000': 809765.0}).rename_axis('api').rename('cumulative_oil')

        gold_df.index = gold_df.index.astype(self.df.index.dtype)

        pd.testing.assert_series_equal(
            self.df['cumulative_oil'].sort_values(ascending=False).head(),
            gold_df)

    def test_gas_production_values(self):

        gold_df = pd.Series({'33053040060000': 3527628.0, '33061025220000': 2025624.0,
                             '33053066030000': 1909689.0, '33053045720000': 1843840.0,
                             '33053070140000': 1714591.0}).rename_axis('api').rename('cumulative_gas')

        gold_df.index = gold_df.index.astype(self.df.index.dtype)

        pd.testing.assert_series_equal(
            self.df['cumulative_gas'].sort_values(ascending=False).head(),
            gold_df)

    def test_plot(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            p = NDWellProductionPlot('eog', 'oil')
            p.save_plot()

            gold_image = cv2.imread('images/eog_oil_wells_in_nd_gold.png')
            test_image = cv2.imread('eog_wells_in_nd.png')

            test_image_resized = skimage.transform.resize(test_image, 
                                                          (gold_image.shape[0], gold_image.shape[1]), 
                                                          mode='constant')

            ssim = skimage.measure.compare_ssim(skimage.img_as_float(gold_image), 
                                                test_image_resized, multichannel=True)
            assert ssim >= 0.75


if __name__ == '__main__':
    unittest.main()
