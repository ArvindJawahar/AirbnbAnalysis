import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

# SETTING PAGE CONFIGURATIONS
st.set_page_config(page_title="AirBnb-Analysis | By ArvindJawahar",
                   page_icon=Image.open(r"D:\PythonProject_Airbnb\logo\airbnb.png"),
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This AirBnb-Analysis app is created by *ArvindJawahar*!"""})

#Page Visualization
st.image(Image.open(r"D:\PythonProject_Airbnb\logo\airbnb_analysis.jpg"), width=1000)
select = option_menu(menu_title="", options=["🏠 Home", "📊 Explore Data", "📄 About Project"], default_index=0, orientation="horizontal")

#----------------Home----------------------#

if select == "🏠 Home":

     st.markdown('# Airbnb Analysis')
     st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
     st.markdown('# Skills take away From This Project:')
     st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
     st.markdown('# Domain:')
     st.subheader('Travel Industry, Property management and Tourism')

if select == "📊 Explore Data":
     fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
     if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(fl, encoding="ISO-8859-1")
     else:
         st.warning("Please upload a file to proceed.")
         st.stop()
     st.sidebar.header("Choose your filter: ")

     # Create for neighbourhood_group
     neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
     if not neighbourhood_group:
         df2 = df.copy()
     else:
         df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

     # Create for neighbourhood
     neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
     if not neighbourhood:
         df3 = df2.copy()
     else:
         df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

     # Filter the data based on neighbourhood_group, neighbourhood

     if not neighbourhood_group and not neighbourhood:
         filtered_df = df
     elif not neighbourhood:
         filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
     elif not neighbourhood_group:
         filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
     elif neighbourhood:
         filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
     elif neighbourhood_group:
         filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
     elif neighbourhood_group and neighbourhood:
         filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
     else:
         filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

     room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

     col1, col2 = st.columns(2)
     with col1:
        st.subheader("Room_type_ViewData")
        fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                     template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

     with col2:
        st.subheader("Neighbourhood_group_ViewData")
        fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
        fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

     cl1, cl2 = st.columns((2))
     with cl1:
        with st.expander("Room_type wise price"):
            st.write(room_type_df.style.background_gradient(cmap="Blues"))
            csv = room_type_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

     with cl2:
        with st.expander("Neighbourhood_group wise price"):
            neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
            st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
            csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

     # Create a scatter plot
     data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
     data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                            titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                            yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
     st.plotly_chart(data1, use_container_width=True)

     with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
         st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

     # Download orginal DataSet
     csv = df.to_csv(index=False).encode('utf-8')
     st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

     import plotly.figure_factory as ff

     st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
     with st.expander("Summary_Table"):
        df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

     # map function for room_type

    # If your DataFrame has columns 'Latitude' and 'Longitude':
     st.subheader("Airbnb Analysis in Map view")
     df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

     st.map(df)

 # ----------------------Contact---------------#

if select == "📄 About Project":
     Name = (f'{"Name :"}  {"ARVINDJAWAHAR A"}')
     mail = (f'{"Mail :"}  {"arvindjawahar@protonmail.com"}')
     description = "An Aspiring DATA-SCIENTIST..!"
     social_media = {
                     "GITHUB": "https://github.com/ArvindJawahar",
                     "LINKEDIN": "https://in.linkedin.com/in/arvindjawahar-a-95607626b/"
                    }

     # col1,
     # col1.image(Image.open("C:\\Users\\arunk\\OneDrive\\Desktop\\passpoer size photo.jpg"), width=300)

     # with col1:
     st.header('Airbnb Analysis')
     st.subheader(
         "This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
     st.write("---")
     st.subheader(Name)
     st.subheader(mail)

     st.write("#")
     cols = st.columns(len(social_media))
     for index, (platform, link) in enumerate(social_media.items()):
         cols[index].write(f"[{platform}]({link})")