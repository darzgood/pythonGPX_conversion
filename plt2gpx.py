# Copyright (c) 2020 Darrell Good
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os

"""
To Use:
>>> python plt2gpx.py [PLT FILENAME].plt
"""


def plt2gpx(file):
    """
    Opens a PLT 'file' containing GPS points and timestamps and constructs a GPX
    track with them
    """
    base = os.path.splitext(file)[0]
    gpxFilename = base+".gpx"

    with open(file, "r") as PLTdata, open("gpxTemplate.gpx") as template, open(gpxFilename, "w") as GPXfile:
        #Skip PLT header
        for i in range(6):
            PLTdata.readline()
        for line in template:
            if "{{POINTS}}" in line:
                for pltLine in PLTdata:
                    GPXfile.write(getTrackPoint(pltLine.strip()))
            else:
                GPXfile.write(line)

def getTrackPoint(pltLine):
    """
    plt data is organized as:
    (0) latitude, (1) longitude, (2) unused, (3) altitude, (4) days since Dec. 30 1899, (5) date, (6) time.
    returns the xml code for a trkpt with data from pltLine
    """
    data = pltLine.split(",")
    trackPoint = \
    """\n\t<trkpt lat="{0}" lon="{1}">
    \t\t<ele>{2}</ele>
    \t\t<time>{3}T{4}Z</time>
    \t</trkpt>""".format(data[0], data[1], data[3], data[5], data[6])
    return trackPoint

if __name__ == "__main__":
    if len(sys.argv) > 1:
        plt2gpx(sys.argv[1])
    else:
        print("Please add the file to convert as an argument.")
