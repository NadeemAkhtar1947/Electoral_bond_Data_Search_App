import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# Add a Markdown component to display the greeting
st.markdown("### Hi, My name is Nadeem and this app is developed by me")

links_row = "<a href='https://www.linkedin.com/in/nadeem-akhtar-/' target='_blank'>" \
            "<img src='https://img.icons8.com/color/48/000000/linkedin.png' width='30'></a>" \
            " | " \
            "<a href='https://github.com/NadeemAkhtar1947' target='_blank'>" \
            "<img src='https://img.icons8.com/color/48/000000/github.png' width='30'></a>" \
            " | " \
            "<a href='https://www.kaggle.com/mdnadeemakhtar/code' target='_blank'>" \
            "<img src='https://www.kaggle.com/static/images/site-logo.png' width='30'></a>" \
            " | " \
            "<a href='https://tyrex.netlify.app/' target='_blank'>" \
            "<img src='https://img.icons8.com/color/48/000000/globe--v1.png' width='30'></a>"

# Display the links row using Markdown
st.markdown(links_row, unsafe_allow_html=True)



# Function to increment view count
def increment_views():
    # Read current view count from file
    try:
        with open("view_count.txt", "r") as file:
            views = int(file.read())
    except FileNotFoundError:
        # If file doesn't exist, initialize view count to 0
        views = 0

    # Increment view count
    views += 1

    # Write updated view count to file
    with open("view_count.txt", "w") as file:
        file.write(str(views))

    return views

# Increment view count only once per user visit
if not st.session_state.get("view_counted", False):
    total_views = increment_views()
    st.session_state.view_counted = True
else:
    total_views = int(open("view_count.txt", "r").read())

# Display total views
st.write("Total Views:", total_views)

# Your Streamlit app code goes here...









merged_df = pd.read_csv("merged_file.csv")

merged_df.rename(columns={'Date of\rEncashment':'Redeemed date', 'Account no. of\rPolitical Party' :'Account No.', 'Denominations_x':'Denominations', 'Date of\rPurchase':'Purchase date','Name of the Purchaser':'company','Status':'status'}, inplace=True)
df = merged_df[['Bond Number','Redeemed date','Political Party','Account No.','Denominations','Purchase date','company','status']]
# Convert denomination to crore
df['Denominations'] = df['Denominations'] / 1e7

# Rename the column
df.rename(columns={'Denominations': 'Denomination (Crore)'}, inplace=True)

###--------------------------------------------###
# Convert 'Redeemed date' to datetime format
df['Redeemed date'] = pd.to_datetime(df['Redeemed date'])

# Extract year from 'Redeemed date' and create a new column
df['Year'] = df['Redeemed date'].dt.year

# group by 'Year' and 'party' and take sum of denomination in a year
df_year_party = df.groupby(['Year', 'Political Party'])['Denomination (Crore)'].sum().reset_index()

###-----------------------------------------------###
# Convert 'Redeemed date' to datetime format
df['Purchase date'] = pd.to_datetime(df['Purchase date'])

# Extract year from 'Redeemed date' and create a new column
df['Year'] = df['Purchase date'].dt.year

# group by 'Year' and 'party' and take sum of denomination in a year
df_year_company = df.groupby(['Year', 'company'])['Denomination (Crore)'].sum().reset_index().sort_values(by='Denomination (Crore)',ascending=False)

###----------------------------------------###

st.sidebar.title("Electoral Bond Analysis")
st.sidebar.image("download.jpg")
# Create a selectbox for choosing between party wise and Winter company wise
select_analysis = st.sidebar.selectbox("Select Analysis", ("Party wise", "Company wise"))

# Define options for both party wise and company wise
party_wise = ('Top party by donations', 'donation distribution by party', 'party wise donations', 'Year wise Party Analysis','Overall Party Analysis')
company_wise = ('Top company by donations', 'donation distribution by company', 'company wise donations', 'Year wise company Analysis', 'Overall company Analysis')


