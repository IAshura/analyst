import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#mengubah style seaborn
sns.set(style='dark')

#mengimport data
all_data = pd.read_csv('https://raw.githubusercontent.com/IAshura/analyst/main/main_data.csv')

datetime_columns = ['date']
all_data.sort_values(by='date', inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

#menyiapkan dataframe yang diperlukan
def create_month_recap(df):
    plot_month = df['month'].astype(str)
    plot_year = df['year'].astype(str)
    df['year_month'] = plot_month + ' ' + plot_year
    df['total_sum'] = df.groupby('year_month')['total'].transform('sum')
    return df[['year_month', 'total_sum']]

def create_season_recap(df):
    season_recap = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_recap

def create_weather_recap(df):
    weather_recap = df.groupby(by='weather').agg({
    'total': 'mean'
    }).reset_index()
    return weather_recap

#membuat filter tanggal pada sidebar
max_date = pd.to_datetime(all_data['date']).dt.date.max()
min_date = pd.to_datetime(all_data['date']).dt.date.min()

with st.sidebar:

    #input start_date dan end_date
    start_date, end_date = st.date_input(
        label='Pilih  Rentang Waktu',
        max_value=max_date,
        min_value=min_date,
        value=[min_date, max_date]
    )
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)
    
    st.write(
        """ 
        **Muhammad Mazen Fayiz Birizqie**\n
        Dicoding ID: **mazen_fayiz**\n
        Email: **m258d4ky2197@bangkit.academy**
        """
    )

main_df = all_data[(all_data['date'] >= str(start_date)) & 
                (all_data['date'] <= str(end_date))]

month_recap_df = create_month_recap(main_df)
season_recap_df = create_season_recap(main_df)
weather_recap_df = create_weather_recap(main_df)

st.header('BIKE SHARING ANALYTICS DASHBOARD')
# Subheader Season and Weather Recap
st.subheader('Recap Season and Weather')

# Create a subplot with a figure size of 20x10
fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y='registered',
    x='season',
    data=season_recap_df.sort_values(by='registered', ascending=False),
    color='tab:blue',
    label='Registered User',
    ax=ax
)

sns.barplot(
    y='casual',
    x='season',
    data=season_recap_df.sort_values(by='casual', ascending=False),
    color='tab:orange',
    label='Casual User',
    ax=ax
)

ax.set_title('Number of Rent by Season', loc='center', fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.legend(fontsize=20)

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)

# Membuat UI

st.subheader('Relationship between weather conditions (temperature, humidity, wind speed) and Number of Bike Rentals per Hour')
plt.figure(figsize=(10, 6))
sns.set(style='whitegrid')
sns.lineplot(
    data=main_df,  # Menggunakan main_df yang sudah difilter berdasarkan rentang tanggal yang dipilih
    x='temp',  # Menggunakan suhu sebagai sumbu x
    y='total',  # Menggunakan jumlah sewa sepeda sebagai sumbu y
    marker='o'
)
plt.title("Relationship between weather conditions (temperature, humidity, wind speed) and Number of Bike Rentals per Hour")
plt.xlabel("Suhu (°C)")
plt.ylabel("Jumlah Sewa Sepeda")

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)



# Subheader Monthly Recap
st.subheader('performance of rental bicycle monthly')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_recap_df['year_month'],
    month_recap_df['total_sum'],
    marker='o',
    linewidth=5,
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)
