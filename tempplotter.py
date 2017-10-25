import pandas as pd
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as dates
import datetime as dt

con = sqlite3.connect("/data/rhomicron.com/www/templog.db")
df = pd.read_sql_query("SELECT * from temps", con, index_col=None, parse_dates=['timestamp'])

con.close()

df2 = df.ix[3:]
x = df2['timestamp'].astype(dt.datetime)

#print(x.tail(10))
#print(df2['temp'].tail(100))

# Create a plot with matplotlib and store .png
fig, axes = plt.subplots(3, figsize=(8,8), sharex=False)
fig.text(0.5, 0.01, 'Time', fontsize=14, ha='center')
fig.text(0.06, 0.5, 'Temperature (Celcius)', fontsize=14, va='center', rotation='vertical')


#axes[0].plot(df2['timestamp'], df2['temp'])

axes[0].plot(x, df2['temp']/1000, color='black', label='Loft')
axes[1].plot(x, pd.rolling_mean(df2['temp']/1000, 3000), color='black', label='Loft moving average N=3000')
#axes[2].plot(x.tail(100), (df2['temp'].tail(100))/1000, color='black', label='Last N=1000')
             
#axes[0].axhline(df2['temp'].mean(), color='black', linestyle='--', label="Mean temp: %.1f" % (df2['temp'].mean()))
#axes[1].bar(df2['temp'].values, df2['temp'].values)

#print(df2['temp'].values)
#axes[0].xaxis_date()
#axes[0].xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%d.%m.%y'))


for ax in axes:
	ax.grid(True, which='Both')
	ax.xaxis_date()
	ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%d.%m.%y'))
	ax.legend(bbox_to_anchor=(.95, .25), loc=1, borderaxespad=0., prop={'size':10})
	ax.tick_params(labelsize=11)
	#ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

#df2.plot(ax=axes[0])
#df2.plot()


fig.savefig('/data/rhomicron.com/www/loft_temp.jpg')

