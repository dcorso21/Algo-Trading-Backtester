# LOCAL FUNCTIONS #############
from local_functions.main import global_vars as gl
import time


def test_trade(mode='csv', csv_file='first', batch_path=False):

    start_time = time.time()
    gl.controls.master_configure(
        mode=mode, csv_file=csv_file, batch_path=batch_path)

    gl.screen.pick_stock_direct(mode)
    if gl.stock_pick == 'nan':
        return

    while True:

        gl.gather.update_direct()          # Updates Info...
        orders = gl.analyse.analyse()      # Analyse and build orders
        gl.trade_funcs.exe_orders(orders)  # Execute orders.

        if gl.loop_feedback == False:
            break

    gl.save_all()
    print('\ndone')
    print('\nP\L: ${:.2f}'.format(gl.pl_ex['real']))

    duration = time.time() - start_time
    print(f'\nalgo finished in {duration} second(s)\n')
