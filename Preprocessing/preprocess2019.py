import csv
import pandas as pd
import datetime

df = pd.read_csv("data/COBRA-2019.csv")
keep_col = ['Occur Date', 'Occur Time', 'Beat', 'Location', 'Shift Occurrence', 'UCR #', 'UCR Literal', 'Neighborhood', 'NPU', 'Longitude', 'Latitude']
new_f = df[keep_col]
#new_f.rename(columns = {'UCR Literal':'UCRLiteral'},inplace = True)

# new_f = new_f['Beat'].fillna(0)
print(new_f['Occur Time'].dtype)
new_f['Beat'] = new_f['Beat'].astype('str')
#new_f['Occur Time'] = pd.to_numeric(new_f['Occur Time'])
new_f[['Beat','Useless']] = new_f['Beat'].str.split('.',expand=True)

new_f = new_f.drop(columns = ['Useless', 'Shift Occurrence'])

new_f[['Neighborhood']] = new_f[['Neighborhood']].fillna(value='Null')
new_f = new_f[new_f['Neighborhood']!='Null']

def occurence_time(row):
	if row['Occur Time'] < 800:
		return "Morning"
	elif row['Occur Time'] < 1600:
		return "Day"
	else:
		return "Evening"

print('Length of dataset: ',len(new_f))
new_f['Shift Occurrence'] = new_f.apply (lambda row: occurence_time (row),axis=1)


# Changes each date(YYYY-MM-DD) to day of the week(0: Monday through 6: Sunday)
def day_of_week(row):
    cur_date = row['Occur Date']
    month, day, year = (int(x) for x in cur_date.split('/'))    
    dt = datetime.date(year, month, day)
    return(dt.weekday())
  
new_f['Day of Week'] = new_f.apply(lambda row: day_of_week (row), axis=1)

def year(row):
    cur_date = row['Occur Date']
    month, day, year = (int(x) for x in cur_date.split('/'))    
    year = int(year)
    return year

new_f['Year'] = new_f.apply(lambda row: year(row), axis=1)
#cat_list = new_f.UCRLiteral.unique()
#print(cat_list)
def crime_category(row):
	cat = 0
	if row['UCR Literal'] in ['HOMICIDE','MANSLAUGHTER']:
		cat = 1
	if row['UCR Literal'] in ['AGG ASSAULT','ROBBERY-PEDESTRIAN','ROBBERY-COMMERCIAL','ROBBERY-RESIDENCE']:
		cat = 2
	if row['UCR Literal'] in ['BURGLARY-RESIDENCE','BURGLARY-NONRES','AUTO THEFT']:
		cat = 3
	if row['UCR Literal'] in ['LARCENY-FROM VEHICLE','LARCENY-NON VEHICLE']:
		cat = 4
	return cat

new_f['Crime Category'] = new_f.apply(lambda row: crime_category (row), axis=1)
new_f = new_f[ (new_f['Longitude'] >= -84.5) & (new_f['Longitude'] <= -84.2)]
new_f = new_f[ (new_f['Latitude'] >= 33.61) & (new_f['Latitude'] <= 33.92)]
new_f = new_f[ (new_f['Year'] == 19)]
new_f = new_f.drop(['Year'],axis=1)
#new_f = new_f[ (new_f['Occur Date'] >= '01/01/2019') & (new_f['Occur Date'] <= '9/23/2019')]

print(new_f)
new_f.to_csv("cobra-clean2019.csv", index=False)