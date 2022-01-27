from bokeh.plotting import figure, row, column
from bokeh.io import show
from bokeh.layouts import layout
import pandas as pd
import numpy as np
from os.path import join

kraj = 'Poland'
HLE = pd.read_csv('HLE-IHME.csv')

HLE = HLE[~HLE.isnull().any(axis=1)]
HLE1 = HLE.loc[HLE['Entity'] == kraj]
x = HLE1['Year'].to_numpy()
y1 = HLE1['Healthy Life Expectancy (IHME)'].to_numpy()
y2 = HLE1['Life Expectancy (IHME)'].to_numpy()
y3 = HLE1['Years Lived With Disability (IHME)'].to_numpy()

HLE2 = HLE.groupby('Entity').agg(HLE=('Healthy Life Expectancy (IHME)',np.max),LE=('Life Expectancy (IHME)',np.max), diff = ('Years Lived With Disability (IHME)',np.max))

#wykresy
fig1=figure(
	x_range=(1988,2018),
	x_axis_label='rok',y_axis_label='y',
	height=450,
	width=500,
	title=kraj,
	sizing_mode='stretch_width')
fig1.line(x,y1,
		line_width=2.3,
		line_color='red')
fig1.line(x,y2,
		line_width=2.3,
		line_color='green')
fig1.grid.grid_line_dash=(61,15)
fig1.toolbar.logo = None
fig1.toolbar.autohide = True

fig2=figure(
	x_range=(1988,2018),
	x_axis_label='rok',y_axis_label='y',
	height=450,
	width=500,
	title=kraj,
	sizing_mode='stretch_width')
fig2.line(x,y3,
		line_width=2.3,
		line_color='red')
fig2.line(x,y2-y1,
		line_width=2.3,
		line_color='green')
fig2.grid.grid_line_dash=(61,15)
fig2.toolbar.logo = None
fig2.toolbar.autohide = True

fig4=figure(
	x_range=list(HLE2.index.values)[:15],
	x_axis_label='kraj',y_axis_label='najdłuższa zpodziewana długość życia',
	height=420,
	width=500,
	title=kraj,
	sizing_mode='stretch_width',
	toolbar_location='right')
fig4.xgrid.grid_line_color = None
fig4.toolbar.logo = None
fig4.toolbar.autohide = True
fig4.vbar(x = HLE2.index.values[:15],top = HLE2['LE'].to_numpy()[:15], width = .7)
fig4.x_range.range_padding = .1


l=layout(fig4,[fig1,fig2])
show(l)


#print(HLE2.index.values)

#for row in HLE2.index:
#	print(row)

#print(x,'\n\n',y1,'\n\n',y2,'\n\n',y3)
#for i in x:
#	print(i)
#cd = pd.read_csv(HLE, parse_dates=['Year'])

#print(cd[['Year','Healthy Life Expectancy (IHME)']].to_numpy())
#print(cd.index)
#cd[].count() cd[].max() cd[].unique() cd[].value_counts() cd[].describe() .value_counts()
#cd.loc() cd.iloc()

#print(cd.iloc[1:10,3])
#print(cd.loc[1:10,'Year'])
#cd['Year']=cd['Year'].astype('int16')
#print(cd.dtypes)
#print(cd['Year'])

#cd.groupby('Year').agg(sum_cases=('Healthy Life Expectancy (IHME)',np.sum),sum_cases=('Healthy Life Expectancy (IHME)',np.sum))

