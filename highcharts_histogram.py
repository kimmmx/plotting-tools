import os
import webbrowser
import pandas as pd
from highcharts import Highchart


def create_histogram(src_csv, dst_html, title=None, subtitle=None,
                     x_axis_header=None, y_axis_header=None, x_axis_name=None, y_axis_name=None):
    """Creates basic histogram using Highcharts

        Args:
            src_csv (string): Path to csv with source data
            dst_html (string): Path to destination html output
            title (string): Title of histogram
            subtitle (string): Subtitle of histogram
            x_axis_header (str): Name of x-axis header in csv file. Defaults to None.
            y_axis_header (str): Name of y-axis header in csv file. Defaults to None.
            x_axis_name (str): Name of x-axis to use in histogram. Defaults to None.
            y_axis_name (str): Name of y-axis to use in histogram. Defaults to None.

        Returns:
            None.

    """

    # Check destination
    if dst_html[-5:] == '.html':
        dst_chart = dst_html[:-5]  # Omit '.html' for exporting with Highcharts
    else:
        dst_chart = dst_html
        dst_html += '.html'

    # Import source csv into pandas DataFrame
    src_df = pd.read_csv(src_csv)

    # Define headers if not given
    if not x_axis_header:
        x_axis_header = src_df.columns[0]
    if not y_axis_header:
        y_axis_header = src_df.columns[1]

    # Define axis names if not given
    if not x_axis_name:
        x_axis_name = x_axis_header
    if not y_axis_name:
        y_axis_name = y_axis_header

    # Convert source to list of lists
    hist_data = []
    for index, row in src_df.iterrows():
        hist_data.append([str(row[x_axis_header]), float(row[y_axis_header])])

    # Define chart options
    options = {
        'chart': {
            'type': 'column',
            # 'zoomType': 'x'  # Causes incorrect x-axis labels when zoomed out too far
        },
        'title': {
            'text': title
        },
        'subtitle': {
            'text': subtitle
        },
        'xAxis': {
            'type': 'category',
            'title': {
                'text': x_axis_name
            }
        },
        'yAxis': {
            'title': {
                'text': y_axis_name
            }
        },
        'tooltip': {
            'shared': True,
            'pointFormat': '{point.y:,.0f}'
        },
        'legend': {
            'enabled': False
        },
        'plotOptions': {
            'series': {
                'borderWidth': 0,
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.y:,.0f}'
                }
            }
        },
    }

    # Create chart, export, and open
    h = Highchart(width=1920, height=1080)
    h.set_dict_options(options)
    h.add_data_set(hist_data, 'column')
    h.save_file(dst_chart)
    webbrowser.open('file://' + dst_html)


if __name__ == '__main__':  # Example usage

    # Define home folder
    home_path = os.path.expanduser('~')

    # Define source csv
    source = os.path.join(home_path, 'Documents/histogram2.csv')

    # Define path to destination html
    destination = os.path.join(home_path, 'Documents/output.html')

    create_histogram(source, destination,
                     title='AMI Temperature Distribution',
                     subtitle='Histogram of all AMI meter temperature readings until 08/23/2016',
                     x_axis_name='Temperature',
                     y_axis_name='Number of readings'
                     )
