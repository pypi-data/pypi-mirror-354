import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

class BioreactorDashboard:
    def __init__(self, data_path='simulation_outputs/'):
        """
        Initialize bioreactor dashboard
        
        Args:
            data_path: Path to simulation output data
        """
        self.data_path = data_path
        self.app = dash.Dash(__name__)
        self._setup_layout()
        self._setup_callbacks()
        
    def _setup_layout(self):
        """Set up dashboard layout"""
        self.app.layout = html.Div([
            html.Div([
                html.H1("Festo Bioreactor Dashboard", style={'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.H3("Current Status"),
                        html.Div(id='status-indicators'),
                    ], className='four columns'),
                    
                    html.Div([
                        html.H3("Control Settings"),
                        html.Div([
                            html.Label("Temperature Setpoint:"),
                            dcc.Slider(
                                id='temp-setpoint',
                                min=25, max=45, step=0.5,
                                value=37,
                                marks={i: str(i) for i in range(25, 46, 5)}
                            ),
                            
                            html.Label("pH Setpoint:"),
                            dcc.Slider(
                                id='ph-setpoint',
                                min=6, max=8, step=0.1,
                                value=7.2,
                                marks={i: str(i) for i in range(6, 9)}
                            ),
                            
                            html.Label("DO Setpoint:"),
                            dcc.Slider(
                                id='do-setpoint',
                                min=0, max=100, step=1,
                                value=30,
                                marks={i: str(i) for i in range(0, 101, 20)}
                            ),
                        ]),
                    ], className='four columns'),
                    
                    html.Div([
                        html.H3("Simulation Controls"),
                        html.Button('Start Simulation', id='start-sim', n_clicks=0),
                        html.Button('Pause Simulation', id='pause-sim', n_clicks=0),
                        html.Div(id='sim-status'),
                    ], className='four columns'),
                ], className='row'),
                
                html.Div([
                    dcc.Graph(id='biomass-plot'),
                    dcc.Graph(id='controls-plot'),
                    dcc.Graph(id='temperature-plot'),
                    dcc.Graph(id='biomass-growth-plot'),
                ], className='row'),
                
                dcc.Interval(
                    id='interval-component',
                    interval=1000,  # in milliseconds
                    n_intervals=0
                )
            ], className='container')
        ])
    
    def _setup_callbacks(self):
        """Set up dashboard callbacks"""
        @self.app.callback(
            Output('biomass-plot', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_biomass_plot(n):
            df = self._load_data()
            return self._create_biomass_figure(df)
        
        @self.app.callback(
            Output('controls-plot', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_controls_plot(n):
            df = self._load_data()
            return self._create_controls_figure(df)
        
        @self.app.callback(
            Output('status-indicators', 'children'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_status(n):
            df = self._load_data()
            latest = df.iloc[-1]
            return html.Div([
                html.Div([
                    html.H4("Current Values"),
                    html.P(f"Temperature: {latest['temperature']:.1f} °C"),
                    html.P(f"pH: {latest['ph']:.1f}"),
                    html.P(f"DO: {latest['do']:.1f}%"),
                    html.P(f"Biomass: {latest['biomass']:.2f} OD600"),
                ]),
                html.Div([
                    html.H4("Setpoints"),
                    html.P(f"Temp SP: {latest['temp_setpoint']:.1f} °C"),
                    html.P(f"pH SP: {latest['ph_setpoint']:.1f}"),
                    html.P(f"DO SP: {latest['do_setpoint']:.1f}%"),
                ])
            ])
        
        @self.app.callback(
            Output('temperature-plot', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_temperature_plot(n):
            df = self._load_data()
            return self._create_temperature_figure(df)
        
        @self.app.callback(
            Output('biomass-growth-plot', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_biomass_growth_plot(n):
            df = self._load_data()
            return self._create_biomass_growth_figure(df)
    
    def _load_data(self):
        """Load simulation data"""
        try:
            return pd.read_csv(f'{self.data_path}/simulation_results.csv')
        except:
            return pd.DataFrame({
                'time': [0],
                'biomass': [0],
                'temperature': [37],
                'ph': [7.2],
                'do': [30],
                'temp_setpoint': [37],
                'ph_setpoint': [7.2],
                'do_setpoint': [30]
            })
    
    def _create_biomass_figure(self, df):
        """Create biomass growth figure"""
        return {
            'data': [
                go.Scatter(
                    x=df['time'],
                    y=df['biomass'],
                    name='Biomass',
                    mode='lines',
                    line=dict(color='blue')
                )
            ],
            'layout': go.Layout(
                title='Biomass Growth',
                xaxis={'title': 'Time (h)'}
            )
        }
    
    def _create_controls_figure(self, df):
        """Create control parameters figure"""
        return {
            'data': [
                go.Scatter(
                    x=df['time'],
                    y=df['temperature'],
                    name='Temperature',
                    mode='lines',
                    line=dict(color='red')
                ),
                go.Scatter(
                    x=df['time'],
                    y=df['ph'],
                    name='pH',
                    mode='lines',
                    line=dict(color='green')
                ),
                go.Scatter(
                    x=df['time'],
                    y=df['do'],
                    name='DO',
                    mode='lines',
                    line=dict(color='purple')
                )
            ],
            'layout': go.Layout(
                title='Control Parameters',
                xaxis={'title': 'Time (h)'}
            )
        }
    
    def _create_temperature_figure(self, df):
        """Create temperature profile figure"""
        return px.line(df, x='time', y='temperature', title='Bioreactor Temperature Profile')
    
    def _create_biomass_growth_figure(self, df):
        """Create biomass growth curve figure"""
        return px.line(df, x='time', y='biomass', title='Biomass Growth Curve')
    
    def run(self, debug=True):
        """Run the dashboard server"""
        self.app.run_server(debug=debug)

if __name__ == '__main__':
    dashboard = BioreactorDashboard()
    dashboard.run()