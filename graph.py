import numpy as np
import pandas as pd
import os
from bokeh.layouts import layout
from bokeh.models import HoverTool, TapTool, CustomJS, Slider, ColumnDataSource, WidgetBox
from bokeh.plotting import figure, output_file, show

output_file('dashboard.html')

BASE_DIR = "/Users/agoraqa/Desktop/videos/iOS/test3_blackmagic/point/"
loss10_1 = "loss10_1_point"
loss10_2 = "loss10_2_point"
loss20_1 = "loss20_1_point"
loss20_2 = "loss20_2_point"
suffix = ".csv"
clean_threshold=0

def read_csv(dir):
    return pd.read_csv(dir)

# def data_source(f_name):
#     df = read_csv(BASE_DIR+f_name+suffix)
#     source = ColumnDataSource(data=dict(
#         x = df['FRAME'],
#         y = df['PIX_VALUE_DIFF'],
#         # desc = df['DESC']
#     ))
#     return source


def figure_plot(f_name, fx_range=None, fy_range=None, threshold=0):
    df = read_csv(BASE_DIR+f_name+suffix)

    # Cleaning freeze frame pixel value
    if threshold != 0:
        df.loc[(df['PIX_VALUE_DIFF'] <= threshold) & (df['PIX_VALUE_DIFF'] >= -threshold), 'PIX_VALUE_DIFF'] = 0
        df.loc[df['PIX_VALUE_DIFF']==0, 'DESC'] = 'Freeze frame'
        df.loc[df['PIX_VALUE_DIFF']!=0, 'DESC'] = 'Moving frame'
    else:
        df['DESC'] = ''

    source = ColumnDataSource(data=dict(
        x = df['FRAME'],
        y = df['PIX_VALUE_DIFF'],
        desc = df['DESC']
    ))

    p = figure(title="Video Transition Analysis: "+f_name, width=1000, height=250, toolbar_location="below", x_range=fx_range, y_range=fy_range)

    p.step('x', 'y', source=source, color="#778899", alpha=0.8,  mode="center")
    cr = p.circle('x', 'y', source=source, radius=0.5, legend='Pixel Difference Value', fill_color="firebrick", hover_fill_color="red",
        line_color=None, hover_line_color="white", fill_alpha=0.2, hover_alpha=0.5)

    hover = HoverTool(tooltips=[
        ("Frame No.", "@x"),
        ("Pixel Difference Value", "@y"),
        ("Description", "@desc")
        ],
        renderers=[cr])
    p.add_tools(hover)
    p.xaxis.axis_label = 'Frame'
    p.yaxis.axis_label = 'Pixel Difference Value'
    p.grid.grid_line_alpha=0.5
    return p, p.x_range, p.y_range

# def slider():
#     x = np.linspace(0, 10, 100)
#     y = np.sin(x)
#
#     source = ColumnDataSource(data=dict(x=x, y=y))
#
#     plot = figure(
#         y_range=(-10, 10), tools='', toolbar_location=None,
#         title="Sliders example")
#     plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
#
#     callback = CustomJS(args=dict(source=source), code="""
#         var data = source.data;
#         var t = thres.value;
#         x = data['x']
#         y = data['y']
#         for (i = 0; i < x.length; i++) {
#             y[i] = y+t/10;
#         }
#         source.change.emit();
#     """)
#
#     threshold_slider = Slider(start=0, end=10, value=1, step=0.1, title="Threshold", callback=callback, callback_policy='mouseup')
#     callback.args["thres"] = threshold_slider
#     widgets = WidgetBox(threshold_slider)
#     return widgets, plot

f1, f1_x_range, f1_y_range = figure_plot(loss10_1, threshold=clean_threshold)
f2, f2_x_range, f2_y_range = figure_plot(loss10_2, f1_x_range, f1_y_range, threshold=clean_threshold)
f3, f3_x_range, f3_y_range = figure_plot(loss20_1, f1_x_range, f1_y_range, threshold=clean_threshold)
f4, f4_x_range, f4_y_range = figure_plot(loss20_2, f1_x_range, f1_y_range, threshold=clean_threshold)

# widgets, plot = slider()

l = layout([
    # widgets,
    # plot,
    f1,
    f2,
    f3,
    f4,
], sizing_mode='scale_width')

show(l)
