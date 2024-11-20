# Import Library
import pandas as pd
import numpy as np
import streamlit as st
import datetime

# Loading data set
df = pd.read_excel("nuclear_explosions.xlsx")

# checking Null values
df.isnull().sum()

# Creating dictionary For rename header
df = df.rename(columns={
   "Data.Source": "Source",
   "Location.Cordinates.Latitude": "Latitude",
   "Location.Cordinates.Longitude": "Longitude",
   "Data.Magnitude.Body": "Magnitude_Body",
   "Data.Magnitude.Surface": "Magnitude_Surface",
   "Location.Cordinates.Depth": "Depth",
   "Data.Yeild.Lower": "Yeild_Lower",
   "Data.Yeild.Upper": "Yeild_Upper",
   "Data.Purpose": "Purpose",
   "Data.Name": "Name",
   "Data.Type": "Type",
   "Date.Day": "Day",
   "Date.Month": "Month",
   "Date.Year": "Year"
})

print(df.head(5))

# Dictionary to map misspelled names to the correct ones
location_corrections = {
    "Amchitka Ak": "Amchitka",
    "Arkhan Russ": "Arkhangelsk",
    "Astrak Russ": "Astrakhan",
    "Azgie Kazakh": "Azgir",
    "Azgir Kazakh": "Azgir",
    "Bashki Russ": "Bashkiria",
    "Bashkir Russ": "Bashkiria",
    "C. Nevada": "Central Nevada",
    "Carlsbad Nm": "Carlsbad",
    "Chita Russ": "Chita",
    "Christmas Is": "Christmas Island",
    "Emu Austr": "Emu",
    "Fallon Nv": "Fallon",
    "Fangataufa": "Fangataufa",
    "Fangataufaa": "Fangataufa",
    "Farmingt Nm": "Farmington",
    "Grand V Co": "Grand Valley",
    "Hattiesb Ms": "Hattiesburg",
    "Hattiese Ms": "Hattiesburg",
    "Htr Russ": "Hitler Region",
    "Hururoa": "Mururoa",
    "In Ecker Alg": "In Ekker",
    "Irkuts Russ": "Irkutsk",
    "Jakuts Ruse": "Yakutsk",
    "Jakuts Russ": "Yakutsk",
    "Johnston Is": "Johnston Island",
    "Kalmyk Russ": "Kalmykia",
    "Kazakh": "Kazakhstan",
    "Kazakhstan": "Kazakhstan",
    "Kemero Russ": "Kemerovo",
    "Komi Russ": "Komi",
    "Krasno Russ": "Krasnoyarsk",
    "Kz Russ": "Kazakhstan",
    "Malden Is": "Malden Island",
    "Mangy Kazakh": "Mangyshlak",
    "Marali Austr": "Maralinga",
    "Mary Turkmen": "Mary",
    "Mellis Nv": "Mellis",
    "Monteb Austr": "Monte Bello",
    "Mtr Russ": "Murmansk",
    "Mueueoa": "Mururoa",
    "Murm Russ": "Murmansk",
    "Murueoa": "Mururoa",
    "Muruhoa": "Mururoa",
    "Mururoa": "Mururoa",
    "N2 Russ": "N2 Region",
    "Nellis Nv": "Nellis",
    "Nz Russ": "New Zealand Region",
    "Offuswcoast": "Off US West Coast",
    "Orenbg Russ": "Orenburg",
    "Pamuk Uzbek": "Pamuk",
    "Perm Russ": "Perm",
    "Reggane Alg": "Reggane",
    "Rifle Co": "Rifle",
    "S. Atlantic": "South Atlantic",
    "S.Atlantic": "South Atlantic",
    "Semi Kazakh": "Semipalatinsk",
    "Stavro Russ": "Stavropol",
    "Tuymen Russ": "Tyumen",
    "Tyumen Russ": "Tyumen",
    "Ukeaine": "Ukraine",
    "Uzbek": "Uzbekistan",
    "W Kazakh": "West Kazakhstan",
    "W Mururoa": "West Mururoa",
    "Wsw Mururoa": "West-Southwest Mururoa",
}

