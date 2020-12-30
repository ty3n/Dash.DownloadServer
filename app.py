import flask
import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from flask import send_file, send_from_directory
from dash.dependencies import Output, Input, State
from page import *
import requests
import pandas as pd
from db import *

app = dash.Dash(__name__)

_app_route = '/dash-core-components/logout_button'
app.config['suppress_callback_exceptions']=True
app.title = "MES SYSTEM"

# Create a login route
@app.server.route('/custom-auth/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')
    partnumber = data.get('partnumber')
    print(type(flask.request.remote_addr))
    if not username or not password or not partnumber:
        if username != 'admin':
            flask.abort(401)
    if not len([i for i in tb_seek() if username in i]):
        if flask.request.remote_addr != '127.0.0.1' or username != 'admin':
            flask.abort(401)
    # actual implementation should verify the password.
    # Recommended to only keep a hash in database and use something like
    # bcrypt to encrypt the password and check the hashed results.
    # Return a redirect with
    rep = flask.redirect(_app_route)
    # Here we just store the given username in a cookie.
    # Actual session cookies should be signed or use a JWT token.
    rep.set_cookie('custom-auth-session', username)
    rep.set_cookie('custom-auth-pn', partnumber)
    return rep

# create a logout route
@app.server.route('/custom-auth/logout', methods=['POST'])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect(_app_route)
    rep.set_cookie('custom-auth-session', '', expires=0)
    return rep

# Simple dash component login form.

app.layout = html.Div(id='custom-auth-frame')

def request_author_bat(partnumber):
    try:
        btnStatus = False
        # r = requests.get('http://127.0.0.1:3000/explore/repos')
        r = requests.get('http://127.0.0.1/')
        # author = [i for i in r.content.decode().split('\n') if partnumber in i][-1].strip().split('/')[0].strip()
        author='NickTest'
        f = open(os.path.join(os.getcwd(),'downloads/')+partnumber+'.bat','w')
        f.write('cd ..\n')
        f.write('cd Desktop\n')
        f.write('rmdir /S /Q {}\n'.format(partnumber))
        # f.write('git clone http://192.168.0.10:3000/{}/{}.git\n'.format(author,partnumber))
        f.write('git clone http://127.0.0.1/{}/{}.git\n'.format(author,partnumber))
        f.write('cd ..\n')
        f.write('cd Downloads/\n')
        f.write('del {}*.bat\n'.format(partnumber))
    except:
        author = 'None'
        btnStatus = True
    return author, btnStatus

@app.callback(Output('custom-auth-frame', 'children'),
              [Input('custom-auth-frame', 'id')])
def dynamic_layout(_):
    session_cookie = flask.request.cookies.get('custom-auth-session')
    partnumber = flask.request.cookies.get('custom-auth-pn')
    # get author name
    if partnumber:
        author, btnStatus = request_author_bat(partnumber)
        # print(partnumber,author,btnStatus)
    else:
        author, btnStatus = None, None
    if not session_cookie:
        # If there's no cookie we need to login.
        return loginForm(flask.request.remote_addr)
    # elif flask.request.remote_addr == '127.0.0.1' and session_cookie == 'admin':
    #     return adminForm(flask.request.remote_addr,session_cookie,partnumber,True)
    return logoutForm(flask.request.remote_addr,session_cookie,partnumber,btnStatus)

@app.callback(
    Output('download', 'href'),
    [Input('download', 'n_clicks')])
def generate_report_url(n_clicks):
    partnumber = flask.request.cookies.get('custom-auth-pn')
    return '/dash/urldownload/'+ str(partnumber)

@app.server.route('/dash/urldownload/<partnumber>')
def generate_report_url(partnumber):
    # return send_from_directory(os.path.join(os.getcwd(),'Test1'),'term.py', as_attachment = True)
    # return send_file(os.path.join(os.getcwd(),'Test1'), attachment_filename = 'example.zip', as_attachment = True)
    return send_file(os.path.join(os.getcwd(), 'downloads/')+partnumber+'.bat', as_attachment = True)

@app.callback(
    Output('admintable', 'table'),
    [Input('delete_0', 'n_clicks')],)
def generate_report_url(n_clicks):
    print(df_to_table(pd.DataFrame(tb_seek())))
    # tb_delete(int(id_.split('_')[-1])+1)
    return df_to_table(pd.DataFrame(tb_seek()))
    # return df_to_table(pd.DataFrame(tb_seek()))

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')