from can_withdraw import can_withdraw
from profit import ProfitCalulator


desired_rate = .04
profit_calulator = ProfitCalulator(.05)
arbitrage_available = profit_calulator.arbitrage_available(.10)


if len(arbitrage_available.keys()) > 0:
    print("Executing arbitrage: ")
    print(arbitrage_available)
else:
    print("No opportunities available at {0}".format((str(desired_rate * 100)+"%")))