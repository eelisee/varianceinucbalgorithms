import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

# Initialisiere die Dash App
app = dash.Dash(__name__)
app.title = "Simulation of variance-aware algorithms for Stochastic Bandit Problems"

# Dateipfade der CSV-Dateien
base_path = r"C:/Users/canis/OneDrive/Dokumente/uni/uni-surface/FSS 2024/BA/bachelorarbeit_vrlfg/BA/github/BA_code/2_algorithms_results"
algorithm_data= [
    "1_ETC", "2_Greedy", "3_UCB"
]

algorithms = [
    "ETC", "Greedy", "UCB"
]
colors = [
    'blue', 'green', 'red'
]

# wenn alle fertig durchgelaufen, dann alle hinzufügen
#algorithms = [
#     "1_ETC", "2_Greedy", "3_UCB", "4_UCB-Normal", "5_UCB-V", "6_UCB-Tuned", "7_PAC-UCB", "8_UCB-Improved", "9_EUCBV"
# ]
# colors = [
#     'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple'
# ]

# Dummy-Plot Funktion
def create_dummy_plot(title):
    return dcc.Graph(
        figure={
            'data': [
                go.Scatter(x=[1, 2, 3], y=[4, 1, 2], mode='lines+markers')
            ],
            'layout': go.Layout(
                title=title,
                margin={'l': 30, 'r': 10, 'b': 30, 't': 40},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'black'}
            )
        }
    )

# Funktion zum Laden der Daten
def load_data(algorithm):
    results_path = os.path.join(base_path, f"{algorithm}_results.csv")
    average_results_path = os.path.join(base_path, f"{algorithm}_average_results.csv")

    df_results = pd.read_csv(results_path)
    df_average = pd.read_csv(average_results_path)

    return df_results, df_average

# Layout der App
app.layout = html.Div(
    style={'backgroundColor': 'white', 'color': 'black', 'font-family': 'Arial, sans-serif'},
    children=[
        html.Div(
            style={'textAlign': 'center', 'padding': '20px'},
            children=[
                html.H1("Simulation of variance-aware algorithms for Stochastic Bandit Problems")
            ]
        ),
        html.Div(
            style={'display': 'flex'},
            children=[
                # Linke Navigationsleiste
                html.Div(
                    style={'flex': '1', 'padding': '20px', 'backgroundColor': '#f0f0f0'},
                    children=[
                        html.H2("Einstellungen"),
                        html.Div(
                            children=[
                                html.Label('Verteilung der Arme'),
                                dcc.Dropdown(
                                    id='arm_distribution',
                                    options=[
                                        {'label': '2 Arme mit jeweils bernoulliverteilten Rewards mit mean [0.9, 0.8]', 'value': 'dist1'},
                                        {'label': '2 Arme mit jeweils bernoulliverteilten Rewards mit mean [0.9, 0.895]', 'value': 'dist2'},
                                        {'label': '2 Arme mit jeweils bernoulliverteilten Rewards mit mean [0.5, 0.495]', 'value': 'dist3'}
                                    ],
                                    value='dist1'
                                ),
                                html.Label('Erster Zug'),
                                dcc.Dropdown(
                                    id='first_move',
                                    options=[
                                        {'label': 'Optimaler Arm', 'value': 'optimal'},
                                        {'label': 'Anderer Arm', 'value': 'other'}
                                    ],
                                    value='optimal'
                                ),
                                html.Label('Alpha'),
                                dcc.Dropdown(
                                    id='alpha',
                                    options=[
                                        {'label': '0.01', 'value': '0.01'},
                                        {'label': '0.05', 'value': '0.05'},
                                        {'label': '0.1', 'value': '0.1'}
                                    ],
                                    value='0.01'
                                ),
                                html.Label('Algorithmus auswählen'),
                                dcc.Dropdown(
                                    id='selected_algorithm',
                                    options=[{'label': algo, 'value': algo} for algo in algorithm_data],
                                    value='3_UCB'
                                ),
                            ]
                        ),
                        html.H2("Legende"),
                        html.Ul(
                            children=[html.Li(algo, style={'color': color}) for algo, color in zip(algorithms, colors)]
                        )
                    ]
                ),
                # Rechte Seite mit Plots
                html.Div(
                    style={'flex': '4', 'padding': '20px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'flexWrap': 'wrap'},
                            children=[
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot1')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot2')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot3')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot4')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 5")]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot6')])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback zum Aktualisieren der Plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     Output('plot6', 'figure')],
    [Input('selected_algorithm', 'value')]
)
def update_plots(selected_algorithm):
    # Daten laden
    data = {}
    for algo in algorithm_data:
        data[algo] = load_data(algo)

    # Plot 1: Average Total Reward
    fig1 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig1.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Total Reward'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color)
        ))
    fig1.update_layout(title='Fig. 1: Average Total Reward over Timesteps', paper_bgcolor='white', plot_bgcolor='white', font={'color': 'black'})

    # Plot 2: Average Regret
    fig2 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig2.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Regret'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color)
        ))
    fig2.update_layout(title='Fig.2: Average Total Regret over Timesteps', paper_bgcolor='white', plot_bgcolor='white', font={'color': 'black'})

    # Plot 3: Boxplot
    fig3 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig3.add_trace(go.Box(
            y=[df['Average Zeros Count'].iloc[-1]],
            name=f'{algo} - Zeros',
            marker_color=color
        ))
        fig3.add_trace(go.Box(
            y=[df['Average Ones Count'].iloc[-1]],
            name=f'{algo} - Ones',                                                                                                                                                    # einzelne balken falschrum, nicht der richtige wert
            marker_color=color
        ))
    fig3.update_layout(title='Fig.3: Count of Zeros and Ones', paper_bgcolor='white', plot_bgcolor='white', font={'color': 'black'})

    # Plot 4: Distribution of Total Regret at Timestep 100000
    selected_data = data[selected_algorithm][0]
    df_100k = selected_data[selected_data['Timestep'] == 100000]                                                                                                                      # schleife funktiniert noch nicht
    fig4 = go.Figure(go.Histogram(x=df_100k['Total Regret'], marker_color='blue'))
    fig4.update_layout(title='Distribution of Total Regret at Timestep 100.000',  paper_bgcolor='white', plot_bgcolor='white', font={'color': 'black'}) # for chosen algorithm hinzufügen


    # Plot 5:
    # einfügen



    # Plot 6: Fraction of Suboptimal Arms Pulled
    fig6 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig6.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Suboptimal Arms'] / df['Timestep'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color)
        ))
    fig6.update_layout(title='Proportion of Suboptimal Arms pulled in comparison to all Arms pulled', paper_bgcolor='white', plot_bgcolor='white', font={'color': 'black'})

    return fig1, fig2, fig3, fig4, fig6

# Main Funktion um die App zu starten
if __name__ == '__main__':
    app.run_server(debug=True)