df["WEAPON DEPLOYMENT LOCATION"] = df["WEAPON DEPLOYMENT LOCATION"].replace(location_corrections)


# Dictionary to map purpose abbreviations to full descriptions
purpose_descriptions = {
    "Combat": "Combat Detonation",
    "Fms": "Function Material Study",
    "Fms/Wr": "Function Material Study and Weapon-Related",
    "Me": "Military Exercise",
    "Nan": "Unknown Purpose",
    "Pne": "Peaceful Nuclear Explosion",
    "Pne/Wr": "Peaceful Nuclear Explosion and Weapon-Related",
    "Pne:Plo": "Peaceful Nuclear Explosion for Plowshare Program",
    "Pne:V": "Peaceful Nuclear Explosion for Venting",
    "Sam": "Subatomic Measurement",
    "Sb": "Safety Burst",
    "Se": "Structural Engineering",
    "Se/Wr": "Structural Engineering and Weapon-Related",
    "Transp": "Transportation Testing",
    "We": "Weapon Experimentation",
    "We/Sam": "Weapon Experimentation and Subatomic Measurement",
    "We/Wr": "Weapon Experimentation and Weapon-Related",
    "Wr": "Weapon-Related",
    "Wr/F/S": "Weapon-Related Function Study",
    "Wr/F/Sa": "Weapon-Related Function Study with Safety Analysis",
    "Wr/Fms": "Weapon-Related Function Material Study",
    "Wr/P/S": "Weapon-Related with Peaceful and Safety Analysis",
    "Wr/P/Sa": "Weapon-Related with Peaceful and Safety Analysis",
    "Wr/Pne": "Weapon-Related Peaceful Nuclear Explosion",
    "Wr/Sam": "Weapon-Related Subatomic Measurement",
    "Wr/Se": "Weapon-Related Structural Engineering",
    "Wr/We": "Weapon-Related Weapon Experimentation",
    "Wr/We/S": "Weapon-Related Weapon Experimentation with Safety Analysis",
}

# Apply mapping to the Purpose column
df["Purpose"] = df["Purpose"].replace(purpose_descriptions)


# Dictionary to map abbreviations or inconsistent values to standardized full names
type_corrections = {
    "Atmosph": "Atmospheric",
    "Shaft/Gr": "Shaft Ground-Based",
    "Shaft/Lg": "Shaft Large",
    "Ship": "Ship-Based",
    "Space": "Space-Based",
    "Surface": "Surface",
    "Tower": "Tower",
    "Tunnel": "Tunnel",
    "Ug": "Underground",
    "Uw": "Underwater",
    "Water Su": "Water Surface",
    "Watersur": "Water Surface",
}

# Apply mapping to the Type column
df["Type"] = df["Type"].replace(type_corrections)


# Using Lamdba function Calculation
df["Magnitude_Category"] = df["Magnitude_Body"].apply(
    lambda x: "High" if x > 5 else ("Moderate" if x > 3 else "Low")
)


# List comprehension: High-yield explosions
high_yield_explosions = [
    name for name, yield_upper in zip(df['Name'], df['Yeild_Upper']) if yield_upper > 1000
]
# st.write("Significant Explosions (Yield > 1000kt):", high_yield_explosions)


# Extract Week number of year from date
df['Date'] = pd.to_datetime(df[['Day', 'Month', 'Year']])
df['Week_of_Year'] = df['Date'].dt.isocalendar().week

# Dispaly data set
st.title("Nuclear Explosions(1945 - 1998) Analysis")
st.write("An Overview of the Dataset")
st.write(df.head())

# Side bar
st.sidebar.title("Filter Option")
location = df['WEAPON DEPLOYMENT LOCATION'].unique()
select_location = st.sidebar.multiselect("Select Deployment Location",location,default=["Bikini"])

#year
year_min =int(df['Year'].min())
year_max =int(df['Year'].max())
year_range = st.sidebar.slider("Year Range",year_min,year_max,(year_max,year_min))

# yeild
yield_min = int(df['Yeild_Lower'].min())
yield_max = int(df['Yeild_Lower'].max())
yield_range = st.sidebar.slider("Yeild Range",yield_max,yield_min,(yield_min,yield_max))

