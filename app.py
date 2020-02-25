import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from pprint import pprint

from dash.dependencies import Input, Output, State

from func import generate_crime_entry, generate_ny_counties, parse_charges, output_answers

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


flask_server = flask.Flask(__name__)
app = dash.Dash(__name__, server=flask_server,
                url_base_pathname='/',
                external_stylesheets=external_stylesheets)
server = app.server


# app.config['suppress_callback_exceptions'] = True
# app.scripts.config.serve_locally = True

ny_counties = generate_ny_counties()


app.layout = html.Div(children=[
html.Div(children=[
    html.Div(html.H2(
        children='Closing the Second Chance Gap', style={"color":"rgb(234, 231, 220)"}), style={"text-align": "center", "background-color":"#50C878", "padding-bottom":"1px", "padding-top":"1px"}),

    html.Iframe(width="100%",height="400",style={"text-align":"center"},
    src="//cscue.maps.arcgis.com/apps/Embed/index.html?webmap=d89b5f63fedf4bb3adc332c282e09e7b&extent=-145.7934,13.2422,-42.2582,55.5797&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"),


    #tabs here
    html.Br(),
    html.Br(),
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Manual Enter', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Upload Document', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Resources', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    ], style={}),

    html.Div(children=[
        html.Br(),
        html.Div(children=[
            html.Div(children=html.P(), className="three columns"),
            html.Div(children=[
                dcc.Dropdown(id='state-dropdown',
                             options=[
                                {'label': 'New York', 'value': 'NY'},
                                {'label': 'Washington State',
                                 'value': 'WA'}
                             ],
                             placeholder='Select State...'),
                html.Br(),
                dcc.Dropdown(id='ny-county-dropdown',
                             options=ny_counties,
                             style={"display": "none"},
                             placeholder='Select County...'
                             ),
            ], className="six columns"),
            html.Div(children=html.P(), className="three columns"), ],
            className="row"
        ),


        html.Br(),

        html.Div(children=[
            html.Div(children=html.P(), className="three columns"),
            html.Div(children=[
                html.P(children='Number of crimes you\'d like to enter: ',
                       style={"display": "inline"}),
                dcc.Input(
                    type='number',
                    value=0,
                    id='crimes-committed-input',
                    min=0,
                    max=3
                ),
                html.Hr(),
                
            ], className="six columns"),
            html.Div(children=html.P(), className="three columns"), ],
            className="row"
        ),
        html.Br(),
        html.Div(id='charges-div', children=generate_crime_entry(1),
             className="row", style={"text-align": "center"}),
    ], id="manual-input", style={} ),

    



    html.Br(),
    html.Div(children=html.Button('Submit', id='submit-crimes-button',
                                  className="button-primary"), style={"text-align": "center"}),


    html.Hr(),
    html.Div(children=[
        html.H1(children="CONGRATS! You can be free now!",
                style={"text-align": "center"}, id="result"),
        html.H5(children='If your answer is YES to any of the below questions, you are not eligible for expungement.', style={'text-align':'center'}),
        html.Div(children=[
            html.Div(children=[
                html.P(
                    children="DO YOU HAVE MORE THAN TWO (2) CRIMINAL CONVICTIONS?"),
                html.P(children="DO YOU HAVE MORE THAN ONE FELONY CONVICTION?"),
                html.P(
                    children="HAVE LESS THAN TEN YEARS PASSED SINCE YOUR LAST CRIMINAL CONVICTION?"),
                html.P(children="ARE YOU REQUIRED TO REGISTER AS A SEX OFFENDER?"),
                html.P(children="ARE YOU APPLYING TO SEAL AN INELIGIBLE OFFENSE?"),
                html.P(children="DO YOU CURRENTLY HAVE AN OPEN CRIMINAL CASE?"),
            ], className="ten columns"),
            html.Div(children=[
                html.P(
                    children="√", id="criminal_convictions"),
                html.P(children="√", id="felony_conviction"),
                html.P(
                    children="X", id="ten_years_period"),
                html.P(children="√", id="sex_offender"),
                html.P(children="√", id="ineligible_offense"),
                html.P(children="√", id="open_criminal_case"),
            ], className="two columns", style={"text-align": "right"}),
        ], className="row"),
    ], id="eligibility_info", style={'display': 'none'}),

], className="container"),


], style={"background-color":"rgb(234, 231, 220, 0.5)", "width":"100%", "margin":"0px"})


@app.callback(Output('charges-div', 'children'),
              [Input('crimes-committed-input', 'value')])
def generate_case_entry_div(value):
    return generate_crime_entry(value)

#for the tabs 
@app.callback(Output('manual-input', 'style'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):
    if (tab == "tab-2" or tab == "tab-3"):
        return {"display":"none"}   
    return {}


@app.callback(Output('ny-county-dropdown', 'style'),
              [Input('state-dropdown', 'value')])
def update_output_component(dropdown_value):
    if dropdown_value == 'NY':
        return {}
    else:
        return {'display': 'none'}

@app.callback([Output('criminal_convictions', 'children'),
               Output('felony_conviction', 'children'),
               Output('ten_years_period', 'children'),
               Output('sex_offender', 'children'),
               Output('ineligible_offense', 'children'),
               Output('open_criminal_case', 'children'),
               Output('result', 'children'),
               Output('eligibility_info', 'style')],
              [Input('submit-crimes-button', 'n_clicks')],
              [State('charges-div', 'children')])

def update_crimes_store(n, charges):
    if n is not None and n >= 1:
        eligible_list, eligible = parse_charges(charges)
        ret = [0, 0, 0, 0, 0, 0]
        return_message = ''
        ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], return_message = output_answers(
            eligible_list, eligible)
        print('Test Output')
        pprint(ret)
        pprint(return_message)
        return ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], return_message, {}
    return "","","","","", "","", {'display':'none'}


if __name__ == '__main__':
    flask_server.run(debug=True)
