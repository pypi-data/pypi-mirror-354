__copyright__ = """
Copyright (C)  2022 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from osgeo import gdal
import pandas as pd
import os
import random
import subprocess

class CSV2Raster:
    def __init__(self, input_file='', output_file='output.nc', sep=" ", dataframe=''):
        self.input_file = input_file
        self.inputfile_sep = sep
        self.tempOut = output_file
        self.output_file = 'output.nc'
        self.dataFrame = dataframe

    def convert(self):
        if self.input_file != '':
            self.dataFrame = pd.read_csv(self.input_file,
                                         sep=self.inputfile_sep,
                                         header=None, index_col=None)

        self.dataFrame = self.dataFrame.sort_values(['y', 'x'], ascending=[True, True])
        dataFrameColumns = self.dataFrame.columns

        randInt = str(random.randint(0, 100000))
        self.dataFrame = self.dataFrame.sort_values(by=['y', 'x'], ascending=[False, True])

        for i in range(2, len(dataFrameColumns)):
            self.dataFrame.to_csv("xyzformat.xyz", index=False, header=None, sep=" ")
            raster = gdal.Translate("temp_" + randInt + "_" + str(dataFrameColumns[i]) + ".nc", "xyzformat.xyz")
            self.dataFrame = self.dataFrame.drop(columns=dataFrameColumns[i])
            buffer = 'ncrename -v Band1,' + str(dataFrameColumns[i]) + " temp_" + randInt + "_" + str(dataFrameColumns[i]) + ".nc"
            print(subprocess.getstatusoutput(buffer))

        buffer = 'cdo -f nc2 cat ' + "temp_" + randInt + "_*.nc " + self.output_file
        print(subprocess.getstatusoutput(buffer))

        buffer = 'rm ' + "temp_" + randInt + "_*.nc"
        print(subprocess.getstatusoutput(buffer))

        if self.tempOut[-3:] == '.nc':
            os.rename(self.output_file, self.tempOut)
        elif self.tempOut[-3:] == 'iff' or self.tempOut[-3:] == 'tif':
            buffer = 'gdal_translate -of GTiff output.nc ' + self.tempOut
            print(subprocess.getstatusoutput(buffer))
            buffer = 'rm output.nc'
            print(subprocess.getstatusoutput(buffer))
        else:
            os.rename(self.output_file, self.tempOut + ".nc")

        os.remove("xyzformat.xyz")
