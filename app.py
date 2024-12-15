import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title="StartUp Analysis")

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] =  df['date'].dt.month
df['year'] =  df['date'].dt.year

def load_overall_analysis():
    st.title("Overall Analysis")

    # total invested amount
    total = round(df['amount'].sum())
    
    
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]

    # avg ticket price 
    average_funding = df.groupby('startup')['amount'].sum().mean()

    # number of funded startups
    num_startup = df['startup'].nunique()


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max Funding', str(max_funding) + 'Cr')
    with col3:
        st.metric('Average Funding', str(round(average_funding)) + 'Cr')
    with col4:
        st.metric('Funded Startups', str(num_startup))

    st.header('MoM Graph')
    select_option = st.selectbox('Select Type', ['Total', 'Count'])
    if select_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str') 
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig5)


def load_investor_details(investor):
    st.title(investor)



    # load the 5 recent investment of investor
    filtered_df = df[df['investors'].str.contains(investor, na=False)] 
    result_df = filtered_df[['date', 'startup', 'vertical', 'city', 'investors', 'round', 'amount']].head()
    # result_df
    st.subheader("Most Recent Invesments")
    st.dataframe(result_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor, na = False)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
        st.subheader("Biggest Invesments")
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor, na = False)].groupby('vertical')['amount'].sum()
        st.subheader("Sectors Invested In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor, na = False)].groupby('round')['amount'].sum()
        st.subheader("Round Invested In")
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels = round_series.index, autopct= "%0.01f%%")
        st.pyplot(fig2)
    with col4:
        city_series = df[df['investors'].str.contains(investor, na = False)].groupby('city')['amount'].sum()
        st.subheader("City Invested In")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels = city_series.index, autopct= "%0.01f%%")
        st.pyplot(fig3)
        
    col5, col6  = st.columns(2)
    with col5:
        df['year'] =  df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor, na = False)].groupby('year')['amount'].sum()
        st.subheader("YoY Invested Graph")
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)
        st.pyplot(fig4)

    



st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.title("Show Overall Analysis")
    if btn0:
        load_overall_analysis()
elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp', sorted(df['Startup Name'].unique().tolist()))
    btn1 = st.sidebar.button("Find StartUp Details")
    st.title("StartUp Analysis")
else : 
    selected_investor = st.sidebar.selectbox(
    'Select Investor',
    df['investors'].dropna().str.split(',').explode().str.strip().drop_duplicates().sort_values()
)
    btn2 = st.sidebar.button("Find Investor Details")
    st.title("Investor Analysis")
    if btn2:
        load_investor_details(selected_investor)