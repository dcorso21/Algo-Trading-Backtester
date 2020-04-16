from local_functions.main import global_vars as gl


# 3 % gain... sell all
def percentage_gain():
    '''
    ## Percentage Gain
    ### Sell Condition
    If the current price is a certain percentage over the average, then sell EVERYTHING. 

    Returns a Sells DataFrame

    #### Note: 
    If the condition is not met, this returns a blank DF. 
    '''
    avg = gl.common_ana.get_average()
    if gl.current['close'] > (avg * 1.03):
        # sell all
        everything = gl.current_positions.qty.sum()
        cancel_spec = gl.o_tools.cancel_specs['standard']
        exe_price = gl.o_tools.bid_price()
        sells = gl.o_tools.create_sells(
            everything, exe_price, cancel_spec)
        gl.log_funcs.log('----> over 3 perc gain triggered. ')
        return sells
    sells = gl.pd.DataFrame()
    return sells


def target_unreal():
    '''
    ## Target Unreal
    ### Sell Condition
    If the amount in unreal is above a specified target, sell EVERYTHING. 

    Returns a Sells DataFrame

    #### Note: 
    If the condition is not met, this returns a blank DF. 
    '''
    target_int = 200
    unreal = gl.pl_ex['unreal']
    if unreal > target_int:
        # sell all
        everything = gl.current_positions.qty.sum()
        exe_price = gl.o_tools.bid_price()
        cancel_spec = gl.o_tools.cancel_specs['standard']
        sells = gl.o_tools.create_sells(everything, exe_price, cancel_spec)
        gl.log_funcs.log(f'----> unreal hits trigger: {unreal}')
        return sells

    sells = gl.pd.DataFrame()
    return sells


# if exposure is over 30K... sell half
def exposure_over_account_limit():
    '''
    ## Exposure over Account Limit
    ### Sell Condition
    If the amount owned in shares is more than I can afford, immediately sell HALF. 

    Returns a Sells DataFrame

    #### Note: 
    If the condition is not met, this returns a blank DF. 
    '''
    available_capital = gl.account.get_available_capital()
    exposure = gl.pl_ex['last_ex']
    if exposure > available_capital:
        half = int(gl.current_positions.qty.sum()/2)
        exe_price = gl.o_tools.bid_price()
        cancel_spec = gl.o_tools.cancel_specs['standard']
        sells = gl.o_tools.create_sells(half, exe_price, cancel_spec)
        gl.log_funcs.log('----> over-exposed sell half.')
    else:
        sells = gl.pd.DataFrame()
    return sells


def eleven_oclock_exit():
    '''
    ## Eleven O'Clock Exit
    ### Sell Condition
    If the current minute is 11:00:00, then sell EVERYTHING. 

    Returns a Sells DataFrame

    #### Note: 
    If the condition is not met, this returns a blank DF. 
    '''
    current = gl.current

    if (current['minute'] == '11:00:00') or (gl.sell_out == True):
        everything = gl.current_positions.qty.sum()
        exe_price = gl.o_tools.extrapolate_exe_price()
        avg = gl.common_ana.get_average()
        price = gl.current['close']
        if (exe_price < avg) and (price > avg):
            exe_price = avg
        cancel_spec = gl.o_tools.cancel_specs['standard']
        sells = gl.o_tools.create_sells(everything, exe_price, cancel_spec)
        gl.log_funcs.log('Sell to Stop...')
        gl.buy_lock = True
        gl.sell_out = True
    else:
        sells = gl.pd.DataFrame()
    return sells
