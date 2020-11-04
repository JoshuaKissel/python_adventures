import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import seaborn as sns
import mpld3 as mpld3


df = pd.read_csv('incident_report_per_dow_in_ALL.csv', delimiter=',')

print(df.head(10))

sns.set(style='darkgrid')
sns.set_style('ticks')
b = sns.barplot(
data=df,
color='b')
b.set_xlabel(xlabel='Hour')
b.set_ylabel('Incident Count')
b.set_title('Amount of Incidents per Hour for week of ')
plt.xticks(
	rotation=90,
	horizontalalignment='center',
	fontweight='light',
	fontsize='6')

plt.show()