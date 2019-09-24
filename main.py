from flask import Flask, render_template, request, redirect, url_for

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd
import numpy as np
import pickle
from bokeh.models import (CategoricalColorMapper, HoverTool,
                          ColumnDataSource, Panel,
                          FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
                                  Tabs, CheckboxButtonGroup,
                                  TableColumn, DataTable, Select)
from bokeh.layouts import column, WidgetBox
from bokeh.embed import components
from bokeh.layouts import gridplot

app = Flask(__name__)


@app.route('/')
def home():
    # get the dataset
    Table = pd.read_excel('AB_NYC_2019_excel.xlsx')
    Table = Table.dropna()
    cols = Table.columns
    row = np.sort(np.unique(Table['room_type'].tolist()))
    context = {'liste': cols, 'rows': row}

    #get the text to do the html that will be saved after each plot
    infile = open('vars.pkl', 'rb')
    variables, html_code = pickle.load(infile)
    infile.close()
    # initializes the pickle where the last plots will be saved
    outfile = open('vars.pkl', 'wb')
    pickle.dump([dict(vars_x=[], vars_y=[], lasts_rows=[]), html_code], outfile)
    outfile.close()

    return render_template('test.html', context=context)


@app.route('/tracer/<x_name>/<y_name>/<row_i>')
def tracer(x_name, y_name, row_i):
    # get all the inputs
    infile = open('vars.pkl', 'rb')
    variables, html_code = pickle.load(infile)
    infile.close()

    variables['vars_x'].append(x_name)
    variables['vars_y'].append(y_name)
    variables['lasts_rows'].append(row_i)

    outfile = open('vars.pkl', 'wb')
    pickle.dump([variables, html_code], outfile)
    outfile.close()

    # load the data
    Table = pd.read_excel('AB_NYC_2019_excel.xlsx')
    Table = Table.dropna()
    rows = np.sort(np.unique(Table['room_type'].tolist()))
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select,help"

    # output to static HTML file
    output_file("line.html")
    dico = {}
    vars_dico = {}
    p2 = []

    # iterate between all the data available and create a dict that will be the source
    # the common element will be the identifier
    for x_var, y_var, row_i in zip(variables['vars_x'], variables['vars_y'], variables['lasts_rows']):
        df = pd.DataFrame(np.array(Table[Table.room_type == row_i]), columns=list(Table.columns.values))
        vars_dico[x_var + '_' + row_i] = np.array(df[x_var].tolist())
        vars_dico[y_var + '_' + row_i] = np.array(df[y_var].tolist())

    vars_dico['id'] = df['id'].tolist()
    source = ColumnDataSource(vars_dico)

    # do the same loop that before and plot all the rows
    for x_var, y_var, row_i in zip(variables['vars_x'], variables['vars_y'], variables['lasts_rows']):
        p1 = figure(plot_width=525, plot_height=500, toolbar_location="right", title='plot '+x_var+' vs '+y_var+' row '+row_i,
                        tools=TOOLS)
        p1.circle(x=x_var + '_' + row_i, y=y_var + '_' + row_i, source=source, fill_color='green', size=3)
        p1.xaxis.axis_label = x_var
        p1.yaxis.axis_label = y_var
        p2.append(p1)

    list_plot = [p2[i:i+3] for i in range(0,len(p2), 3)]
    p3 = gridplot(list_plot)
    script, div = components(p3)

    #save each plot in a static html
    filename = 'templates/last_plots.html'
    f = open(filename,'w')
    f.write(html_code % (script, div))
    f.close()

    context = {'tracer': True, 'liste': Table.columns, 'rows': rows}

    return render_template('test.html', context=context, div=div, script=script)


@app.route('/change', methods=['POST'])
def change():
    x = request.form.get("x")
    y = request.form.get("y")
    row_i = request.form.get("row_i")

    return redirect(url_for('tracer', x_name=x, y_name=y, row_i=row_i))


if __name__ == "__main__":
    app.run()
