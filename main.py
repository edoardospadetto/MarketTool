from src.frankfurt_se import *
from src.time_misc import *
from  datetime import timedelta, datetime

import matplotlib.pyplot as plt
import numpy as np

to_date = datetime.now()
from_date = to_date - timedelta(days = 365*2)
to_date= int(toUnixTimestamp(to_date))
from_date =int(toUnixTimestamp(from_date))


stocks = { "Ferrari" : 'NL0011585146',
"Mercedes" : 'DE0007100000',
"Stellantis": "NL00150001Q9",
"BMW" : "DE0005190003",
"Renault" : "FR0000131906" }

print('from:', from_date, ' to:', to_date)
for name, isin in stocks.items():
    data = get_price_hystory(isin, resolution='1d' , from_date=from_date, to_date=to_date )


    high = np.array(data['h'])
    time = np.array(data['t'])
    print(len(time))


    plt.plot(time,np.log(high/high[0]), label = name)

plt.legend()
plt.show()
