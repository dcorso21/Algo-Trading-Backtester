from local_functions.main import global_vars as gl


def reset_variables():
    '''
    ## Reset Variables
    There are many global variables that are used throughout the algorithm, 
    and this file resets them so you can easily run the algo back to back. 
    '''

    csv_indexes = []

    gl.pos_update = False
    gl.loop_feedback = True
    gl.buy_lock = False
    gl.sell_out = False
    gl.chart_response = False

    gl.current_frame = gl.pd.DataFrame()
    gl.daily_ohlc = gl.pd.DataFrame()
    gl.open_orders = gl.pd.DataFrame()
    gl.current_positions = gl.pd.DataFrame()
    gl.filled_orders = gl.pd.DataFrame()
    gl.mom_frame = gl.pd.DataFrame()
    gl.sup_res_frame = gl.pd.DataFrame()

    # PL and Exposure
    gl.sys.dont_write_bytecode = True

    pl_ex = {
        'unreal': 0,
        'real': 0,
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
        'current': 'nan',
        'three_min': 'nan',
        'five_min': 'nan',
        'ten_min': 'nan',
        'mean': 'nan'
    }

    gl.volas = volas

    # mom_frame

    # Logging Notes
    df = gl.pd.DataFrame()
    headers = gl.pd.Series(
        ['minute', 'second', 'message', 'core', 'file', 'function', 'line'])

    df = df.append(headers, ignore_index=True)
    df = df.set_index(0)
    df.to_csv('temp_assets/log.csv', header=False)

    print('variables reset')
