from bokeh.plotting import figure, row, column
from bokeh.io import curdoc, show
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
from bokeh.layouts import layout
from bokeh.models import Slider
import numpy as np

#bokeh serve .\Projekt5.py --show
step=.2
x1_range=400
y1_limit = 60


def gen_y1(step,limit):
	x=0
	while True:
		yield limit*(.3+(np.sin(x/7)**2)/2+(np.cos(x/5)**2)/4)
		x+=step

def gen_xy2():
	i=0
	while True:
		for j in range(10):
			yield [i+np.random.triangular(-350,0,350), 2*i+np.random.triangular(-500,0,500)]
		i+=1
		
def gen_xy3():
	while True:
		yield [np.random.triangular(-6,-4.5,-3) if np.random.random()<.5 else np.random.triangular(3,4.5,6), np.random.triangular(-6,-4.5,-3) if np.random.random()<.5 else np.random.triangular(3,4.5,6)]



#curdoc=curdoc()
#generacja danych
x1=np.array(np.arange(0,x1_range,step))
y_gen1 = gen_y1(step,y1_limit)
y1=np.array([next(y_gen1) for xi in x1])

xy2=gen_xy2()
xy2_data=np.array([next(xy2) for i in range(10000)])

xy3=gen_xy3()
xy3_data=np.array([next(xy3) for i in range(3000)])

#print(xy2_data)
#print(xy3_data)

#wykresy
fig1=figure(
	x_range=(0,40),
	x_axis_label='x',y_axis_label='y',
	height=450,
	width=500,
	title="suwaki miały sterować x_range'em i y_range'em, ale nie wyszło",
	sizing_mode='stretch_width')
fig1.line(x1,y1,
		  line_width=2.3,
		  line_color='red')
fig1.grid.grid_line_dash=(61,15)
fig1.toolbar.logo = None
fig1.toolbar.autohide = True
fig1.circle(
    x1,
    y1,
    color='green',
    radius=np.log(y1/10)/5,
    fill_alpha=.25)

fig2=figure(
	background_fill_color=all_palettes['Viridis'][256][0],
	height=400,
	width=500,
	match_aspect=True,
	sizing_mode='scale_height')
fig2.grid.visible=False
fig2.toolbar.logo = None
fig2.toolbar.autohide = True

hex_size1=15.0
binned_data = hexbin(xy2_data[:,0],xy2_data[:,1],hex_size1)
cmap=linear_cmap('counts','Viridis256',0,max(binned_data['counts']))
fig2.hex_tile(
	size=hex_size1,
	source=binned_data,
	fill_color=cmap,
	line_color=None)



fig3=figure(
	background_fill_color=all_palettes['Inferno'][256][0],
	height=400,
	width=500,
	match_aspect=True,
	sizing_mode='scale_height')
fig3.grid.visible=False
fig3.toolbar.logo = None
fig3.toolbar.autohide = True

hex_size2=.1
binned_data2 = hexbin(xy3_data[:,0],xy3_data[:,1],hex_size2)
cmap=linear_cmap('counts','Inferno256',0,max(binned_data2['counts']))
fig3.hex_tile(
	size=hex_size2,
	source=binned_data2,
	fill_color=cmap,
	line_color=None)
#figure(x_range=(-10,10),y_range=(-10,10))
#fig3.scatter(x=xy3_data[:,0],y=xy3_data[:,1])

fig4=figure(
	background_fill_color=all_palettes['Inferno'][256][255],
	height=400,
	width=500,
	match_aspect=True,
	sizing_mode='scale_height')
fig4.grid.visible=False
fig4.toolbar.logo = None
fig4.toolbar.autohide = True

fig4.scatter(xy3_data[:,0],xy3_data[:,1], fill_color=all_palettes['Turbo'][256][80], line_color=all_palettes['Turbo'][256][80])

#suwaki
s1=Slider(
	start=0,end=300,step=.5,
	value=0,
	title='suwak, co nie działa',
	sizing_mode='fixed',
	width=300,
	height=30)


s2=Slider(
	start=0,end=1000,step=5,
	value=0,
	title='suwak, co nie działa 2',
	sizing_mode='fixed',
	width=300,
	height=30)





#def callback1(attr,old,new):
#	fig1.x_range=(0+s1.value,40+s1.value)
#s1.on_change('value',callback1)




upper=row(column(s1, s2), row(fig1,sizing_mode='stretch_width'))
lower = row(fig2, fig3, fig4, sizing_mode='scale_height')

l=layout(column(upper,lower),sizing_mode='stretch_width')
#l=layout([[column(s1, s2), fig1],
#		  [fig2, fig3]], sizing_mode='scale_height')

curdoc().add_root(l)
curdoc().title='nie działa'
#show(l)