#Depth Selection
depth_selction = ["Above Ground", "Underground","All"]
select_depth = st.sidebar.radio("Select Depth",depth_selction)

# image
st.sidebar.image("Header.jpeg")

# Part secound 
def filter_data(df,location,year_range,yield_range,depth):
    filter_data = df[df["WEAPON DEPLOYMENT LOCATION"].isin(location)]
    
    filter_data = filter_data[(filter_data["Year"]>=year_range[0])&
                                (filter_data["Year"]<=year_range[1])]
    
    
    filter_data = filter_data[(filter_data["Yeild_Lower"]>=yield_range[0])&
                                (filter_data["Yeild_Lower"]<=yield_range[1])]
    
    if depth != "All":
        if depth == "Above Ground":
            filter_data = filter_data[filter_data['Depth'] < 0]
        elif depth == "Underground":
            filter_data = filter_data[filter_data['Depth'] > 0]
    return filter_data

filter_data = filter_data(df,select_location,year_range,yield_range,select_depth)
st.write("Filtered Data",filter_data)
#----------------------------------------------------------------
# Ploting bar
import matplotlib.pyplot as plt
st.subheader("Number of Nuclear Explosions by Deployment Location")
if filter_data.empty:
    st.write("No Data Available")
else:
    location_count = filter_data["WEAPON DEPLOYMENT LOCATION"].value_counts()
    fig, ax = plt.subplots()
    location_count.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Number of Explosions")
    
    st.pyplot(fig)
#------------------------------------------------------------
#-----------------------------------_-------------------------
# Pivot Table: Count of Explosions by Purpose and Location
st.subheader("Count of Explosions by Purpose and Location")

if filter_data.empty:
    st.write("No Data Available")
else:
    pivot_table = pd.pivot_table(
        filter_data,
        values="Name",  
        index="Purpose",  
        columns="WEAPON DEPLOYMENT LOCATION",  
        aggfunc="count",  
        fill_value=0  
    )

    
    st.write(pivot_table)
    
#---------------------------------------------------   
# Line plot
st.subheader("Yearly Trend of Explosion Counts by Country")

if filter_data.empty:
    st.write("No Data Available")
else:
    yearly_counts = filter_data.groupby(["Year", "WEAPON SOURCE COUNTRY"]).size().unstack()

    # Create the line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    yearly_counts.plot(ax=ax, marker="o", linewidth=2)

    # Customize the chart
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Explosions")
    ax.legend(title="Country", loc="upper left", bbox_to_anchor=(1, 1))
    ax.grid(True, linestyle="--", alpha=0.6)

    st.pyplot(fig)
    
    

 #================================================================   
 # pie plot
import  plotly.express as px
st.subheader("Distributions of Explosion Purposes")
purpose_count = filter_data['Purpose'].value_counts()
fig = px.pie(names=purpose_count.index,values=purpose_count,title="Explosion Purpses Distrubution")
st.plotly_chart(fig)


#================================================

# Map Disply
from streamlit_folium import st_folium
import folium
st.subheader("Geographical distribution of Nuclear Explosions")
if filter_data.empty:
    st.write("No Data Available")
else:
    map_center = [20,0]
    m = folium.Map(location=map_center, zoom_start=2)
    for _, row in filter_data.iterrows():
        folium.Marker(
            location = [row['Latitude'],row['Longitude']],
            popup = f"{row["Name"]} - Yield{row['Yeild_Upper']}kt",
            icon = folium.Icon(color = "red" if row['Depth']< 0 else "blue")
            ).add_to(m)
        
    st_folium(m,width=700,key = "unique_map_for_explosions")

# Download Csv
csv = filter_data.to_csv(index = False)
st.download_button(f"Download Filtered Data  as csv", data =csv ,file_name="Filtered_Data",mime = 'text/csv')

# Add error handling to prevent issues when loading or filtering data.

try:
    data = pd.read_excel("nuclear_explosions.xlsx")
except FileNotFoundError:
    st.error("The data file could not be found.")
except Exception as e:
    st.error(f"An error occurred: {e}")