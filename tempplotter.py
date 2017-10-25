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

# Remove first 3 rows
df2 = df.ix[3:]
df = df.ix[3:]

# Re-index dfx with time column
df.set_index('timestamp', inplace=True)

n_days = 7
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
starttime = datetime.now() - timedelta(days=n_days)#'2017-10-20 17:00:00'
stoptime = now#'2017-10-22 20:00:00'

mask = (df.index > starttime) & (df.index <= stoptime)
print(mask)

x = df2['timestamp'].astype(dt.datetime)

# Create a plot with matplotlib and store .png
fig, axes = plt.subplots(2, figsize=(8,8), sharex=False)
fig.text(0.5, 0.05, 'Time', fontsize=14, ha='center')
fig.text(0.06, 0.5, 'Temperature (Celcius)', fontsize=14, va='center', rotation='vertical')

# Rolling mean N
n = 12000

axes[0].plot(df.index, df['temp']/1000, color='black', alpha=0.3, label='Loft temperature')
axes[0].plot(df.index, df['temp'].rolling(center=True, window=n).mean()/1000, color='black', label='Moving average')

   
axes[1].plot(df.index[mask], df['temp'][mask].rolling(center=True, window=10).mean()/1000, color='black', label='Last %d days' % n_days)
          
for ax in axes:
	ax.grid(True, which='Both')
	ax.xaxis_date()
	ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%d.%m.%y'))
	ax.legend(bbox_to_anchor=(0.97, .97), loc=1, borderaxespad=0., prop={'size':10})
	ax.tick_params(labelsize=11)
	#ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))


fig.savefig('loft_temp.jpg')

