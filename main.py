# Jerry Day 5/29/2023
#
#

# To do
# Add description
# I'm here: ... Set up the callback for Run the calculator.
#   1) Check all values with returned suggestions.
#   2) Calculate the expected value and variance.
# Create the plot

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from treys import Card
# from treys import Evaluator
from treys import Deck
from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
# Playground
deck = Deck()
# a_card = deck.draw()
# Card.print_pretty_cards(a_card)
# print(Card.ints_to_pretty_str(a_card))
# print(type(Card.ints_to_pretty_str(a_card)))
# print(Card.new('Th'))
# print(Card.new('9h'))
# end playground

# creating options for card dropdowns
card_value_dict = {'Ace': 'A', 'King': 'K', 'Queen': 'Q', 'Jack': 'J', '10': 'T'}
card_value_dict.update({str(i): str(i) for i in range(9, 1, -1)})
card_value_options = [{'label': key, 'value': value} for (key, value) in card_value_dict.items()]

card_suit_dict = {'Spades': 's', 'Diamonds': 'd', 'Clubs': 'c', 'Hearts': 'h'}
card_suit_options = [{'label': key, 'value': value} for (key, value) in card_suit_dict.items()]


def update_card(card_value, card_suit):
    the_card = ''
    if card_value is not None and card_suit is not None:
        the_card = Card.new(card_value + card_suit)
    return the_card


