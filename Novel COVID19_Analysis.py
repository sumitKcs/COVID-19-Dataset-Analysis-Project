
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



#reading data from csv file on Kaggle
data = pd.read_csv("covid_19_data.csv")
data.shape

data.head()

data.drop("SNo",axis=1,inplace=True)
data.drop("Last Update",axis=1, inplace=True)
data.info()

data.describe()

#checking for duplicate rows
duplicate_rows=data.duplicated(subset=['Country/Region','Province/State','ObservationDate'])
data[duplicate_rows]

# Countries list of spreading infection across the world
country_list = list(data['Country/Region'].unique())
print(country_list)
len(country_list)

# Checking the dates in the ObervationDate section 
print(list(data['ObservationDate'].unique()))
print(len(list(data['ObservationDate'].unique())))

# Converting date to datetime object
data['ObservationDate'] = pd.to_datetime(data['ObservationDate'])
data['Date_date'] = data['ObservationDate'].apply(lambda x:x.date())

#The total number of confirmed cases for each country 
df_country=data.groupby(['Country/Region']).max().reset_index(drop=None)
print(df_country[['Country/Region','Confirmed','Deaths','Recovered']])

#Number of cases reported each day
df_by_date=data.groupby(['Date_date']).sum().reset_index(drop=None)
df_by_date['daily_cases']=df_by_date.Confirmed.diff()
df_by_date['daily_deaths']=df_by_date.Deaths.diff()
df_by_date['daily_recoveries']=df_by_date.Recovered.diff()
df_by_date

#plotting the data
#Number of confirmed cases by date 

dataDate=data.groupby(['Date_date']).sum().reset_index(drop=None)

plt.figure(figsize=(12,5))
sns.axes_style("whitegrid")
sns.barplot(x="Date_date",
            y="Confirmed",
            data=dataDate[178:193],
            palette=sns.color_palette("coolwarm",15)
            )
plt.xticks(rotation=60)
plt.ylabel('Number of confirmed cases(in lacs)',fontsize=15)
plt.xlabel('Dates',fontsize=15)

#  Plotting two line for deaths and recoveries respectively

plt.figure(figsize=(8,5))
plt.plot('Date_date',
         'Deaths',
         data=dataDate,
         color='red'
         )
plt.plot('Date_date',
         'Recovered',
         data=dataDate,
         color='green'
         )
plt.xticks(rotation=60)
plt.ylabel('Number of cases(in l acs)',fontsize=15)
plt.xlabel('Dates',fontsize=15)
plt.legend()

# Most affected countries

plt.figure(figsize=(15,5))
sns.barplot(x="Country/Region",
            y="Confirmed",
            data=df_country.nlargest(10,'Confirmed'),
            palette=sns.cubehelix_palette(15,reverse=True)
            )
plt.xticks(rotation=60,fontsize=12)
plt.ylabel("Number of cases (in lacs)",fontsize=20)
plt.ylabel('Countries',fontsize=20)

#mortality rate over time
# numbers of deaths divide by number of confirmed cases

plt.figure(figsize=(10,5))
df_by_date['mrate']=df_by_date.apply(lambda x:x['Deaths']*100/(x['Confirmed']),axis=1)
plt.plot('Date_date',
         'mrate',
         data=df_by_date,
         color='red')

plt.xticks(rotation=45,fontsize=12)
plt.ylabel('M0rtallity rate(%)',fontsize=20)
plt.xlabel('Deaths',fontsize=20)


# Number of cases based on provinces

plt.figure(figsize=(10,5))

data_province = data.copy()
df_province=data_province.groupby(['Province/State']).max().reset_index(drop=None)
df_province.dropna(axis=0,inplace=True)
df_province = df_province.nlargest(15,'Confirmed')

plt.figure(figsize=(10,6))
sns.barplot(x='Confirmed',
            y='Province/State',
            hue=variable,
            data=df_province,
            palette='Set1')

plt.ylabel('Provinces',fontsize=15)
plt.xlabel('Number of Cases',fontsize=15)
plt.xticks(rotation=45,fontsize=12)



























