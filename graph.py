import numpy as np
import pandas as pd
import os
import argparse
from bokeh.layouts import layout
from bokeh.models import HoverTool, TapTool, CustomJS, Slider, ColumnDataSource, WidgetBox
from bokeh.plotting import figure, output_file, show
from bokeh.models.glyphs import Text

def figure_plot(f_name, fx_range=None, fy_range=None):
    df = pd.read_csv(f_name)

    source = ColumnDataSource(data=dict(
        x = df['FRAME'],
        y = df['PIX_VALUE_DIFF'],
    ))

    source_2 = ColumnDataSource(data=dict(
        x = df['FRAME'],
        y = df['PIX_VALUE_DIFF'],
    ))

    p = figure(title="Video Transition Analysis: "+f_name, width=1000, height=250, toolbar_location="below", x_range=fx_range, y_range=fy_range)

    p.step('x', 'y', source=source_2, color="#778899", alpha=0.8,  mode="center")
    cr = p.circle('x', 'y', source=source_2, radius=0.5, legend='Pixel Difference Value', fill_color="firebrick", hover_fill_color="red",
        line_color=None, hover_line_color="white", fill_alpha=0.2, hover_alpha=0.5)
    hover = HoverTool(tooltips=[
        ("Frame No.", "@x"),
        ("Pixel Difference Value", "@y"),
        ],
        renderers=[cr])
    p.add_tools(hover)
    p.xaxis.axis_label = 'Frame'
    p.yaxis.axis_label = 'Pixel Difference Value'
    p.grid.grid_line_alpha=0.5

    callback = CustomJS(args=dict(source=source, source_2=source_2), code="""
        var d = source.data;
        var d2 = source_2.data;
        var t = thres.value;
        y = d['y']
        y2 = d2['y']
        for (i = 0; i < y.length; i++) {
            if (y[i] <= t){
                y2[i]=0
            }
            else {
                y2[i]=y[i]
            }
        }
        source_2.change.emit();
    """)

    threshold_slider = Slider(start=0, end=100, value=0, step=1, title="Threshold", callback=callback, callback_policy='throttle')
    callback.args["thres"] = threshold_slider
    widgets = WidgetBox(threshold_slider)
    return widgets, p, p.x_range, p.y_range

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='*', type=argparse.FileType('r'), help="Directory of input file.")
    args = parser.parse_args()

    input_files = args.input
    x_r=y_r = 0
    plots = []
    for i, file in enumerate(input_files):
        if i == 0:
            w, f, x_r, y_r = figure_plot(file.name)
            DATA_DIR = os.path.dirname(file.name)
            DATA_NAME = file.name.split('/')[-2]
        else:
            w, f, _x_r, _y_r = figure_plot(file.name, x_r, y_r)
        plots.extend((w,f))

    output_file(os.path.join(DATA_DIR, DATA_NAME+'_compare.html'), title=DATA_NAME)
    l = layout(plots, sizing_mode='scale_width')

    show(l)
