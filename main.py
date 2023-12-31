from io import StringIO

import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import gpxpy.gpx
from pandas.io.parsers import TextFileReader

TIME_ELEVATION = '$.initChartDenivele'
TIME_SPEED = '$.initChartSpeed'
POSITION = '$.initTracks'


def getJSArray(new_char) -> str:
    array: str = ""
    square_brackets: int = 0
    opens: bool = False
    while not (square_brackets <= 0 and opens):
        char: str = new_char()
        if char != '(':
            array += char
        if char == '[':
            array = array[:-2]
            square_brackets += 1
            opens = True
        elif char == ']':
            array = array[:-1] + '\n'
            square_brackets -= 1
        elif char == '{':
            array = array[:-2]
            square_brackets += 1
            opens = True
        elif char == '}':
            array = array[:-1] + '\n'
            square_brackets -= 1

    return array


def read_html_page(filepath: str):
    buffer_string: str = ""
    df = pd.DataFrame()
    dfLoc = pd.DataFrame()
    with open(filepath) as f:
        while "</html>" not in buffer_string:
            new_char: str = f.read(1)
            if new_char.isspace() or new_char == '(':
                buffer_string = ""
            else:
                buffer_string += new_char

            if TIME_ELEVATION in buffer_string:
                temp = getJSArray(lambda: f.read(1))
                df = pd.read_csv(
                        StringIO(temp),
                        sep=',',
                        names=['Unix-Time', 'Elevation-Meters']
                )
                print(df)
                buffer_string = ""
            if TIME_SPEED in buffer_string:
                temp = getJSArray(lambda: f.read(1))
                df2 = pd.read_csv(
                        StringIO(temp),
                        sep=',',
                        names=['Unix-Time', 'Speed-Meters']
                )
                print(df2)
                df = df.join(
                    df2.set_index('Unix-Time'),
                    how='outer',
                    on='Unix-Time'
                )
                print(df)
                buffer_string = ""
            if POSITION in buffer_string:
                temp = getJSArray(lambda: f.read(1))
                trim = lambda x: x[4:]
                dfLoc = pd.read_csv(
                        StringIO(temp),
                        sep=',',
                        names=['Lat', 'Long'],
                        converters={'Long': trim, 'Lat': trim}
                    )
                print(dfLoc)
                buffer_string = ""
    df['Unix-Time'] = pd.to_datetime(df['Unix-Time'],unit='ms')
    dfCount: float = df.shape[0]
    locCount: float = dfLoc.shape[0]
    countRatio: float = dfCount / locCount
    plt.plot(df['Unix-Time'],df['Speed-Meters'])
    plt.plot(df['Unix-Time'], df['Elevation-Meters'])
    #plt.show()

    # gpx setup
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for index, row in dfLoc.iterrows():
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
            latitude=row['Lat'],
            longitude=row['Long'],
            time=df['Unix-Time'][np.floor(index * countRatio)],
            elevation=df['Elevation-Meters'][np.floor(index * countRatio)],
            speed=df['Speed-Meters'][np.floor(index * countRatio)]
        ))

    print('Created GPX:', gpx.to_xml())

    with open(filepath[:-4]+'gpx','w') as f:
        f.write(gpx.to_xml())

def main():
    for i in range(18,22):
        read_html_page(f'temp/{i}.html')

main()