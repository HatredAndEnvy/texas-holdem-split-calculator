# Jerry Day 5/29/2023
#
#
import math

# To do
# Add description
# I'm here: ... Set up the callback for Run the calculator.
#   1) Check all values with returned suggestions.
#   2) Calculate the expected value and variance.
# Create the plot

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
from treys import Card
from treys import Evaluator
from treys import Deck
from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

# creates the evaluator for the app.
evaluator = Evaluator()

# Playground
# deck = Deck()
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


def full_board_status_check(opp1, opp2, your1, your2, flop1, flop2, flop3, turn):
    # returns pass fail and a string that works in the message: 'The board has '+ full_board_status_check[1] + '.'
    face_up_cards = [opp1, opp2, your1, your2, flop1, flop2, flop3, turn]
    if "" in face_up_cards:
        return {'result': 'fail', 'message': 'missing cards'}
    elif len(set(face_up_cards)) != len(face_up_cards):  # If there are duplicate cards
        return {'result': 'fail', 'message': 'duplicate cards'}
    else:
        return {'result': 'pass', 'message': 'no problems'}


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
        ], style={'text-align': 'center', 'width': '40%', "border": "2px black solid"}),  # end of Opponents cards
        html.Div([
            html.H5("The Table"),
            # flop first card
            html.Div([
                html.H6('The flop'),
                dcc.Store(id='flop-first-card'),
                dcc.Dropdown(card_value_options, id='flop-first-value-dd'),
                dcc.Dropdown(card_suit_options, id='flop-first-suit-dd'),
                html.Div('--', id='flop-first-card-output')
            ], style={'width': '16%', 'display': 'inline-block'}),
            html.Div(style={'width': '2%', 'display': 'inline-block'}),
            # flop second card
            html.Div([
                dcc.Store(id='flop-second-card'),
                dcc.Dropdown(card_value_options, id='flop-second-value-dd'),
                dcc.Dropdown(card_suit_options, id='flop-second-suit-dd'),
                html.Div('--', id='flop-second-card-output')
            ], style={'width': '16%', 'display': 'inline-block'}),
            html.Div(style={'width': '2%', 'display': 'inline-block'}),
            # flop third card
            html.Div([
                dcc.Store(id='flop-third-card'),
                dcc.Dropdown(card_value_options, id='flop-third-value-dd'),
                dcc.Dropdown(card_suit_options, id='flop-third-suit-dd'),
                html.Div('--', id='flop-third-card-output')
            ], style={'width': '16%', 'display': 'inline-block'}),
            html.Div(style={'width': '4%', 'display': 'inline-block'}),
            # turn card
            html.Div([
                html.H6('The turn'),
                dcc.Store(id='turn-card'),
                dcc.Dropdown(card_value_options, id='turn-value-dd'),
                dcc.Dropdown(card_suit_options, id='turn-suit-dd'),
                html.Div('--', id='turn-card-output')
            ], style={'width': '16%', 'display': 'inline-block'}),
            html.Div(style={'width': '4%', 'display': 'inline-block'}),
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
                ], style={'align-items': 'center'}),
                html.P(id='board-status', children=['Look here for table status messages.'])
            ], style={'width': '16%', 'display': 'inline-block'})
        ], style={'padding': "2rem 0rem"}),
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
        ], style={'text-align': 'center', 'width': '40%', "border": "2px black solid"})  # end of your cards
    ], style={'width': '50%', 'display': 'inline-block'}),  # close left div
    html.Div([  # open right div
        html.Div([
            html.Div([  # the pot
                html.P("Enter the pot value between 1 and 1MM"),
                dbc.Input(id='pot-input', type='number', min=1, max=1000000, step=.01, value=100)
            ], style={'width': '45%', 'text-align': 'center', 'display': 'inline-block', 'padding': "1rem 0rem"}),
            html.Div([  # the split
                html.P("Enter the number of splits (1 means no split)"),
                dbc.Input(id='split-number-input', type='number', min=1, max=44, step=1, value=2)
            ], style={'width': '45%', 'text-align': 'center', 'display': 'inline-block', 'padding': "1rem 0rem"})
        ]),
        html.Div([html.Button('Run the Calculator', id='run-the-calculator-button')],
                 style={'width': '45%', 'text-align': 'center', 'padding': "1rem 0rem"}
                 ),
        html.Div(id='run-the-calculator-output', children=[
            html.Div([
                html.H6(['No Split Analysis']),
                html.Div(id='no-split-text-output')
                ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div([
                html.H6(id='n-split-title'),
                html.Div(id='n-split-text-output')
                ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
            dcc.Graph(id='split-analysis-graph')
        ])
    ], style={'width': '39%', 'display': 'inline-block', 'vertical-align': 'top'})  # close right div
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
     Output(component_id='river-split-second-card', component_property='data'),
     Output(component_id='board-status', component_property='children')],
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
    board_status = full_board_status_check(opp1, opp2, your1, your2, flop1, flop2, flop3, turn)
    valid_cards = (board_status['result'] == 'pass')
    board_status_message = 'The board has {}.'.format(board_status['message'])
    if ("run-it-split-button" == ctx.triggered_id) & valid_cards:
        new_deck = Deck()
        drawn_cards = new_deck.draw(10)
        # can't directly remove cards from the deck, so...
        valid_draws = [card for card in drawn_cards if card not in face_up_cards]
        if n_clicks is None:
            raise PreventUpdate
        else:
            return valid_draws[0], valid_draws[1], board_status_message
    else:
        return '', '', board_status_message


# working here          ***************************************************************************************
# add graph to output. id='split-analysis-graph' comp is a figure
@app.callback(
    [Output(component_id='no-split-text-output', component_property='children'),
     Output(component_id='n-split-title', component_property='children'),
     Output(component_id='n-split-text-output', component_property='children'),
     Output(component_id='split-analysis-graph', component_property='figure'),
     ],
    [Input(component_id='opp-first-card', component_property='data'),
     Input(component_id='opp-second-card', component_property='data'),
     Input(component_id='your-first-card', component_property='data'),
     Input(component_id='your-second-card', component_property='data'),
     Input(component_id='flop-first-card', component_property='data'),
     Input(component_id='flop-second-card', component_property='data'),
     Input(component_id='flop-third-card', component_property='data'),
     Input(component_id='turn-card', component_property='data'),
     Input(component_id='run-the-calculator-button', component_property='n_clicks'),
     Input(component_id='pot-input', component_property='value'),
     Input(component_id='split-number-input', component_property='value'),
     ],
    running=[(Output('run-the-calculator-button', 'disabled'), True, False)],
    prevent_initial_call=True
)
def run_the_calculator(opp1, opp2, your1, your2, flop1, flop2, flop3, turn, n_clicks, pot, number_of_splits):
    face_up_cards = [opp1, opp2, your1, your2, flop1, flop2, flop3, turn]
    board_status = full_board_status_check(opp1, opp2, your1, your2, flop1, flop2, flop3, turn)
    valid_cards = (board_status['result'] == 'pass')
    # board_status_message = 'The board has {}.'.format(board_status['message'])
    if n_clicks is None:
        raise PreventUpdate
    elif not (('run-the-calculator-button' == ctx.triggered_id) & valid_cards):
        return '', '', '', {}
    else:  # Cards are valid, and the calculator button has been pressed.
        new_deck = Deck()
        outcome_list = []
        for river_card in new_deck.cards:
            if river_card in face_up_cards:
                continue
            opp_hand_value = evaluator.evaluate(hand=[opp1, opp2], board=[flop1, flop2, flop3, turn, river_card])
            your_hand_value = evaluator.evaluate(hand=[your1, your2], board=[flop1, flop2, flop3, turn, river_card])
            if your_hand_value < opp_hand_value:
                outcome_list.append('w')
            elif your_hand_value == opp_hand_value:
                outcome_list.append('d')
            else:
                outcome_list.append('l')
        outcome_series = pd.Series(data=outcome_list)
        total_outcomes = len(outcome_series)
        print(total_outcomes)
        outcome_value_counts = outcome_series.value_counts()
        print(outcome_value_counts)
        unique_outcomes = len(outcome_value_counts)  # not always possible to have wins, losses and draws.
        print(unique_outcomes)
        try:
            wins = outcome_value_counts['w']
        except KeyError:
            wins = 0
        try:
            draws = outcome_value_counts['d']
        except KeyError:
            draws = 0
        try:
            loses = outcome_value_counts['l']
        except KeyError:
            loses = 0
        # no split analysis
        ns_ex = pot*(wins + 0.5*draws)/total_outcomes
        ns_var = (pot-ns_ex)**2 * wins/total_outcomes + (0.5*pot-ns_ex)**2 * draws/total_outcomes + (0-ns_ex)**2 * loses/total_outcomes
        ns_sd = math.sqrt(ns_var)
        ns_children = [html.P('Expectation: ${:.2f}'.format(ns_ex)),
                       html.P('Standard Deviation: ${:.2f}'.format(ns_sd)),
                       html.P('Variance: {:.2f}'.format(ns_var)),
                       html.P('You win {} of the {} possible rivers. You draw {} and lose {}.'.format(wins, total_outcomes, draws, loses))]
        # split analysis
        wdl_combos = [(w, d, l) for w in range(wins + 1) for d in range(draws + 1) for l in range(loses + 1) if (w + d + l == number_of_splits)]
        wdl_normalized_value_to_2 = [2*w + 1*d + 0*l for w, d, l in wdl_combos]
        wdl_probs = []
        for w, d, l in wdl_combos:
            prob_a_wdl = 1/(math.factorial(w) * math.factorial(d) * math.factorial(l) * math.comb(total_outcomes, number_of_splits)) * math.perm(wins, w) * math.perm(draws, d) * math.perm(loses, l)
            wdl_probs.append(prob_a_wdl)
        wdl_df = pd.DataFrame({'wdl_combos': wdl_combos, 'wdl_values_2': wdl_normalized_value_to_2, 'Probability': wdl_probs})
        x_table = wdl_df.groupby('wdl_values_2').Probability.agg('sum').reset_index()
        x_table['Winnings'] = pot/number_of_splits/2 * x_table.wdl_values_2
        x_mean = (x_table.Winnings * x_table.Probability).sum()
        x_table['x_mean'] = x_mean
        x_table['x_minus_mean'] = x_table.Winnings - x_mean
        x_var = (x_table['x_minus_mean']**2 * x_table['Probability']).sum()
        x_sd = math.sqrt(x_var)
        split_children = [html.P('Expectation: ${:.2f}'.format(x_mean)),
                          html.P('Standard Deviation: ${:.2f}'.format(x_sd)),
                          html.P('Variance: {:.2f}'.format(x_var))]
        fig = go.Figure(
            data=[go.Bar(name='No Split', x=[0, pot/2, pot],
                         y=[loses/total_outcomes, draws/total_outcomes, wins/total_outcomes]),
                  go.Bar(name='{} Split'.format(number_of_splits), x=x_table.Winnings, y=x_table.Probability)],
            layout=go.Layout(
                title=go.layout.Title(text="Winnings Distribution",)
            )
        )
        fig.layout.xaxis = {'title': {'text': 'Winnings'}}
        fig.layout.yaxis = {'title': {'text': 'Probability'}, 'tickformat': ",.0%"}
        # fig.layout.height = 600
        # fig.layout.width = 800
        # print(x_table)
        return ns_children, '{} Split Analysis'.format(number_of_splits), split_children, fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
