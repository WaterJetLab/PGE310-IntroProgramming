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
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, ColorBar, LinearAxis, Range1d, CustomJS, HoverTool
from bokeh.plotting import figure


class ProductionPlot(object):
    
    
    def __init__(self, production_df):
        
        production_df['date'] = pd.to_datetime(production_df['date'], format='%Y-%m-%d')
        
        production_df.set_index(['date'], inplace=True)
        production_df['api'] = production_df['api'].astype('str')

        oil_df = production_df.pivot(columns='api')['oil'][self.well_df.index.values.astype('str')]
        gas_df = production_df.pivot(columns='api')['gas'][self.well_df.index.values.astype('str')]
        
        self.production_dict = {}
        self.production_dict['apis'] = self.well_df.index.values.astype('str')
        self.production_dict['dates'] = [oil_df.index.values] * len(self.production_dict['apis'])
        self.production_dict['oil'] = [oil_df[name].values for name in oil_df]
        self.production_dict['gas'] = [gas_df[name].values for name in gas_df]
        
        return
    
    def create_production_plot(self):
        
        self.prod_plot = figure(plot_width=500, plot_height=400, 
                                x_axis_type='datetime', x_axis_label='Date',
                                y_axis_label='Oil (bbls)',
                                tools='box_zoom,pan')
       
        data_source = ColumnDataSource(data=self.production_dict)
        plot_source = ColumnDataSource(data=dict(dates=[self.production_dict['dates'][0]], 
                                                 oil=[self.production_dict['oil'][0]], 
                                                 gas=[self.production_dict['gas'][0]],
                                                 apis=[self.production_dict['apis'][0]],
                                                 plot_indices=[0]))
        
        # Setting the second y axis range name and range
        self.prod_plot.y_range=Range1d(0, np.nanmax(plot_source.data['oil']))
        self.prod_plot.extra_y_ranges = {"gas": Range1d(0, np.nanmax(plot_source.data['gas']))}

        # Adding the second axis to the plot.  
        self.prod_plot.add_layout(LinearAxis(y_range_name="gas", axis_label='Gas (mcf)'), 'right')
        
        self.prod_plot.yaxis[0].axis_label_text_color = "blue"
        self.prod_plot.yaxis[0].major_label_text_color = "blue"
        self.prod_plot.yaxis[1].axis_label_text_color = "green"
        self.prod_plot.yaxis[1].major_label_text_color = "green"
        
        # Add lines for production histories.
        self.prod_plot.multi_line(xs='dates', ys='oil', source=plot_source, line_width=2, 
                                  line_color='blue', line_alpha=0.4, 
                                  hover_line_color='blue', hover_line_alpha=1.0, name='oil')
        self.prod_plot.multi_line(xs='dates', ys='gas', source=plot_source, line_width=2, 
                                  line_color='green', line_alpha=0.4, hover_line_color='green', 
                                  hover_line_alpha=1.0, y_range_name='gas', name='gas')
        
        #Add hover tool 
        self.prod_plot.add_tools(HoverTool(renderers=[self.prod_plot.select_one({'name': 'oil'}), 
                                                      self.prod_plot.select_one({'name': 'gas'})], 
                                           tooltips=[('API', '@apis'),]))
        
        #Hack to control when to update figure based on hover or selection.
        update_flag_source = ColumnDataSource(data=dict(update_flag=[True]))
        
        #JS callback for interaction
        callback = CustomJS(args=dict(data_source=data_source, 
                                      plot_source=plot_source,
                                      update_flag_source=update_flag_source,
                                      yr=self.prod_plot.y_range, 
                                      extra_yr=self.prod_plot.extra_y_ranges), code="""
                                      
                var arraysEqual = function (arr1, arr2) {
                
                // Check if the arrays are the same length
                if (arr1.length !== arr2.length) return false;
                
                // Check if all items exist and are in the same order
                for (var i = 0; i < arr1.length; i++) {
                    if (arr1[i] !== arr2[i]) return false;
                }

                // Otherwise, return true
                return true;
                };
                
                var updateData = function (source, indices) {
                
                const data = {'dates': [], 'oil': [], 'gas': [], 'apis': [], 'plot_indices': []}

                for (var i = 0; i < indices.length; i++) {
                    data['dates'].push(source.data.dates[i]);
                    data['oil'].push(source.data.oil[i]);
                    data['gas'].push(source.data.gas[i]);
                    data['apis'].push(source.data.apis[i]);
                    data['plot_indices'].push(indices[i]);
                }
                return data;  
                };
                
                var nanMax = function (a, b) { return (isNaN(b) || b < a) ? a : b };
                
                var arrayMax = function(arr) {return arr.reduce(nanMax)};
                
                var maxAll = function(arr) {
                
                var max = Number.MIN_VALUE;
                for (var i = 0; i < arr.length; i++) {
                    max = nanMax(arrayMax(arr[i]), max);
                };
                
                return max;
                };
    
                var indices = [];
                
                if (cb_obj.tool_name === "Hover"){
                    indices = cb_data.index['1d'].indices;
                } else {
                    indices = cb_obj.indices;
                    if (!arraysEqual(plot_source.data.plot_indices, indices) && indices.length > 0){
                        plot_source.data = updateData(data_source, indices);
                        update_flag_source.data.update_flag[0] = false;
                    } else if (indices.length === 0) {
                        update_flag_source.data.update_flag[0] = true;
                    } else {
                        update_flag_source.data.update_flag[0] = false;
                    };
                };
               
                
                if (!arraysEqual(plot_source.data.plot_indices, indices) && indices.length > 0 && update_flag_source.data.update_flag[0]){    
                    plot_source.data = updateData(data_source, indices);
                }
                update_flag_source.change.emit()
                
                var oil_max = maxAll(plot_source.data['oil']);
                var gas_max = maxAll(plot_source.data['gas']);
                
                yr.start = 0
                yr.end = oil_max
                extra_yr['gas'].start = 0
                extra_yr['gas'].end = gas_max
                
                """)
        
        tooltips = [("API:", "@api"),
                    ("Cum. Oil. (bbls):", "@cumulative_oil"),
                    ("Cum. Gas. (mcf):", "@cumulative_gas"),]
        
        
        #Add hover w/ JS callback to well_plot
        self.well_plot.add_tools(HoverTool(tooltips=tooltips, 
                                           callback=callback, 
                                           renderers=[self.well_plot.select_one({'name': 'wells'})]))
        
        #Activate callback on change of selection
        well_source = self.well_plot.select_one({'name': 'wells'}).data_source
        well_source.selected.js_on_change('indices', callback)
        
        return

        
