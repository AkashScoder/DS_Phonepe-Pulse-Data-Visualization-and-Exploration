import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px
from PIL import Image
import json

# Setting up page configuration
icon = Image.open(
    "C://Users//akash//PycharmProjects//PhonePe pulse visualization//Phonepe-Pulse-Data-Visualization-and-Exploration//PhonePe-IMG.jpg")
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | By Akash S",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This dashboard app is created by Akash
                        Data has been cloned from Phonepe Pulse Github Repository"""})

# Sidebar headerimport pandas as pd
# from sqlalchemy import create_engine
# import streamlit as st
st.sidebar.header(" Welcome to the dashboard ")

# Creating connection with MySQL using SQLAlchemy
DATABASE_URL = "mysql+pymysql://root:2261389@localhost/PhonePe"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL)

# Main menu selection
selected = st.sidebar.selectbox("Menu", ["Home", "Top Charts", "Performance Analysis", "Geographic Analysis", "About"])

# Custom CSS for styling
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .big-chart {
        width: 100%;
        height: 600px;
    }
    .centered-title {
        text-align: center;
    }
    .banner-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4B0082;
        margin-bottom: 1rem;
    }
    .tech-list {
        list-style-type: none;
        padding: 0;
    }
    .tech-list li {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# MENU 1 - HOME
if selected == "Home":
    st.image(
        "C://Users//akash//PycharmProjects//PhonePe pulse visualization//Phonepe-Pulse-Data-Visualization-and-Exploration//PhonePe-IMG.jpg",
        width=300)  # Adjust the width as needed
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")

    st.markdown("### :violet[Domain:] **Fintech**")
    st.markdown("### :violet[Technologies Used:]")
    st.markdown("- Github Cloning")
    st.markdown("- Python, Pandas")
    st.markdown("- MySQL, SQLAlchemy")
    st.markdown("- Streamlit, Plotly")

    st.markdown("## :rocket: Overview")
    st.markdown(
        "Explore PhonePe Pulse data with interactive visualizations to uncover insights about transactions, users, top states, districts, pincodes, and popular brands.")

    st.markdown("### :bulb: Key Features")
    st.markdown("- Visualize transaction trends and user demographics")
    st.markdown("- Analyze top-performing states, districts, and brands")
    st.markdown("- Interactive bar charts, pie charts, and geographical maps for deeper insights")

    st.image(
        "C://Users//akash//PycharmProjects//PhonePe pulse visualization//Phonepe-Pulse-Data-Visualization-and-Exploration//PhonePe-IMG.jpg",
        width=300)  # Adjust the width as needed

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown('<h1 class="centered-title">Top Charts</h1>', unsafe_allow_html=True)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    # colum1, colum2 = st.columns([0.75,0.75], gap="small")
    # with colum1:
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2024)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    if Year == 2024 and Quarter in [2, 3, 4]:
        st.markdown("#### Sorry No Data to Display for 2024 Qtr 2,3,4")

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        # col1, col2, col3 = st.columns(3, gap="small")
        top_n = st.sidebar.slider('Select Top N', min_value=1, max_value=20, value=5)
        performance_choice = st.sidebar.selectbox('Select Performance Type',
                                                  options=['Best Performing', 'Worst Performing'])
        level = st.sidebar.selectbox("Select Level", ["State", "District", "Pincode"])
        # Determine the order based on the performance choice
        order = 'DESC' if performance_choice == 'Best Performing' else 'ASC'


        # Function to display centered visualization
        def display_centered_visualization(fig):
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


        # Visualization for 'State' level
        if level == 'State':
            st.markdown("### :violet[State]")
            query = f"""
                        SELECT state, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total
                        FROM agg_transaction
                        WHERE year = {Year} AND quarter = {Quarter}
                        GROUP BY state
                        ORDER BY Total {order}
                        LIMIT {top_n}
                    """
            df = pd.read_sql(query, engine)
            if top_n < 6:
                visualization = st.sidebar.selectbox('select Visualization type',
                                                     options=['Pie Chart', 'Bar chart'])
            else:
                visualization = 'Bar Chart'
            if visualization == 'Pie Chart':
                fig = px.pie(
                    df,
                    values='Total',  # Change this according to your dataframe column
                    names='state',  # Change this according to your dataframe column
                    title=f'Top {top_n} {performance_choice} {level} based on Transaction',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['Total']  # Change this according to your dataframe column
                )
            else:
                fig = px.bar(
                    df,
                    x='state',
                    y='Total',
                    title=f'Top {top_n} {performance_choice} {level} based on Transaction',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    labels={'Total_Transactions_Sum': 'Total'}
                )
            display_centered_visualization(fig)

        # Visualization for 'Pincode' level
        if level == 'Pincode':
            st.markdown('<h3 class="centered-text">Pincode</h3>', unsafe_allow_html=True)
            query = f"""
                        SELECT pincode, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total_Transaction_amount
                        FROM top_trans
                        WHERE year = {Year} AND quarter = {Quarter}
                        GROUP BY pincode
                        ORDER BY Total_Transaction_amount {order}
                        LIMIT {top_n}
                    """
            df = pd.read_sql(query, engine)
            if top_n < 6:
                visualization = st.sidebar.selectbox('select Visualization type', options=['Pie Chart', 'Bar chart'])
            else:
                visualization = 'Bar Chart'
            if visualization == 'Pie Chart':
                fig = px.pie(
                    df,
                    values='Total_Transaction_amount',  # Change this according to your dataframe column
                    names='pincode',  # Change this according to your dataframe column
                    title=f'Top {top_n} {performance_choice} {level} based on Transaction',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['Total_Transaction_amount']  # Change this according to your dataframe column
                )
            else:
                fig = px.bar(
                    df,
                    x='pincode',
                    y='Total_Transaction_amount',
                    title=f'Top {top_n} {performance_choice} {level} based on Transaction',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    labels={'Total_Transactions_Sum': 'Total_Transaction_amount'}
                )
            display_centered_visualization(fig)

        # Visualization for 'District' level
        if level == 'District':
            st.markdown('<h3 class="centered-text">District</h3>', unsafe_allow_html=True)
            query = f"""
                        SELECT district, SUM(Count) AS Total_Count, SUM(Amount) AS Total
                        FROM map_trans
                        WHERE year = {Year} AND quarter = {Quarter}
                        GROUP BY district
                        ORDER BY Total {order}
                        LIMIT {top_n}
                    """
            df = pd.read_sql(query, engine)
            if top_n < 6:
                visualization = st.sidebar.selectbox('select Visualization type', options=['Pie Chart', 'Bar chart'])
            else:
                visualization = 'Bar Chart'
            if visualization == 'Pie Chart':
                fig = px.pie(
                    df,
                    values='Total',  # Change this according to your dataframe column
                    names='district',  # Change this according to your dataframe column
                    title=f'Top {top_n} {performance_choice} {level} based on Transaction',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['Total']  # Change this according to your dataframe column
                )
            else:
                fig = px.bar(
                    df,
                    x='district',
                    y='Total',
                    title=f'Top {top_n} {performance_choice} {level} based on Transaction',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    labels={'Total_Transactions_Sum': 'Total'}
                )
            display_centered_visualization(fig)
    # Top Charts - USERS
    if Type == "Users":
        top_n = st.sidebar.slider('Select Top N', min_value=1, max_value=20, value=5)
        performance_choice = st.sidebar.selectbox('Select Performance Type',
                                                  options=['Best Performing', 'Worst Performing'])
        level = st.sidebar.selectbox("Select Level", options=["brands", "state", "district", "pincode"])
        # Determine the order based on the performance choice
        order = 'DESC' if performance_choice == 'Best Performing' else 'ASC'

        if level == "brands":
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                query = f"""
                            SELECT brands, SUM(count) AS Total_Count, AVG(percentage)*100 AS Avg_Percentage
                            FROM agg_users
                            WHERE year = {Year} AND quarter = {Quarter}
                            GROUP BY brands
                            ORDER BY Total_Count {order}
                            LIMIT {top_n}
                        """
                df = pd.read_sql(query, engine)
                if top_n < 6:
                    choice = st.sidebar.selectbox('select visualization type', options=['Bar chart', 'Pie chart'])
                else:
                    choice = 'Bar Chart'
                if choice == 'Pie chart':
                    fig = px.pie(df,
                                 title=f'Top {top_n} {performance_choice} {level} based on users',
                                 values="Total_Count",
                                 names="brands",
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 hover_data=['Avg_Percentage'])
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                else:
                    fig = px.bar(df,
                                 title=f'Top {top_n} {performance_choice} {level} based on users',
                                 x="Total_Count",
                                 y="brands",
                                 orientation='h',
                                 color='Avg_Percentage',
                                 color_continuous_scale=px.colors.sequential.Agsunset)

                fig.update_layout(xaxis_title='Total Count',
                                  yaxis_title='Brands')
                st.markdown('<div class="centered">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        elif level == 'district':
            st.markdown("### :violet[District]")
            query_district = f"""
                        SELECT district, SUM(count) AS total_users, SUM(amount) AS total_amount
                        FROM map_trans
                        WHERE year = {Year} AND quarter = {Quarter}
                        GROUP BY district
                        ORDER BY total_users {order}
                        LIMIT {top_n}
                    """
            df = pd.read_sql(query_district, engine)
            if top_n < 6:
                choice = st.sidebar.selectbox('select visualization type', options=['Bar chart', 'Pie chart'])
            else:
                choice = 'Bar Chart'
            if choice == 'Pie chart':
                fig = px.pie(df,
                             title=f'Top {top_n} {performance_choice} {level} based on users',
                             values="total_users",
                             names="district",
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['total_amount'])
                fig.update_traces(textposition='inside', textinfo='percent+label')

            else:
                fig = px.bar(df,
                             title=f'Top {top_n} {performance_choice} {level} based on users',
                             x="total_users",
                             y="district",
                             orientation='h',
                             color='total_amount',
                             color_continuous_scale=px.colors.sequential.Agsunset)

                fig.update_layout(xaxis_title='total_users',
                                  yaxis_title='district')
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif level == 'pincode':
            st.markdown("### :violet[Pincode]")
            query_pincode = f"""
                        select pincode,transaction_count,transaction_amount 
                        from top_trans where year={Year} and quarter={Quarter} 
                        order by transaction_count {order}
                        limit {top_n};
                    """
            df = pd.read_sql(query_pincode, engine)
            if top_n < 6:
                choice = st.sidebar.selectbox('select visualization type', options=['Bar chart', 'Pie chart'])
            else:
                choice = 'Bar Chart'
            if choice == 'Pie chart':
                fig = px.pie(df,
                             title=f'Top {top_n} {performance_choice} {level} based on users',
                             values="transaction_count",
                             names="pincode",
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['transaction_amount'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
            else:
                fig = px.bar(df,
                             title=f'Top {top_n} {performance_choice} {level} based on users',
                             x="transaction_count",
                             y="pincode",
                             orientation='h',
                             color='transaction_amount',
                             color_continuous_scale=px.colors.sequential.Agsunset)

                fig.update_layout(xaxis_title='transaction_count',
                                  yaxis_title='pincode')
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("### :violet[State]")
            query_state = f"""
                        SELECT state, SUM(count) AS total_users, SUM(amount) AS total_amount
                        FROM map_trans
                        WHERE year = {Year} AND quarter = {Quarter}
                        GROUP BY state
                        ORDER BY total_users {order}
                        LIMIT {top_n}
                    """
            df = pd.read_sql(query_state, engine)
            if top_n < 6:
                choice = st.sidebar.selectbox('select visualization type', options=['Bar chart', 'Pie chart'])
            else:
                choice = 'Bar Chart'
            if choice == 'Pie chart':
                fig = px.pie(df,
                             title=f'Top {top_n} {performance_choice} {level} based on users',
                             values="total_users",
                             names="state",
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['total_amount'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
            else:
                fig = px.bar(df,
                             title=f'Top {top_n} {performance_choice} {level} based on users',
                             x="total_users",
                             y="state",
                             orientation='h',
                             color='total_amount',
                             color_continuous_scale=px.colors.sequential.Agsunset)

                fig.update_layout(xaxis_title='total_users',
                                  yaxis_title='state')
            st.markdown('<div class="centered">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# MENU 3 - EXPLORE DATA
if selected == "Performance Analysis":
    state = st.sidebar.selectbox('Choose Metric analyze performance',
                                 options=['Transactions', 'Users', 'Transaction Type', 'Brands'])
    history = st.sidebar.selectbox('select year', options=['overall', 2018, 2019, 2020, 2021, 2022, 2023])
    if state == 'Users':
        if history == 'overall':
            sub_query = 'select distinct(state) from top_user'
            sub_df = pd.read_sql(sub_query, engine)
            states = sub_df['state']
            state = st.sidebar.selectbox('Select the state', options=states)
            query = f'''
                                   select year,state,sum(registered_users) as counts from top_user
                                    where state='{state}' and year<2024
                                     group by state,year ;
                                   '''
            df = pd.read_sql(query, engine)

            fig = px.scatter(df,
                             x='year',
                             y='counts',
                             title=f'Performance History of registered users of {state}',
                             labels={'year': 'Time Period', 'counts': 'Performance Metric'},
                             color_discrete_sequence=['#636EFA'])
            fig.add_traces(px.line(df,
                                   x='year',
                                   y='counts',
                                   labels={'year': 'Time Period', 'counts': 'Registered Users'},
                                   color_discrete_sequence=['#636EFA']).data)

            # Update layout
            fig.update_layout(xaxis_title='Time Period',
                              yaxis_title='Registered Users',
                              showlegend=True)

            # Show the plot
            st.plotly_chart(fig, use_container_width=True)
        else:
            sub_query = 'select distinct(state) from top_user'
            sub_df = pd.read_sql(sub_query, engine)
            states = sub_df['state']
            state = st.sidebar.selectbox('Select the state', options=states)
            query = f'''
                                   select quarter,state,sum(registered_users) as counts from top_user
                                    where state='{state}' and year={history}
                                    group by state,quarter,year
                                   '''
            df = pd.read_sql(query, engine)

            fig = px.scatter(df,
                             x='quarter',
                             y='counts',
                             title=f'Performance History of registered users of {state} on {history}',
                             labels={'quarter': 'Time Period', 'counts': 'Performance Metric'},
                             color_discrete_sequence=['#636EFA'])
            fig.add_traces(px.line(df,
                                   x='quarter',
                                   y='counts',
                                   labels={'quarter': 'Quarter', 'counts': 'Registered Users'},
                                   color_discrete_sequence=['#636EFA']).data)

            # Update layout
            fig.update_layout(xaxis_title='Quarter',
                              yaxis_title='Registered Users',
                              showlegend=True)

            # Show the plot
            st.plotly_chart(fig, use_container_width=True)
    elif state == 'Transactions':
        if history == 'overall':
            sub_query = 'select distinct(state) from top_trans'
            sub_df = pd.read_sql(sub_query, engine)
            states = sub_df['state']
            state = st.sidebar.selectbox('Select the state', options=states)
            query = f'''
                                   select year,state,sum(transaction_amount) as total_transaction from top_trans
                                    where state='{state}' and year<2024
                                     group by state,year ;
                                   '''
            df = pd.read_sql(query, engine)

            fig = px.scatter(df,
                             x='year',
                             y='total_transaction',
                             title=f'Performance History of total transactions of {state}',
                             labels={'year': 'Time Period', 'total_transaction': 'Total Transaction'},
                             color_discrete_sequence=['#636EFA'])
            fig.add_traces(px.line(df,
                                   x='year',
                                   y='total_transaction',
                                   labels={'year': 'Time Period', 'total_transaction': 'Total Transaction'},
                                   color_discrete_sequence=['#636EFA']).data)

            # Update layout
            fig.update_layout(xaxis_title='Time Period',
                              yaxis_title='Total Transactions in Billions',
                              showlegend=True)

            # Show the plot
            st.plotly_chart(fig, use_container_width=True)
        else:
            sub_query = 'select distinct(state) from top_trans'
            sub_df = pd.read_sql(sub_query, engine)
            states = sub_df['state']
            state = st.sidebar.selectbox('Select the state', options=states)
            query = f'''
                                    select year,state,quarter,sum(transaction_amount) as total_transactions from top_trans
                                    where state='{state}' and year={history}
                                    group by state,year,quarter
                                   '''
            df = pd.read_sql(query, engine)
            df['total_transactions'] = df['total_transactions'] / 1_000_000_000
            fig = px.scatter(df,
                             x='quarter',
                             y='total_transactions',
                             title=f'Performance History of total_transaction of {state} on {history}',
                             labels={'quarter': 'Time Period', 'total_transactions': 'Total Transaction'},
                             color_discrete_sequence=['#636EFA'])
            fig.add_traces(px.line(df,
                                   x='quarter',
                                   y='total_transactions',
                                   labels={'quarter': 'Quarter', 'total_transactions': 'Total Transaction'},
                                   color_discrete_sequence=['#636EFA']).data)

            # Update layout
            fig.update_layout(xaxis_title='Quarter',
                              yaxis_title='Total Transactions in Billions',
                              showlegend=True)

            # Show the plot
            st.plotly_chart(fig, use_container_width=True)
    elif state == 'Transaction Type':
        if history == 'overall':
            sub_query1 = 'select distinct(state) as state from agg_transaction'
            sub_query2 = 'select distinct(transaction_type) as types from agg_transaction'
            sub_df1 = pd.read_sql(sub_query1, engine)
            sub_df2 = pd.read_sql(sub_query2, engine)
            state_list = sub_df1['state']
            transaction_type_list = sub_df2['types']
            states = st.sidebar.selectbox('Select the state', options=state_list)
            transaction_type = st.sidebar.selectbox('Select transaction type', options=transaction_type_list)
            query = f'''
                                    select state,year,transaction_type,sum(transaction_amount) as  total_transactions from agg_transaction 
                                    where state='{states}'  and transaction_type = '{transaction_type}' 
                                    group by state,year,transaction_type ;
                                   '''
            df = pd.read_sql(query, engine)
            df['total_transactions'] = df['total_transactions'] / 1000000000
            fig = px.pie(df, values='total_transactions', names='year',
                         title=f'Distribution of  {transaction_type} for {state} in billions',
                         )
            st.plotly_chart(fig)
        else:
            sub_query1 = 'select distinct(state) as state from agg_transaction'
            sub_df1 = pd.read_sql(sub_query1, engine)
            state_list = sub_df1['state']
            states = st.sidebar.selectbox('Select the state', options=state_list)
            query = f'''
                                                select state,year,transaction_type,sum(transaction_amount) as  total_transactions from agg_transaction 
                                                where state='{states}' and year={history} 
                                                group by state,year,transaction_type ;
                                               '''
            df = pd.read_sql(query, engine)
            df['total_transactions'] = df['total_transactions'] / 1000000000
            fig = px.pie(df, values='total_transactions', names='transaction_type',
                         title=f'Distribution of {state} in year {history} for {states} in billions',
                         )
            st.plotly_chart(fig)
    elif state == 'Brands':
        if history == 'overall':
            sub_query1 = 'select distinct(state) as state from agg_transaction'
            sub_df1 = pd.read_sql(sub_query1, engine)
            state_list = sub_df1['state']
            states = st.sidebar.selectbox('select the state', options=state_list)
            query = f'''
                     select state,brands,sum(count) as 'No of Users' from agg_users
                     where state='{states}' group by brands,state;
                     '''
            df = pd.read_sql(query, engine)
            vis_type = st.sidebar.selectbox('select visualization type', options=['Bar plot', 'pie plot'])
            if vis_type == 'Bar plot':
                fig = px.bar(df, x='brands', y='No of Users', color='brands',
                             labels={'brands': 'Brands', 'No of Users': 'Number of Users'},
                             title=f'Overall number of users by brands in {states} in the year {history}')
                st.plotly_chart(fig)
            else:
                fig = px.pie(df, values='No of Users', names='brands',
                             title=f'Number of Users per Brand in {states}',
                             labels={'brands': 'Brands', 'No of Users': 'Number of Users'})
                st.plotly_chart(fig)

        else:
            vis_type = st.sidebar.selectbox('select visualization type', options=['Bar plot', 'pie plot'])
            sub_query1 = 'select distinct(state) as state from agg_transaction'
            sub_df1 = pd.read_sql(sub_query1, engine)
            state_list = sub_df1['state']
            states = st.sidebar.selectbox('select the state', options=state_list)
            query = f'''
                                 select state,brands,sum(count) as 'No of Users' from agg_users
                                 where state='{states}' and year={history} group by brands,state;
                                 '''
            df = pd.read_sql(query, engine)
            if vis_type == 'Bar plot':
                fig = px.bar(df, x='brands', y='No of Users', color='brands',
                             labels={'brands': 'Brands', 'No of Users': 'Number of Users'},
                             title=f'Overall number of users by brands in {states}')

                # Display the bar chart
                st.plotly_chart(fig)
            else:
                fig = px.pie(df, values='No of Users', names='brands',
                             title=f'Number of Users per Brand in the year {history}',
                             labels={'brands': 'Brands', 'No of Users': 'Number of Users'})

                # Display the pie chart using Streamlit
                st.plotly_chart(fig)
if selected == 'Geographic Analysis':
    metrics = st.sidebar.selectbox('Select the metric', options=['Transaction_amount', 'transaction count', 'users'])
    if metrics == 'Transaction_amount':
        all_states = [
            'Andaman and Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
            'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Puducherry', 'Punjab', 'Rajasthan',
            'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ]

        # Sidebar options and user selections
        perf_choice = st.sidebar.selectbox('Choose the performance metric:', options=['Best', 'Worst'])
        result = 'desc' if perf_choice == 'Best' else 'asc'
        year = st.sidebar.selectbox('Select the year', options=[2018, 2019, 2020, 2021, 2022, 2023])
        top_values = st.sidebar.slider('Select N', min_value=1, max_value=10, value=5)

        # SQL Query to fetch data
        query = f'''
                SELECT state, SUM(transaction_amount) AS 'Total Transaction'
                FROM agg_transaction
                WHERE year = {year}
                GROUP BY state
                ORDER BY SUM(transaction_amount) {result}
                LIMIT {top_values};
            '''

        # Read data into DataFrame
        df = pd.read_sql(query, engine)

        # Load GeoJSON file for Indian states
        with open(
                'C:/Users/akash/PycharmProjects/PhonePe pulse visualization/Phonepe-Pulse-Data-Visualization-and-Exploration/Indian_States.json') as f:
            india_states = json.load(f)

        # Convert state names to title case (if needed)
        new_lists = []
        lists = df['state']
        for i in lists:
            if i == 'odisha':
                i = 'Orissa'
            elif i == 'dadra-&-nagar-haveli-&-daman-&-diu':
                i = 'Dadra and Nagar Haveli'
            elif i == 'andaman-&-nicobar-islands':
                i = 'Andaman and Nicobar'
            strs = ''
            for j in i:
                if j == '-':
                    strs += ' '
                else:
                    strs += j
            new_lists.append(strs.title())
        df['state'] = new_lists
        # Create a DataFrame with all states and default Total Transaction value
        all_states_df = pd.DataFrame(all_states, columns=['state'])
        all_states_df['Total Transaction'] = 0  # Default value for non-selected states

        # Merge the DataFrame with SQL results
        merged_df = all_states_df.merge(df, on='state', how='left', suffixes=('default', ''))
        merged_df['Total Transaction'] = merged_df['Total Transaction'].fillna(0)  # Fill NaNs with default value

        # Create choropleth map
        fig = px.choropleth(
            merged_df,
            geojson=india_states,
            featureidkey='properties.NAME_1',  # Adjust according to your GeoJSON file
            locations='state',
            color='Total Transaction',
            color_continuous_scale='Viridis',
            projection='mercator'
        )

        # Update layout
        fig.update_geos(
            fitbounds="locations",
            visible=False
        )

        fig.update_layout(
            title='Transaction Map of Indian States',
            title_x=0.25,  # Center the title
            geo=dict(
                lakecolor='rgb(255, 255, 255)'
            )
        )

        # Display the choropleth map
        st.plotly_chart(fig)
    elif metrics == 'transaction count':
        all_states = [
            'Andaman and Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
            'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Puducherry', 'Punjab', 'Rajasthan',
            'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ]

        # Sidebar options and user selections
        perf_choice = st.sidebar.selectbox('Choose the performance metric:', options=['Best', 'Worst'])
        result = 'desc' if perf_choice == 'Best' else 'asc'
        year = st.sidebar.selectbox('Select the year', options=[2018, 2019, 2020, 2021, 2022, 2023])
        top_values = st.sidebar.slider('Select N', min_value=1, max_value=10, value=5)

        # SQL Query to fetch data
        query = f'''
                        select state,sum(transaction_count) as 'total_transaction_count' from top_trans 
                        where year = {year} group by state
                        order by sum(transaction_count) {result}
                        limit {top_values};
                    '''

        # Read data into DataFrame
        df = pd.read_sql(query, engine)

        # Load GeoJSON file for Indian states
        with open(
                'C:/Users/akash/PycharmProjects/PhonePe pulse visualization/Phonepe-Pulse-Data-Visualization-and-Exploration/Indian_States.json') as f:
            india_states = json.load(f)

        # Convert state names to title case (if needed)
        new_lists = []
        lists = df['state']
        for i in lists:
            if i == 'odisha':
                i = 'Orissa'
            elif i == 'dadra-&-nagar-haveli-&-daman-&-diu':
                i = 'Dadra and Nagar Haveli'
            elif i == 'andaman-&-nicobar-islands':
                i = 'Andaman and Nicobar'
            strs = ''
            for j in i:
                if j == '-':
                    strs += ' '
                else:
                    strs += j
            new_lists.append(strs.title())
        df['state'] = new_lists
        # Create a DataFrame with all states and default Total Transaction value
        all_states_df = pd.DataFrame(all_states, columns=['state'])
        all_states_df['total_transaction_count'] = 0  # Default value for non-selected states

        # Merge the DataFrame with SQL results
        merged_df = all_states_df.merge(df, on='state', how='left', suffixes=('default', ''))
        merged_df['total_transaction_count'] = merged_df['total_transaction_count'].fillna(
            0)  # Fill NaNs with default value

        # Create choropleth map
        fig = px.choropleth(
            merged_df,
            geojson=india_states,
            featureidkey='properties.NAME_1',  # Adjust according to your GeoJSON file
            locations='state',
            color='total_transaction_count',
            color_continuous_scale='Viridis',
            projection='mercator'
        )

        # Update layout
        fig.update_geos(
            fitbounds="locations",
            visible=False
        )

        fig.update_layout(
            title='Total Transaction Count Map of Indian States',
            title_x=0.25,  # Center the title
            geo=dict(
                lakecolor='rgb(255, 255, 255)'
            )
        )

        # Display the choropleth map
        st.plotly_chart(fig)

    else:
        all_states = [
            'Andaman and Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
            'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Puducherry', 'Punjab', 'Rajasthan',
            'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ]

        # Sidebar options and user selections
        perf_choice = st.sidebar.selectbox('Choose the performance metric:', options=['Best', 'Worst'])
        result = 'desc' if perf_choice == 'Best' else 'asc'
        year = st.sidebar.selectbox('Select the year', options=[2018, 2019, 2020, 2021, 2022, 2023])
        top_values = st.sidebar.slider('Select N', min_value=1, max_value=10, value=5)

        # SQL Query to fetch data
        query = f'''
                select state,sum(registered_users) as total_user from top_user 
                where year={year} group by state 
                order by sum(registered_users) {result} 
                limit {top_values};
            '''

        # Read data into DataFrame
        df = pd.read_sql(query, engine)

        # Load GeoJSON file for Indian states
        with open(
                'C:/Users/akash/PycharmProjects/PhonePe pulse visualization/Phonepe-Pulse-Data-Visualization-and-Exploration/Indian_States.json') as f:
            india_states = json.load(f)

        # Convert state names to title case (if needed)
        new_lists = []
        lists = df['state']
        for i in lists:
            if i == 'odisha':
                i = 'Orissa'
            elif i == 'dadra-&-nagar-haveli-&-daman-&-diu':
                i = 'Dadra and Nagar Haveli'
            elif i == 'andaman-&-nicobar-islands':
                i = 'Andaman and Nicobar'
            strs = ''
            for j in i:
                if j == '-':
                    strs += ' '
                else:
                    strs += j
            new_lists.append(strs.title())
        df['state'] = new_lists
        # Create a DataFrame with all states and default Total Transaction value
        all_states_df = pd.DataFrame(all_states, columns=['state'])
        all_states_df['total_user'] = 0  # Default value for non-selected states

        # Merge the DataFrame with SQL results
        merged_df = all_states_df.merge(df, on='state', how='left', suffixes=('default', ''))
        merged_df['total_user'] = merged_df['total_user'].fillna(0)  # Fill NaNs with default value

        # Create choropleth map
        fig = px.choropleth(
            merged_df,
            geojson=india_states,
            featureidkey='properties.NAME_1',  # Adjust according to your GeoJSON file
            locations='state',
            color='total_user',
            color_continuous_scale='Viridis',
            projection='mercator'
        )

        # Update layout
        fig.update_geos(
            fitbounds="locations",
            visible=False
        )

        fig.update_layout(
            title='Registered Users Map of Indian States',
            title_x=0.25,  # Center the title
            geo=dict(
                lakecolor='rgb(255, 255, 255)'
            )
        )

        # Display the choropleth map
        st.plotly_chart(fig)

# MENU 4 - ABOUT
if selected == "About":
    st.markdown("# :sparkles: About")
    st.markdown("## :computer: Domain: **Fintech**")
    st.markdown("## :bulb: Technologies Used")
    st.markdown("- **Github Cloning**")
    st.markdown("- **Python**")
    st.markdown("- **Pandas**")
    st.markdown("- **MySQL**")
    st.markdown("- **SQLAlchemy**")
    st.markdown("- **Streamlit**")
    st.markdown("- **Plotly**")

    st.markdown("## :bar_chart: Overview")
    st.markdown(
        "Explore PhonePe Pulse data with interactive visualizations to uncover insights about transactions, users, top states, districts, pincodes, and popular brands.")

    st.markdown("### :mag: Insights You Can Gain:")
    st.markdown("- **Top 10 states, districts, and pincodes by transactions**")
    st.markdown("- **Analysis of user demographics and behaviors**")
    st.markdown("- **Visualizations including bar charts, pie charts, and geographical maps**")

    st.markdown("### :rocket: Features")
    st.markdown("- Visualize trends and patterns in transaction data")
    st.markdown("- Analyze user engagement and geographical distribution")
    st.markdown("- Gain actionable insights for business decisions")

    st.markdown("### :bulb: Why It Matters")
    st.markdown(
        "Understanding transaction trends and user behavior is crucial for optimizing business strategies in the fintech industry.")

    st.markdown("### :eyes: Get Started")
    st.markdown("Explore the interactive charts and maps to discover valuable insights from PhonePe Pulse data!")
