from local_functions.analyse import order_eval
from local_functions.main import global_vars as gl


def reset_variables(mode, csv_file):
    '''
    ## Reset Variables
    There are many global variables that are used throughout the algorithm, 
    and this file resets them so you can easily run the algo back to back. 
    '''

    def get_sim_df(csv_file):
        m = gl.pd.read_csv(csv_file)
        m['open'] = m.open.astype(float)
        m['high'] = m.high.astype(float)
        m['low'] = m.low.astype(float)
        m['close'] = m.close.astype(float)
        m['volume'] = m.volume.astype(float).astype(int)
        # Re-Order
        m = m[['ticker', 'time', 'open', 'high', 'low', 'close', 'volume']]
        return m

    if mode == 'csv':
        gl.csv_indexes = []
        gl.sim_df = get_sim_df(csv_file)

    gl.order_count = 0

    gl.pos_update = False
    gl.loop_feedback = True
    gl.buy_lock = False
    gl.sell_out = False
    gl.chart_response = False

    gl.order_specs = gl.pd.DataFrame()
    gl.queued_orders = gl.pd.DataFrame()
    gl.open_orders = gl.pd.DataFrame()
    gl.cancelled_orders = gl.pd.DataFrame()
    gl.current_positions = gl.pd.DataFrame()
    gl.filled_orders = gl.pd.DataFrame()
    gl.current_frame = gl.pd.DataFrame()
    gl.mom_frame = gl.pd.DataFrame()
    gl.sup_res_frame = gl.pd.DataFrame()
    gl.log = gl.pd.DataFrame()

    # PL and Exposure
    gl.sys.dont_write_bytecode = True

    pl_ex = {
        'unreal': 0,
        'min_unreal': 0,
        'max_unreal': 0,
        'real': 0,
        'min_real': 0,
        'max_real': 0,
        'last_ex': 0,
        'max_ex': 0
    }

    gl.pl_ex = pl_ex

    # current
    current = {
        'open': 'nan',
        'high': 'nan',
        'low': 'nan',
        'close': 'nan',
        'volume': 'nan',
        'second': 'nan',
        'minute': 'nan',
        'ticker': 'nan'
    }

    # last_current
    last = {
        'open': 'nan',
        'high': 'nan',
        'low': 'nan',
        'close': 'nan',
        'volume': 'nan',
        'second': 'nan',
        'minute': 'nan',
        'ticker': 'nan'
    }

    gl.current = current
    gl.last = last

    # volas
    volas = {
        'differential': 'nan',
        'current': 'nan',
        'three_min': 'nan',
        'five_min': 'nan',
        'ten_min': 'nan',
        'mean': 'nan'
    }

    gl.volas = volas
    # volumes
    volumes = {
        'safe_capital_limit': 'nan',
        'differential': 'nan',
        'mean': 'nan',
        'minimum': 'nan',
        'extrap_current': 'nan',
        'three_min_mean': 'nan',
        'three_min_min': 'nan',
        'five_min_mean': 'nan',
        'five_min_min': 'nan',
        'ten_min_mean': 'nan',
        'ten_min_min': 'nan',
    }

    gl.volumes = volumes

    # Logging Notes
    # Log is now managed in global vars and log_funcs

    # Logging Efficiency
    df = gl.pd.DataFrame()
    headers = gl.pd.Series(
        ['minute', 'second', 'function', 'run_time'])

    df = df.append(headers, ignore_index=True)
    df = df.set_index(0)
    df.to_csv(gl.filepath['efficiency_log'], header=False)

    print('variables reset')


def master_configure(mode, csv_file):
    reset_variables(mode, csv_file)
    set_buy_conditions()
    set_sell_conditions()
    print('settings configured')


'''----- ORDER CONDITIONS -----'''
# region Default Params for Sell Conditions
sc = order_eval.sell_conditions
# region Percentage Gain

# sc.percentage_gain
percentage_gain = True
percentage_gain_params = {
    'perc_gain': 3
}
# endregion Percentage Gain

# region Target Unreal
# sc.target_unreal
target_unreal = True
target_unreal_params = {
    'target_unreal': 20
}
# endregion Target Unreal

# region Exposure Over Account Limit
# sc.exposure_over_account_limit
exposure_over_account_limit = True
exposure_over_account_limit_params = {}

# endregion Exposure Over Account Limit

# region Timed Exit

# sc.timed_exit
timed_exit = True
timed_exit_params = {
    'time': '11:00:00',
}
# endregion Timed Exit

sell_cond_priority = {
    percentage_gain: (1, 'percentage_gain'),
    target_unreal: (2, 'target_unreal'),
    exposure_over_account_limit: (3, 'exposure_over_account_limit'),
    timed_exit: (4, 'timed_exit'),
}

sell_conditions = []

# endregion Default Params for Sell Conditions


# region Default Params for Buy Conditions

# region aggressive average
# bc.aggresive_average
aggresive_average = True
aggresive_average_params = {}

# endregion aggressive average

# region drop below average
# bc.drop_below_average
drop_below_average = True
drop_below_average_params = {}

# endregion drop below average

buy_cond_priority = {
    aggresive_average: (1, 'aggresive_average'),
    drop_below_average: (2, 'drop_below_average'),
}

buy_conditions = []

# endregion Default Params for Buy Conditions


def set_sell_conditions():
    global sell_conditions

    in_use = []
    for condition in sell_cond_priority.keys():
        if condition == True:
            in_use.append(sell_cond_priority[condition])

    sell_conditions = []
    for entry in sorted(in_use):
        sell_conditions.append(entry[1])


def set_buy_conditions():
    global buy_conditions

    in_use = []
    for condition in buy_cond_priority.keys():
        if condition == True:
            in_use.append(buy_cond_priority[condition])

    buy_conditions = []
    for entry in sorted(in_use):
        buy_conditions.append(entry[1])


'''----- OTHER -----'''
ideal_volatility = 3