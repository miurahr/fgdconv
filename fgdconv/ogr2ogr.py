# -*- coding: utf-8 -*-
# Copyright (c) 2017 Hiroshi Miura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from osgeo import ogr
from osgeo import osr
import os


# only tested and confirmed formats are allowed
def is_valid(driver, filename):
    if driver == "ESRI Shapefile":
        if os.path.exists(filename):
            return False
        else:
            parent_d = os.path.dirname(filename)
            if os.path.exists(parent_d):
                return False
            else:
                return True
    elif driver == "GML":
        if os.path.exists(filename):
            return False
        else:
            return True
    else:
        return False


class Ogr2Ogr:
    def __init__(self, inRef, outRef):
        in_spatial_ref = osr.SpatialReference()
        in_spatial_ref.ImportFromEPSG(inRef)
        out_spatial_ref = osr.SpatialReference()
        out_spatial_ref.ImportFromEPSG(outRef)
        # create the CoordinateTransformation
        self.coordTrans = osr.CoordinateTransformation(in_spatial_ref,
                                                       out_spatial_ref)

    def convert(self, in_filename, in_driver,
                out_filename, out_driver):
        input_driver = ogr.GetDriverByName(in_driver)
        output_driver = ogr.GetDriverByName(out_driver)
        in_data_set = input_driver.Open(in_filename)
        in_layer = in_data_set.GetLayer()
        if out_driver == "ESRI Shapefile":
            basename = os.path.basename(out_filename)
            out_data_set = output_driver\
                .CreateDataSource(out_filename,
                                  options=["SHAPE_ENCODING=UTF-8",
                                           "ENCODING=UTF-8"])
            out_layer = out_data_set.CreateLayer(basename,
                                                 geom_type=ogr.wkbMultiPolygon)
        else:
            out_data_set = output_driver.CreateDataSource(out_filename)
            basename = os.path.basename(out_filename)
            out_layer = out_data_set.CreateLayer(basename,
                                             geom_type=ogr.wkbMultiPolygon)
        in_defn = in_layer.GetLayerDefn()
        for i in range(0, in_defn.GetFieldCount()):
            field_defn = in_defn.GetFieldDefn(i)
            out_layer.CreateField(field_defn)
        out_defn = out_layer.GetLayerDefn()
        in_feature = in_layer.GetNextFeature()
        while in_feature:
            geom = in_feature.GetGeometryRef()
            geom.Transform(self.coordTrans)
            out_feature = ogr.Feature(out_defn)
            out_feature.SetGeometry(geom)
            for i in range(0, out_defn.GetFieldCount()):
                out_feature.SetField(out_defn.GetFieldDefn(i).GetNameRef(),
                                     in_feature.GetField(i))
            out_layer.CreateFeature(out_feature)
            in_feature = in_layer.GetNextFeature()

if __name__ == '__main__':
    pass