def update_card_output(the_card):
    the_card_str = '--'
    if the_card is not None and the_card != '':
        the_card_str = Card.ints_to_pretty_str([the_card])
    return the_card_str


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([html.H3("Texas Holdem")], className='header'),
    html.Div([html.H4("Split Calculator")], className='header'),
    html.Hr(),
    html.P("Explanation goes here."),
    # note for feedback / errors maybe
    # html.P("", id = 'note'),
    # html.Button('Reset Calculator (disabled)', id='reset-button'),
    html.Div([  # open left div
        html.Div(html.Button('Deal new cards', id='randomizer-button'), style={'padding': "1rem 0rem"}),
        html.Br(),
        # opponent's cards
        html.Div([
            html.H5("Opponent's Cards"),
            # opponent's first card
            html.Div([
                dcc.Store(id='opp-first-card'),
                dcc.Dropdown(card_value_options, id='opp-first-value-dd'),
                dcc.Dropdown(card_suit_options, id='opp-first-suit-dd'),
                html.Div('--', id='opp-first-card-output')
            ], style={'width': '40%', 'display': 'inline-block'}),
            html.Div(style={'width': '5%', 'display': 'inline-block'}),
            # opponent's second card
            html.Div([
                dcc.Store(id='opp-second-card'),
                dcc.Dropdown(card_value_options, id='opp-second-value-dd'),
                dcc.Dropdown(card_suit_options, id='opp-second-suit-dd'),
                html.Div('--', id='opp-second-card-output')
            ], style={'width': '40%', 'display': 'inline-block'})
        ], style={'text-align': 'center', 'width': '33.3%', "border": "2px black solid"}),  # end of Opponents cards
        html.Div([
            html.H5("The Table"),
            # flop first card
            html.Div([
                html.H6('The flop'),
                dcc.Store(id='flop-first-card'),
                dcc.Dropdown(card_value_options, id='flop-first-value-dd'),
                dcc.Dropdown(card_suit_options, id='flop-first-suit-dd'),
                html.Div('--', id='flop-first-card-output')
            ], style={'width': '13.3%', 'display': 'inline-block'}),
            html.Div(style={'width': '1.6%', 'display': 'inline-block'}),
            # flop second card
            html.Div([
                dcc.Store(id='flop-second-card'),
                dcc.Dropdown(card_value_options, id='flop-second-value-dd'),
                dcc.Dropdown(card_suit_options, id='flop-second-suit-dd'),
                html.Div('--', id='flop-second-card-output')
            ], style={'width': '13.3%', 'display': 'inline-block'}),
            html.Div(style={'width': '1.6%', 'display': 'inline-block'}),
            # flop third card
            html.Div([
                dcc.Store(id='flop-third-card'),
                dcc.Dropdown(card_value_options, id='flop-third-value-dd'),
                dcc.Dropdown(card_suit_options, id='flop-third-suit-dd'),
                html.Div('--', id='flop-third-card-output')
            ], style={'width': '13.3%', 'display': 'inline-block'}),
            html.Div(style={'width': '3.3%', 'display': 'inline-block'}),
            # turn card
            html.Div([
                html.H6('The turn'),
                dcc.Store(id='turn-card'),
                dcc.Dropdown(card_value_options, id='turn-value-dd'),
                dcc.Dropdown(card_suit_options, id='turn-suit-dd'),
                html.Div('--', id='turn-card-output')
            ], style={'width': '13.3%', 'display': 'inline-block'}),
            html.Div(style={'width': '3.3%', 'display': 'inline-block'}),
            # river cards...
            html.Div([
                html.Button('Run it split', id='run-it-split-button'),
                # river split first card
                html.Div([
                    html.H6('The first split'),
                    dcc.Store(id='river-split-first-card'),
                    html.Div('--', id='river-split-first-card-output')
                ]),
                # river split second card
                html.Div([
                    html.H6('The second split'),
                    dcc.Store(id='river-split-second-card'),
                    html.Div('--', id='river-split-second-card-output')
                ], style={'align-items': 'center'})
            ], style={'width': '13.3%', 'display': 'inline-block'})
        ], style={'padding': "2rem 0rem"}),  # end of table cards ... 'text-align':'center', 'width': '100%', "border":"2px black solid",
        html.Div([
            html.H5("Your Cards"),
            # your first card
            html.Div([
                dcc.Store(id='your-first-card'),
                dcc.Dropdown(card_value_options, id='your-first-value-dd'),
                dcc.Dropdown(card_suit_options, id='your-first-suit-dd'),
                html.Div('--', id='your-first-card-output')
            ], style={'width': '40%', 'display': 'inline-block'}),
            html.Div(style={'width': '5%', 'display': 'inline-block'}),
            # your second card
            html.Div([
                dcc.Store(id='your-second-card'),
                dcc.Dropdown(card_value_options, id='your-second-value-dd'),
                dcc.Dropdown(card_suit_options, id='your-second-suit-dd'),
                html.Div('--', id='your-second-card-output')
            ], style={'width': '40%', 'display': 'inline-block'})
        ], style={'text-align': 'center', 'width': '33.3%', "border": "2px black solid"})  # end of your cards
    ], style={'width': '60%', 'display': 'inline-block'}),  # close left div
    html.Div([  # open right div
        html.Div([  # the pot
            html.P("Enter the pot value between 1 and 1MM"),
            dbc.Input(type='number', min=1, max=1000000, step=.01, value=100)
        ], style={"border": "2px black solid"}),
        html.Div([  # the split
            html.P("Enter the number of splits (1 means no split)"),
            dbc.Input(type='number', min=1, max=10, step=1, value=2)
        ], style={"border": "2px black solid"}),
        html.Button('Run the Calculator', id='run-the-calculator-button'),
        html.Div(id='run-the-calculator-output')
    ], style={'display': 'inline-block', "border": "2px black solid", 'vertical-align': 'top'})  # close right div
])


@app.callback(
    [Output(component_id='opp-first-card', component_property='data', allow_duplicate=True),
     Output(component_id='opp-second-card', component_property='data', allow_duplicate=True),
     Output(component_id='your-first-card', component_property='data', allow_duplicate=True),
     Output(component_id='your-second-card', component_property='data', allow_duplicate=True),
     Output(component_id='flop-first-card', component_property='data', allow_duplicate=True),
     Output(component_id='flop-second-card', component_property='data', allow_duplicate=True),
     Output(component_id='flop-third-card', component_property='data', allow_duplicate=True),
     Output(component_id='turn-card', component_property='data', allow_duplicate=True)],
    Input(component_id='randomizer-button', component_property='n_clicks'),
    prevent_initial_call=True
)
def deal_cards(n_clicks):
    new_deck = Deck()
    if n_clicks is None:
        raise PreventUpdate
    else:
        return new_deck.draw(8)


