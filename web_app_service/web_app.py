from dash import Dash, html, dcc, Input, Output
from dash import dash_table as dt
import plotly.graph_objects as go
import plotly.express as px
from db_api.db_api import get_data_from_db

css = [{'rel': "stylesheet",
		'href': "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"}]

app = Dash(__name__, external_stylesheets=css)

colors = {
	'background': '#D6CBE0',
	'background2': 'white',
	'background3': 'black',
	'background4': 'blue',
}

app.layout = html.Div(id='parent', className="container-fluid",
					  children=[
						  html.Div(className='row',children=[
							  html.Div(className='col-1', children=[
								  html.Img(src='static/img/kanalservice_logo.jpg', style={'width': '100px', "height": '100px'}),
							  ]),
							  html.Div(className='col-11', children=[
								  html.H1('Kanalservice dashboard')
							  ])

						  ]),
						  html.Div(className='row', children=[
							  html.Div(
								  id='left', style={'border': f'4px solid {colors["background2"]}'},
								  className='col-6', children=[
									  dcc.Graph(id='my-graph'),
									  dcc.Interval(
										  id='interval-component',
										  interval=10 * 1000,  # in milliseconds
										  n_intervals=0,
										  # max_intervals=0
									  ),
								  ]),
							  html.Div(id='right', className='col-6', children=[
								  html.Div(className='row', children=[
									  html.Div('col-right.top', id='right_top',
											   style={'border': f'4px solid {colors["background3"]}', 'text-align': 'center',
													  'font-size': '50px'},
											   className='col')]),
								  html.Div(className='row', children=[
									  html.Div('col-right.bottom', id='right_bottom',
											   style={'border': f'4px solid {colors["background4"]}'},
											   className='col')
								  ])

							  ])
						  ])])


@app.callback(Output('my-graph', 'figure'),
			  Output('right_top', 'children'),
			  Output('right_bottom', 'children'),
			  Input('interval-component', 'n_intervals'))
def update_graph(n):
	df = get_data_from_db()
	df['tg_noticed'] = df['tg_noticed'].apply(lambda x: str(x))
	df['deleted'] = df['deleted'].apply(lambda x: str(x))
	last_25 = df.iloc[-25:]
	return {
		'data': [{'x': last_25.delivery_date, 'y': last_25.cost_dollars}],
		'layout': {'uirevision': df, 'margin': {'l': 30,'r': 20,'b': 30,'t': 20}}}, f'{df.cost_dollars.sum()} $', generate_table(df)


def generate_table(dataframe):
	return html.Table(className='table table-striped', style={"display":"block", "max-height":"500px", "overflow-y":"auto"}, children=[
		html.Caption('*Отображены только те записи, которые присутствуют в текущей версии Google Sheet. Удаленные не отображаются.', style={"caption-side": "top"}),
		html.Thead(
			html.Tr([html.Th(col) for col in ["номер заказа", "стоимость $", "дата доставки", "курс обмена", "цена Руб", "уведомление тг", "был ли удален из Google Sheet"]])
		),
		html.Tbody(children=[
			html.Tr([
				html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
			]) for i in range(len(dataframe))
		])
	])


if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=8000)