# Display options based on the selected analysis
if select_analysis == "Party wise":
    user_menu = st.sidebar.radio('Select an option', party_wise, key="party_radio")

    if user_menu == 'Top party by donations':
        st.subheader('Top Political Party by donations')
        party_totals = df.groupby('Political Party')['Denomination (Crore)'].sum().reset_index().sort_values(
            by='Denomination (Crore)', ascending=False)

        # Display the total amount for each party
        st.write(party_totals)

        party_donations = df.groupby('Political Party')['Denomination (Crore)'].sum()
        # Sort party names based on total donation amounts in descending order
        sorted_parties = party_donations.sort_values(ascending=False).index
        # Display select box with sorted party names
        selected_party_name = st.selectbox('Enter a Party name', sorted_parties)
        if selected_party_name:
            st.subheader(f"All Companies donated to {selected_party_name}")

        def top_donations_by_party(df, selected_party_name, n=400):
            party_df = df[df['Political Party'] == selected_party_name]
            company_donations = party_df.groupby('company')['Denomination (Crore)'].sum()
            top_donations = company_donations.sort_values(ascending=False).head(n)
            return top_donations
        top_donations = top_donations_by_party(df, selected_party_name)
        st.write(top_donations)


    # Calculate donation totals by party
    if user_menu == 'donation distribution by party':
        st.subheader('Donation Distribution by Political Party')
        party_totals = df.groupby('Political Party')['Denomination (Crore)'].sum().reset_index().sort_values(
            by='Denomination (Crore)', ascending=False)

        # Create pie chart
        fig_pie = px.pie(party_totals, values='Denomination (Crore)', names='Political Party',
                     title='Electoral Bond Distribution by Political Party (pie plot)',
                     hover_data=['Denomination (Crore)'],
                     labels={'Denomination (Crore)': 'Denomination (Crore)'},
                     hole=0.5,
                     width=800,
                     height=600)

        # Display the pie chart
        st.plotly_chart(fig_pie)

    # Create bar chart
        fig_bar = px.bar(party_totals, x='Political Party', y='Denomination (Crore)',
                     title='Electoral Bond Distribution by party (bar plot)',
                     color='Political Party',
                     hover_data=['Denomination (Crore)'],
                     labels={'Denomination (Crore)': 'Denomination (Crore)'},
                     width=1000,
                     height=700)

        # Display the bar chart
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar)

    if user_menu == 'party wise donations':
        # Calculate total donation amounts for each party
        party_donations = df.groupby('Political Party')['Denomination (Crore)'].sum()
        # Sort party names based on total donation amounts in descending order
        sorted_party = party_donations.sort_values(ascending=False).index
        # Display select box with sorted party names
        selected_party = st.selectbox('Enter a Party name', sorted_party, key='selected_party')
        if selected_party:
            st.subheader(f"Top 20 companies donations to {selected_party}")
        def top_donations_by_party(df, selected_party, n=20):
            party_df = df[df['Political Party'] == selected_party]
            company_donations = party_df.groupby('company')['Denomination (Crore)'].sum()
            top_donations = company_donations.sort_values(ascending=False).head(n)
            return top_donations
        top_donations = top_donations_by_party(df, selected_party)
        st.write(top_donations)

        # Create pie chart
        fig_pie = px.pie(top_donations.reset_index(), values='Denomination (Crore)', names=top_donations.index,
                    title=f'Top 20 companies Donations to {selected_party}',
                     hole = 0.5,width = 800,height = 600)

        st.plotly_chart(fig_pie)
        # Create bar chart
        fig_bar = px.bar(top_donations.reset_index(), x='company', y='Denomination (Crore)',
                         title=f'Top 20 companies Donations to {selected_party}',
                         labels={'company': 'Company', 'Denomination (Crore)': 'Total Donation (Crore)'},
                         width=800,
                         height=700,
                         color='company', color_discrete_sequence=px.colors.qualitative.Plotly)
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar)

    if user_menu == 'Year wise Party Analysis':
        st.subheader("Year wise donations to each party")
        st.write(df_year_party)
        def get_details_by_year_party(df_year_party, year, party):
            filtered_df = df_year_party[(df_year_party['Year'] == year) & (df_year_party['Political Party'] == party)]

            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        year = df_year_party['Year'].unique()
        party = df_year_party['Political Party'].unique()
        selected_year = st.selectbox("Select Year", year)
        selected_party = st.selectbox("Select Party", party)
        details = get_details_by_year_party(df_year_party, selected_year, selected_party)
        st.subheader(f"{selected_party} got donations in {selected_year}")
        st.write(details)

        def get_details_by_year_party(df_year_party, party):
            filtered_df = df_year_party[(df_year_party['Political Party'] == party)]
            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        political_party = df_year_party['Political Party'].unique()
        select_political_party = st.selectbox("Select political party", political_party)
        details = get_details_by_year_party(df_year_party, select_political_party)
        party_denominations = details[details['Denomination (Crore)'] > 0]
        st.write(party_denominations)

        fig = px.line(details, x='Year', y='Denomination (Crore)', hover_name='Year',
                      title=f'Denomination to {select_political_party} Over the Years',
                      labels={'Year': 'Year', 'Denomination (Crore)': 'Denomination (Crore)'},
                      color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig)


    if user_menu == 'Overall Party Analysis':
        def get_details_by_year_party(df_year_party, year, party):
            filtered_df = df_year_party[(df_year_party['Year'] == year) & (df_year_party['Political Party'] == party)]

            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        year = df_year_party['Year'].unique()
        party = df_year_party['Political Party'].unique()
        selected_year = st.selectbox("Select Year", year)
        selected_party = st.selectbox("Select Party", party)
        details = get_details_by_year_party(df_year_party, selected_year, selected_party)
        st.subheader(f"{selected_party} got donations in {selected_year}")
        st.write(details)

        def get_details_by_year_party(df_year_party, party):
            filtered_df = df_year_party[(df_year_party['Political Party'] == party)]
            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        political_party = df_year_party['Political Party'].unique()
        select_political_party = st.selectbox("Select political party", political_party)
        details = get_details_by_year_party(df_year_party, select_political_party)
        party_denominations = details[details['Denomination (Crore)'] > 0]
        st.write(party_denominations)

        fig = px.line(details, x='Year', y='Denomination (Crore)', hover_name='Year',
                      title=f'Denomination to {select_political_party} Over the Years',
                      labels={'Year': 'Year', 'Denomination (Crore)': 'Denomination (Crore)'},
                      color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig)


