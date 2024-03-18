import json
import os
import pandas as pd
from bokeh.io import show, output_file
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import Div

def visualise():

    project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file_path = os.path.join(project_root_dir, 'main.html')
    output_file(output_file_path)

    # Load your JSON data
    with open('aggregated_data.json', 'r') as f:
        data = json.load(f)

    # Convert your JSON data to a format suitable for plotting
    source_protocol = ColumnDataSource(pd.DataFrame(list(data['protocol_counts'].items()), columns=['Protocol', 'Count']))
    source_encryption = ColumnDataSource(pd.DataFrame(list(data['encryption_counts'].items()), columns=['Encryption Status', 'Count']))
    source_country_traffic = ColumnDataSource(pd.DataFrame(list(data['country_traffic'].items()), columns=['Country Traffic', 'Count']))
    source_port_traffic = ColumnDataSource(pd.DataFrame(list(data['port_traffic'].items()), columns=['Port Traffic', 'Count']))
    source_traffic_between_countries = ColumnDataSource(pd.DataFrame(list(data['traffic_between_countries'].items()), columns=['Traffic Between Countries', 'Count']))

    # Create plots with responsive layout and label optimizations
    plot_width = 300  # Adjust width as needed
    plot_height = 300  # Adjust height as needed

    plot_protocol = figure(
        x_range=list(data['protocol_counts'].keys()),
        title="Protocol Counts",
        tools="pan,box_zoom,reset",
        width=plot_width,
        height=plot_height,
        sizing_mode="scale_width"  # Enable responsive layout
    )
    plot_protocol.vbar(x='Protocol', top='Count', source=source_protocol, width=0.9, color='royalblue')
    plot_protocol.y_range.start = 0
    # plot_protocol.xaxis.major_label_orientation = "vertical"  # Rotate labels

    plot_encryption = figure(
        x_range=list(data['encryption_counts'].keys()),
        title="Encryption Counts",
        tools="pan,box_zoom,reset",
        width=plot_width,
        height=plot_height,
        sizing_mode="scale_width"  # Make responsive
    )
    plot_encryption.vbar(x='Encryption Status', top='Count', source=source_encryption, width=0.9, color='darkorange')
    plot_encryption.y_range.start = 0
    # plot_encryption.xaxis.major_label_orientation = "vertical"  # Rotate labels

    plot_country_traffic = figure(
        x_range=list(data['country_traffic'].keys()),
        title="Country Traffic",
        tools="pan,box_zoom,reset",
        width=plot_width,
        height=plot_height,
        sizing_mode="scale_width"  # Make responsive
    )
    plot_country_traffic.vbar(x='Country Traffic', top='Count', source=source_country_traffic, width=0.9, color='forestgreen')
    plot_country_traffic.y_range.start = 0
    plot_country_traffic.xaxis.major_label_orientation = "vertical"  # Rotate labels

    # Make plot_port_traffic and plot_traffic_between_countries responsive
    plot_port_traffic = figure(
        x_range=list(data['port_traffic'].keys()),
        title="Port Traffic",
        tools="pan,box_zoom,reset",
        width=plot_width,
        height=plot_height,
        sizing_mode="scale_width"
    )
    plot_port_traffic.vbar(x='Port Traffic', top='Count', source=source_port_traffic, width=0.9, color='purple')
    plot_port_traffic.y_range.start = 0
    plot_port_traffic.xaxis.major_label_orientation = "vertical"  # Rotate labels

    plot_traffic_between_countries = figure(
        x_range=list(data['traffic_between_countries'].keys()),
        title="Traffic Between Countries",
        tools="pan,box_zoom,reset",
        width=plot_width,
        height=plot_height,
        sizing_mode="scale_width"
    )
    plot_traffic_between_countries.vbar(x='Traffic Between Countries', top='Count', source=source_traffic_between_countries, width=0.9, color='gold')
    plot_traffic_between_countries.y_range.start = 0
    # plot_traffic_between_countries.xaxis.major_label_orientation = "vertical"  # Rotate labels

    # Display link rate metrics as text
    metrics_text = f'''
    <strong>Link Rate Metrics:</strong><br>
    Bytes per Second: {data["bytes_per_second"]}<br>
    Packets per Second: {data["packets_per_second"]}<br>
    Total Bytes: {data["total_bytes"]}<br>
    Total Packets: {data["total_packets"]}<br>
    Encrypted Percentage: {data["encrypted_percentage"]}%
    '''
    div_metrics = Div(text=metrics_text)

    # Layout plots in a 2x3 grid
    layout = gridplot(
        children=[
            plot_protocol, plot_encryption, plot_country_traffic,
            plot_port_traffic, plot_traffic_between_countries, div_metrics
        ], ncols=3
    )

    # Show the layout
    show(layout)