@app.callback(
    Output(component_id='opp-first-card', component_property='data'),
    [Input(component_id='opp-first-value-dd', component_property='value'),
     Input(component_id='opp-first-suit-dd', component_property='value')]
)
def update_opp_first_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='opp-first-card-output', component_property='children'),
    Input(component_id='opp-first-card', component_property='data')
)
def update_opp_first_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='opp-second-card', component_property='data'),
    [Input(component_id='opp-second-value-dd', component_property='value'),
     Input(component_id='opp-second-suit-dd', component_property='value')]
)
def update_opp_second_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='opp-second-card-output', component_property='children'),
    Input(component_id='opp-second-card', component_property='data')
)
def update_opp_second_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='your-first-card', component_property='data'),
    [Input(component_id='your-first-value-dd', component_property='value'),
     Input(component_id='your-first-suit-dd', component_property='value')]
)
def update_your_first_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='your-first-card-output', component_property='children'),
    Input(component_id='your-first-card', component_property='data')
)
def update_your_first_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='your-second-card', component_property='data'),
    [Input(component_id='your-second-value-dd', component_property='value'),
     Input(component_id='your-second-suit-dd', component_property='value')]
)
def update_your_second_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='your-second-card-output', component_property='children'),
    Input(component_id='your-second-card', component_property='data')
)
def update_your_second_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='flop-first-card', component_property='data'),
    [Input(component_id='flop-first-value-dd', component_property='value'),
     Input(component_id='flop-first-suit-dd', component_property='value')]
)
def update_flop_first_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='flop-first-card-output', component_property='children'),
    Input(component_id='flop-first-card', component_property='data')
)
def update_flop_first_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='flop-second-card', component_property='data'),
    [Input(component_id='flop-second-value-dd', component_property='value'),
     Input(component_id='flop-second-suit-dd', component_property='value')]
)
def update_flop_second_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='flop-second-card-output', component_property='children'),
    Input(component_id='flop-second-card', component_property='data')
)
def update_flop_second_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='flop-third-card', component_property='data'),
    [Input(component_id='flop-third-value-dd', component_property='value'),
     Input(component_id='flop-third-suit-dd', component_property='value')]
)
def update_flop_third_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='flop-third-card-output', component_property='children'),
    Input(component_id='flop-third-card', component_property='data')
)
def update_flop_third_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='turn-card', component_property='data'),
    [Input(component_id='turn-value-dd', component_property='value'),
     Input(component_id='turn-suit-dd', component_property='value')]
)
def update_turn_card(card_value, card_suit):
    return update_card(card_value, card_suit)


@app.callback(
    Output(component_id='turn-card-output', component_property='children'),
    Input(component_id='turn-card', component_property='data')
)
def update_turn_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='river-split-first-card-output', component_property='children'),
    Input(component_id='river-split-first-card', component_property='data')
)
def update_river_split_first_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    Output(component_id='river-split-second-card-output', component_property='children'),
    Input(component_id='river-split-second-card', component_property='data')
)
def update_river_split_second_card_output(the_card):
    return update_card_output(the_card)


@app.callback(
    [Output(component_id='river-split-first-card', component_property='data'),
     Output(component_id='river-split-second-card', component_property='data')],
    [Input(component_id='opp-first-card', component_property='data'),
     Input(component_id='opp-second-card', component_property='data'),
     Input(component_id='your-first-card', component_property='data'),
     Input(component_id='your-second-card', component_property='data'),
     Input(component_id='flop-first-card', component_property='data'),
     Input(component_id='flop-second-card', component_property='data'),
     Input(component_id='flop-third-card', component_property='data'),
     Input(component_id='turn-card', component_property='data'),
     Input(component_id='run-it-split-button', component_property='n_clicks')],
    prevent_initial_call=True
)
def run_it_split(opp1, opp2, your1, your2, flop1, flop2, flop3, turn, n_clicks):
    face_up_cards = [opp1, opp2, your1, your2, flop1, flop2, flop3, turn]
    valid_cards = "" not in face_up_cards
    if ("run-it-split-button" == ctx.triggered_id) & valid_cards:  # still misses the case where a card is face up twice
        new_deck = Deck()
        drawn_cards = new_deck.draw(10)
        # can't directly remove cards from the deck, so...
        valid_draws = [card for card in drawn_cards if card not in face_up_cards]
        if n_clicks is None:
            raise PreventUpdate
        else:
            return valid_draws[0], valid_draws[1]
    else:
        return '', ''


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)