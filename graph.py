import numpy as np
import pandas as pd
import os
from bokeh.layouts import layout
from bokeh.models import HoverTool, TapTool, CustomJS, Slider, ColumnDataSource, WidgetBox
from bokeh.plotting import figure, output_file, show

output_file('compare.html')

BASE_DIR = "/Users/agoraqa/Desktop/videos/iOS/test3_blackmagic/point/"
loss10_1 = "loss10_1_point"
loss10_2 = "loss10_2_point"
loss20_1 = "loss20_1_point"
loss20_2 = "loss20_2_point"
suffix = ".csv"

def figure_plot(f_name, fx_range=None, fy_range=None):
    df = pd.read_csv(BASE_DIR+f_name+suffix)

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

    threshold_slider = Slider(start=0, end=100, value=0, step=1, title="Threshold", callback=callback, callback_policy='mouseup')
    callback.args["thres"] = threshold_slider
    widgets = WidgetBox(threshold_slider)
    return widgets, p, p.x_range, p.y_range

w1, f1, f1_x_range, f1_y_range = figure_plot(loss10_1)
w2, f2, f2_x_range, f2_y_range = figure_plot(loss10_2, f1_x_range, f1_y_range)
w3, f3, f3_x_range, f3_y_range = figure_plot(loss20_1, f1_x_range, f1_y_range)
w4, f4, f4_x_range, f4_y_range = figure_plot(loss20_2, f1_x_range, f1_y_range)

l = layout([
    w1,
    f1,
    w2,
    f2,
    w3,
    f3,
    w4,
    f4,
], sizing_mode='scale_width')

show(l)
