import pandas as pd
import numpy as np
from io import StringIO
import json

class TranformUtil:
    
    def plotly_tranform(self, csv_bytestream):
        '''
        This will tranform the s3 response into a format
        suitable for Plotly.js graph.

        - X-Axis is the time progression
        - Y-Axis is the value
        - Each 'point' is a series (one dataframe column)
        {
            points: [
                {
                    x: [july01, july02, july03],
                    y: [it1_row[0], it2_row[0], it3_row[0]]
                },
                {
                    x: [july01, july02, july03],
                    y: [it1_row[1], it2_row[1], it3_row[1]]
                }, . . .
            ]
        }
        :param df:
        :return: json
        '''
        s = str(csv_bytestream, 'utf-8')
        buffered_string = StringIO(s) # allows for buffered reading of the String
        df = pd.read_csv(buffered_string,
                            dtype=np.float32,
                            index_col='timestamp',
                            parse_dates=True
                        )
        # make x once, it is shared across all points
        x = df.index.values.tolist()
        points = []
        # there will be as many points as there are columns
        cols = df.values.shape[1]

        for col_count in range(cols):
            point = {'x': x, 'y': []}
            points.append(point)

        for row in df.itertuples(index=True):
            col_count = 0
            while col_count < cols:
                points[col_count]['y'].append(row[col_count+1])
                col_count += 1

        data = {}
        data['points'] = points
        return json.dumps(data)
