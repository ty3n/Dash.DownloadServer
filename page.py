import flask
import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from flask import send_file, send_from_directory
from dash.dependencies import Output, Input
import dash_table
from app import app
from db import *
import pandas as pd

def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        
        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]+[html.Td(
                    html.B(
                        children='Delete{}'.format(i),
                        id='delete_{}'.format(i),
                        # download = "example.zip",
                        hidden = False,
                        # href="",
                        # target="_blank",
                        n_clicks = 0
                    ),
                )]
            )
            for i in range(len(df))
        ],
        id="table-element",
        className="table__container",
    )

def loginForm(address):
    return html.Div([
        html.Div(
            [html.Img(src=app.get_asset_url("hitron_logo.jpg"))], className="app__banner"
        ),
                html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "HITRON PTD&FACTORY MES SYSTEM",
                                        className="uppercase title",
                                    ),
                                    html.Span(address+' ', className="uppercase bold"),
                                    html.Span(
                                        "over MES SYSTEM, login by typing your account."
                                    ),
                                    html.Br(),
                                    html.Span("Create ", className="uppercase bold"),
                                    html.Span(
                                        "a account, please contact with SYSTEM MANAGER Nick, Ron, Jamens."
                                    ),
                                ]
                            )
                        ],
                        className="app__header",
                    ),
                    html.Div(
                        [
                            html.Form([
                                html.Span('Login as:', className="bold"),
                                html.Br(),
                                dcc.Input(placeholder='username', name='username', type='text'),
                                html.Br(),
                                html.Span('Password:', className="bold"),
                                html.Br(),
                                dcc.Input(placeholder='password', name='password', type='password'),
                                html.Br(),
                                html.Span('Part Number:', className="bold"),
                                html.Br(),
                                dcc.Input(placeholder='partnumber', name='partnumber', type='text'),
                                html.Br(),
                                html.Br(),
                                html.Button('Login', type='submit'),
                            ], action='/custom-auth/login', method='post',className="app__container_left"),          
                        ],
                        className="container_login card app__content bg-white",
                    ),
                ],
                className="app__container",
            ),
    ])

def logoutForm(address,session_cookie,partnumber,btnStatus):
    return html.Div([
        html.Div(
            [html.Img(src=app.get_asset_url("hitron_logo.jpg"))], className="app__banner"
        ),
                html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "HITRON PTD&FACTORY MES SYSTEM",
                                        className="uppercase title",
                                    ),
                                    html.Span(address+' ', className="uppercase bold"),
                                    html.Span(
                                        "over MES SYSTEM, login by typing your account."
                                    ),
                                    html.Br(),
                                    html.Span("Create ", className="uppercase bold"),
                                    html.Span(
                                        "a account, please contact with SYSTEM MANAGER Nick, Ron, Jamens."
                                    ),
                                ]
                            )
                        ],
                        className="app__header",
                    ),
                    html.Div(
                        [
                            html.Form([
                                html.Button('Logout', type='submit')
                            ], action='/custom-auth/logout', method='post')
                        ],
                        className="container card app__content bg-white",
                    ),
                    html.Div(
                        [
                            html.Table(
                                [html.Tr([html.Th('User'),html.Th('Part Number'),html.Th('URL')])]+ 
                                [html.Tr([
                                    html.Td([session_cookie]),
                                    html.Td([partnumber]),
                                    html.Td(
                                        html.A(
                                            'Download',
                                            id='download',
                                            download = "example.zip",
                                            hidden = btnStatus,
                                            href="",
                                            target="_blank",
                                            n_clicks = 0
                                        ),
                                    ),
                                ]),
                            ],
                            id="table-element",
                            className="table__container",
                            ),
                        ],
                        className="container bg-white p-0",
                    ),
                ],
                className="app__container",
            ),
    ])

def adminForm(address,session_cookie,partnumber,btnStatus):
    return html.Div([
        html.Div(
            [html.Img(src=app.get_asset_url("hitron_logo.jpg"))], className="app__banner"
        ),
            html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "HITRON PTD&FACTORY MES SYSTEM",
                                    className="uppercase title",
                                ),
                                html.Span(address+' ', className="uppercase bold"),
                                html.Span(
                                    "over MES SYSTEM, login by typing your account."
                                ),
                                html.Br(),
                                html.Span("Create ", className="uppercase bold"),
                                html.Span(
                                    "a account, please contact with SYSTEM MANAGER Administrator."
                                ),
                            ]
                        )
                    ],
                    className="app__header",
                ),
                html.Div(
                    [
                        html.Form([
                            html.Button('Logout', type='submit')
                        ], action='/custom-auth/logout', method='post')
                    ],
                    className="container card app__content bg-white",
                ),
                html.Div(
                    [
                        df_to_table(pd.DataFrame(tb_seek()))
                        # html.Table(
                        #     [html.Tr([html.Th('User'),html.Th('Part Number'),html.Th('URL')])]+ 
                        #     [html.Tr([
                        #         html.Td([1,2,3]),
                        #         html.Td([4,5,6]),
                        #         html.Td([7,8,9]),
                        #     ]),
                        # ]+[html.Tr([
                        #         html.Td([1,2,3]),
                        #         html.Td([4,5,6]),
                        #         html.Td([7,8,9]),
                        #     ]),
                        # ],
                        # id="table-element",
                        # className="table__container",
                        # ),
                        # dash_table.DataTable(
                        #     id='dataTable',
                        #     columns=[{'id':'Model','name':'Model'},{'id':'Hello','name':'222333'},{'id':'QQQ','name':'fwefwef'}],
                        #     data=[{'Model':'1','Hello':'2','QQQ':'3'},{'Model':'1','Hello':'2','QQQ':'3'},{'Model':'1','Hello':'2','QQQ':'3'}]
                        # )
                    ],
                    className="container bg-white p-0",
                    id="admintable",
                ),
            ],
            className="app__container",
        ),
    ])