# Display options based on the selected season
else:
    user_menu = st.sidebar.radio('Select an option', company_wise, key="company_radio")

    if user_menu == 'Top company by donations':
        st.subheader('Top 500 Company by Donations')
        company_totals = df.groupby('company')['Denomination (Crore)'].sum().reset_index().sort_values(
            by='Denomination (Crore)', ascending=False)
        # Display the total amount for each company
        top_500 = company_totals.head(500)
        # Display the total amount for each party
        st.write(top_500)

    if user_menu == 'donation distribution by company':
        st.subheader('Donation Distribution by Company')
        company_totals = df.groupby('company')['Denomination (Crore)'].sum().reset_index().sort_values(
            by='Denomination (Crore)', ascending=False)
        # Display the total amount for each company
        top_50 = company_totals.head(50)
        # Create pie chart
        fig_pie = px.pie(top_50, values='Denomination (Crore)', names='company',
                     title='Top 50 Bond Purchaser (pie plot)',
                     hover_data=['Denomination (Crore)'],
                     labels={'Denomination (Crore)': 'Denomination (Crore)'},
                     hole=0.5,width=700,height=500)

        # Display the pie chart
        st.plotly_chart(fig_pie)

        # Create bar chart
        fig_bar = px.bar(top_50, x='company', y='Denomination (Crore)',
                     title='Top 50 Bond Purchaser (bar plot)',
                     color='company',
                     hover_data=['Denomination (Crore)'],
                     labels={'Denomination (Crore)': 'Denomination (Crore)'},
                     width=800,
                     height=600)

        # Display the bar chart
        st.plotly_chart(fig_bar)

    if user_menu == 'company wise donations':
        # Calculate total donation amounts for each party
        company_donations = df.groupby('company')['Denomination (Crore)'].sum()

        # Sort party names based on total donation amounts in descending order
        sorted_companies = company_donations.sort_values(ascending=False).index

        # Display select box with sorted party names
        selected_company_name = st.selectbox('Enter a Company name', sorted_companies)

        # Check if a party name is selected
        if selected_company_name:
            st.subheader(f"{selected_company_name} Donated to the following Party")

        def top_donations_by_company(df, selected_company_name, n=20):
            company_df = df[df['company'] == selected_company_name]
            company_donations = company_df.groupby('Political Party')['Denomination (Crore)'].sum()
            top_donations = company_donations.sort_values(ascending=False).head(n)
            return top_donations

        top_donations = top_donations_by_company(df, selected_company_name)
        st.write(top_donations)

        # Create pie chart
        fig_pie = px.pie(top_donations.reset_index(), values='Denomination (Crore)', names=top_donations.index,
                    title=f'{selected_company_name} Donated to the following Party',
                     hole = 0.5,width = 800,height = 600)

        st.plotly_chart(fig_pie)
        # Create bar chart
        fig_bar = px.bar(top_donations.reset_index(), x = 'Political Party', y='Denomination (Crore)',
                         title=f'{selected_company_name} Donated to the following Party',
                         labels={'Political Party': 'Political Party', 'Denomination (Crore)': 'Total Donation (Crore)'},
                         width=800,
                         height=700,
                         color='Political Party', color_discrete_sequence=px.colors.qualitative.Plotly)
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar)


    if user_menu == 'Year wise company Analysis':
        st.subheader("Year wise donations by each company")
        st.write(df_year_company)
        def get_details_by_year_party(df_year_company, year, company):
            filtered_df = df_year_company[(df_year_company['Year'] == year) & (df_year_company['company'] == company)]

            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        year = df_year_company['Year'].unique()
        company = df_year_company['company'].unique()
        selected_year = st.selectbox("Select Year", year)
        selected_company_1 = st.selectbox("Select company", company, key="select_company_1")
        details = get_details_by_year_party(df_year_company, selected_year, selected_company_1)
        st.subheader(f"{selected_company_1} give donations in {selected_year}")
        st.write(details)

        def get_details_by_year_party(df_year_company, company):
            filtered_df = df_year_company[(df_year_company['company'] == company)]
            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df

        com = df_year_company['company'].unique()
        select_company= st.selectbox("Select company", com)
        details = get_details_by_year_party(df_year_company, select_company)
        company_denominations = details[details['Denomination (Crore)'] > 0]
        st.write(company_denominations)

        fig = px.line(details, x='Year', y='Denomination (Crore)', hover_name='Year',
                      title=f'Denomination to {select_company} Over the Years',
                      labels={'Year': 'Year', 'Denomination (Crore)': 'Denomination (Crore)'},
                      color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig)


    if user_menu == 'Overall company Analysis':
        def get_details_by_year_party(df_year_company, year, company):
            filtered_df = df_year_company[(df_year_company['Year'] == year) & (df_year_company['company'] == company)]

            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        year = df_year_company['Year'].unique()
        company = df_year_company['company'].unique()
        selected_year = st.selectbox("Select Year", year)
        selected_company_3 = st.selectbox("Select Bond Purchaser", company, key="select_company_3")
        details = get_details_by_year_party(df_year_company, selected_year, selected_company_3)
        st.subheader(f"{selected_company_3} give donations in {selected_year}")
        st.write(details)

        def get_details_by_year_party(df_year_company, company):
            filtered_df = df_year_company[(df_year_company['company'] == company)]
            # Sort the filtered DataFrame by 'Denomination (Crore)' in descending order
            filtered_df = filtered_df.sort_values(by='Denomination (Crore)', ascending=False)

            return filtered_df
        com = df_year_company['company'].unique()
        select_company = st.selectbox("Select company", com)
        details = get_details_by_year_party(df_year_company, select_company)
        company_denominations = details[details['Denomination (Crore)'] > 0]
        st.write(company_denominations)

        fig = px.line(details, x='Year', y='Denomination (Crore)', hover_name='Year',
                      title=f'Denomination to {select_company} Over the Years',
                      labels={'Year': 'Year', 'Denomination (Crore)': 'Denomination (Crore)'},
                      color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig)


# Add custom text at the bottom using Markdown
st.markdown("---")
st.markdown("Copyright © Nadeem Akhtar. All Rights Reserved")




