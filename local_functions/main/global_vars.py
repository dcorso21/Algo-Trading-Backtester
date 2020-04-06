# Modules
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui


import datetime
import pandas as pd
import logging
import random
import os
import sys
import requests


# Imports - list follows folders
from local_functions.account_info import account_info as account

from local_functions.analysis import analyse as ana
from local_functions.analysis import common_ana

# Daily Analysis
from local_functions.analysis.ana_indicators import daily_ana
from local_functions.analysis.ana_indicators.d_eval import d_price_eval, d_update_docs
from local_functions.analysis.ana_indicators.d_eval.manage_docs import momentum as mom
from local_functions.analysis.ana_indicators.d_eval.manage_docs import supports_resistances as sup_res
from local_functions.analysis.ana_indicators.d_eval.manage_docs import volas as vf

# Position Analysis
from local_functions.analysis.ana_indicators import position_ana
from local_functions.analysis.ana_indicators.p_eval import p_buy_eval, p_sell_eval
from local_functions.analysis.ana_indicators.p_eval import order_tools as o_tools
from local_functions.analysis.ana_indicators.p_eval.conditions import buy_conditions as b_conds
from local_functions.analysis.ana_indicators.p_eval.conditions import sell_conditions as s_conds

# Other
from local_functions.assemble_data import gather_data as gather
from local_functions.assemble_data import stock_screening as screen
from local_functions.main import algo
from local_functions.main import log_funcs
from local_functions.pull_historical import historical_funcs as hist
from local_functions.reset_temp_files import reset_temp_files as reset

from local_functions.trade_funcs import sim_executions as sim_exe
from local_functions.trade_funcs import trade_funcs

from local_functions.live_graph import candles as candles
from local_functions.td_api import api_chart


pos_update = False
loop_feedback = True
buy_lock = False
sell_out = False
chart_response = False


# Sim Data
# only need to reference this once.
sim_df = hist.get_mkt_data(r'example.csv')
csv_indexes = {}
minute_prices = []
minute_volumes = []

# All assets start as blank.


current_frame = pd.DataFrame()
daily_ohlc = pd.DataFrame()
open_orders = pd.DataFrame()
current_positions = pd.DataFrame()
filled_orders = pd.DataFrame()
mom_frame = pd.DataFrame()
sup_res_frame = pd.DataFrame()

current = {}
last = {}
pl_ex = {}
volas = {}


def csv_to_dict(file_path):
    df = pd.read_csv(file_path)
    df = df.set_index('type')
    df = df[['value']]
    dictionary = df.to_dict()['value']
    return dictionary


def save_dict_to_csv(dictionary, file_name):
    df = pd.DataFrame(dictionary, index=['value']).T
    df = df.reset_index().rename(columns={'index': 'type'})
    save_frame(df, file_name)


def save_frame(dataframe, file_name):
    dataframe.to_csv(filepath[file_name])


filepath = {

    'current': r'temp_assets\current.csv',
    'pl_ex': r'temp_assets\pl_and_ex.csv',
    'current_frame': r'temp_assets\charts\current_frame.csv',
    'daily_ohlc': r'temp_assets\charts\daily.csv',
    'mom_frame': r'temp_assets\analysis\mom_frame.csv',
    'sup_res_frame': r'temp_assets\analysis\supports_resistances.csv',
    'volas': r'temp_assets\analysis\volas.csv',
    'current_positions': r'temp_assets\all_orders\current_positions.csv',
    'filled_orders': r'temp_assets\all_orders\filled_orders.csv',
    'open_orders': r'temp_assets\all_orders\open_orders.csv'

}


def save_all():
    '''
    ### Save All Files
    Once trading is done, save all global variables as csv files. 
    '''
    files = {

        'current': current,
        'pl_ex': pl_ex,
        'current_frame': current_frame,
        'mom_frame': mom_frame,
        'sup_res_frame': sup_res_frame,
        'volas': volas,
        'current_positions': current_positions,
        'filled_orders': filled_orders,
        'open_orders': open_orders

    }

    for file_name, file in zip(files.keys(), files.values()):

        if type(file) == dict:
            save_dict_to_csv(file, file_name)
        else:
            save_frame(file, file_name)


def get_vars():
    return current, pl_ex, current_frame, mom_frame, sup_res_frame, volas, current_positions, filled_orders, open_orders


def log(msg='', line_break=False):

    brk = ''
    if line_break == True:
        brk = '\n'

    sec = current['second']
    func_name = sys._getframe(1).f_code.co_name

    line_number = sys._getframe(1).f_lineno
    file_name = sys._getframe(1).f_code.co_filename
    # func_name = "r'{}'".format(func_name)
    file_name = file_name.split('\\')[-1]

    new_line = f'{sec}/ {msg}/ {file_name}/ {func_name}/ {line_number}/ {brk}'
    logging.info(new_line)


def log(msg=''):
    minute = current['minute']
    sec = current['second']
    func_name = sys._getframe(1).f_code.co_name
    line_number = sys._getframe(1).f_lineno
    file_name = sys._getframe(1).f_code.co_filename
    file_name = file_name.split('\\')[-1]

    new_row = {

        'minute': [minute],
        'second': [sec],
        'message': [msg],
        'file': [file_name],
        'function': [func_name],
        'line': [line_number],

    }

    df = pd.DataFrame(new_row)
