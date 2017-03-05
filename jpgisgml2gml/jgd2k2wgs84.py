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


class Jgd2kToWgs84:
    def __init__(self, inRef, outRef):
        self.driver = ogr.GetDriverByName('GML')
        # input SpatialReference to JGD2000
        in_spatial_ref = osr.SpatialReference()
        in_spatial_ref.ImportFromEPSG(inRef)
        # output SpatialReference to WGS84
        out_spatial_ref = osr.SpatialReference()
        out_spatial_ref.ImportFromEPSG(outRef)
        # create the CoordinateTransformation
        self.coordTrans = osr.CoordinateTransformation(in_spatial_ref,
                                                       out_spatial_ref)
        # prepare data store
        self.inLayer = None
        self.outLayer = None

    def convert(self, inFilename, outFilename):
        self.inDataSet = self.driver.Open(inFilename)
        self.inLayer = self.inDataSet.GetLayer()
        self.outDataSet = self.driver.CreateDataSource(outFilename)
        self.outLayer = self.outDataSet.CreateLayer("FGD_GML4326",
                                               geom_type=ogr.wkbMultiPolygon)
        # add fields
        inLayerDefn = self.inLayer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            self.outLayer.CreateField(fieldDefn)

        # get the output layer's feature definition
        outLayerDefn = self.outLayer.GetLayerDefn()

        # loop through the input features
        inFeature = self.inLayer.GetNextFeature()
        while inFeature:
            # get the input geometry
            geom = inFeature.GetGeometryRef()
            # reproject the geometry
            geom.Transform(self.coordTrans)
            # create a new feature
            outFeature = ogr.Feature(outLayerDefn)
            # set the geometry and attribute
            outFeature.SetGeometry(geom)
            for i in range(0, outLayerDefn.GetFieldCount()):
                outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(),
                                    inFeature.GetField(i))
            # add the feature to the shapefile
            self.outLayer.CreateFeature(outFeature)
            # dereference the features and get the next input feature
            outFeature = None
            inFeature = self.inLayer.GetNextFeature()

    def close(self):
        # Save and close
        self.inDataSet = None
        self.outDataSet = None
