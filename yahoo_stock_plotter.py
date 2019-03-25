import csv
from pandas_datareader.data import DataReader
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import pylab as pl

filename = 'symbol_list_yahoo.csv'

def getColumn(filename, column):
    data = csv.reader(open(filename), delimiter=",")
    return [element[column] for element in data]

company = getColumn(filename,2)
ticker = getColumn(filename,1)

loop=0

while loop == 0:
    compname = str(raw_input('What company are you looking for?(Start with capital letter if nothing found)) '))
    options = filter(lambda x: compname in x,company)    
    if len(options) >= 2 and len(options) <= 30:
        print options
        print "Which one is it?"
    elif len(options) == 1:
        print options
        yn = str(raw_input("Is this the one?y/n? "))
        if yn == 'y':
            loop = 1
            compname = options[0]
            pass
        elif yn == 'n':
            pass
        else:
            print "this is not a valid choice"
            pass
    else:
        print "No or too many companies found"
        pass


ticker_symbol = ticker[company.index(compname)]

##### Download the data #####

startdate = datetime(2013,1,1)
enddate = datetime.now()

stock = DataReader(ticker_symbol,  "yahoo", startdate, enddate)

value=[]

for n in range(0,len(stock)):
    value.append(stock["High"][n])

x = np.arange(len(stock))

##### Interpolate #####

y_interpolated = interp1d(x,value,bounds_error=False,fill_value=0.,kind='cubic')
new_x_array = np.arange(min(x),max(x),0.1)

##### Polynomial fit #####

p = np.poly1d(np.polyfit(x,value,50))

pv = np.polyval(p,new_x_array)

pv1 = np.polyval(p,max(x)+1)

##### Least squares fit #####

A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, value)[0]


##### Plot #####

plt.plot(x, m*x + c, 'g', label='Least squares fit')

plt.grid(True)
plt.plot(new_x_array,y_interpolated(new_x_array),'r-',label='Original data')
plt.plot(new_x_array,p(new_x_array),'--', label='Polynomial fit')
plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.legend()
plt.title('Plot of the %s Stock - Daily High from %s - %s \n \n' % (ticker_symbol, startdate.strftime("%Y-%m-%d"),enddate.strftime("%Y-%m-%d")))

plt.show()

