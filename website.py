from turtle import width
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df=pd.read_csv("vgsales.csv")

st.title("How Nintendo plan for their future publishment of games?")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.subheader("Let's get started by looking at the Top 50 video games sales in different regions.")

#Vis 1 bar
rank50 =df.sort_values(by='Global_Sales', ascending=False).head(50)
region_order = ['NA_Sales', 'JP_Sales', 'PAL_Sales', 'Other_Sales']
re = ['North America', 'Japan', 'Europe', 'Other Regions']

bar = alt.Chart(rank50,width=800,height=500).transform_fold(
  ['NA_Sales', 'JP_Sales', 'PAL_Sales', 'Other_Sales'],
  as_=['Regional_Sales', 'Amount']
).mark_bar().encode(
  x=alt.X('Name:N', sort='-y'),
  y=alt.Y('Amount:Q', title='Sales (million $)'),
  color=alt.Color('Regional_Sales:N', sort=region_order),
  order=alt.Order('region_order:Q'),
    opacity=alt.condition(alt.datum.Publisher=='Nintendo  ',alt.value(1),alt.value(0.4))
)

chart = alt.layer(bar).configure_title(fontSize=18, anchor="middle").configure_legend(titleFontSize=14,labelFontSize=12).configure_axis(titleFontSize=14,labelFontSize=11) 

barr = chart.encode(
    tooltip=['Name:N','Regional_Sales:N','Amount:Q','Global_Sales:Q','Genre:N']
)

st.write(barr)

st.markdown("Among top 50 video game global sales, 72% of games are published by Nintendo. Nintendo is quite competitive in the global video game market.")

#Vis 2 line
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.subheader("Next, let's take a look at the trend of sales change of different genre.")
st.caption("You can select the radio button to see differences between regions.")
##US
orderr = df.groupby(['Genre'])['NA_Sales'].sum().sort_values(ascending=False).to_frame().index.tolist()
line_NA = alt.Chart(df,width=800,height=400).transform_aggregate(
    NA_Sales='sum(NA_Sales)',
    groupby=['Year','Genre']
).mark_line().encode(
    x = alt.X('Year:N'),
    y = alt.Y('NA_Sales:Q', title='North America Sales (million $)'),
    color = alt.Color('Genre:N', title='Genre', sort=orderr)
)

NA_line = line_NA.encode(
    tooltip=['Year:N','Genre:N','NA_Sales:Q']
)

selectGenre=alt.selection_single(
    fields=['Genre'],
    init={"Genre":orderr[0]},
    bind=alt.binding_select(options=orderr,name="Select Genres:  ")
)

colorCondition = alt.condition(selectGenre,alt.Color("Genre:N"),alt.value('lightgray'))

NA_final = NA_line.add_selection(
    selectGenre
).encode(
    color=colorCondition
)

##EU
orderr_EU = df.groupby(['Genre'])['PAL_Sales'].sum().sort_values(ascending=False).to_frame().index.tolist()
line_EU = alt.Chart(df,width=800,height=400).transform_aggregate(
    PAL_Sales='sum(PAL_Sales)',
    groupby=['Year','Genre']
).mark_line().encode(
    x = alt.X('Year:N'),
    y = alt.Y('PAL_Sales:Q', title='Europe Sales (million $)'),
    color = alt.Color('Genre:N', title='Genre', sort=orderr_EU)
)

PAL_line = line_EU.encode(
    tooltip=['Year:N','Genre:N','PAL_Sales:Q']
)

selectGenre=alt.selection_single(
    fields=['Genre'],
    init={"Genre":orderr_EU[0]},
    bind=alt.binding_select(options=orderr_EU,name="Select Genres:  ")
)

colorCondition = alt.condition(selectGenre,alt.Color("Genre:N"),alt.value('lightgray'))

PAL_final = PAL_line.add_selection(
    selectGenre
).encode(
    color=colorCondition
)

##JP
orderr_JP = df.groupby(['Genre'])['JP_Sales'].sum().sort_values(ascending=False).to_frame().index.tolist()
line_JP = alt.Chart(df,width=800,height=400).transform_aggregate(
    JP_Sales='sum(JP_Sales)',
    groupby=['Year','Genre']
).mark_line().encode(
    x = alt.X('Year:N'),
    y = alt.Y('JP_Sales:Q', title='Japan Sales (million $)'),
    color = alt.Color('Genre:N', title='Genre', sort=orderr_JP)
)

JP_line = line_JP.encode(
    tooltip=['Year:N','Genre:N','JP_Sales:Q']
)

selectGenre=alt.selection_single(
    fields=['Genre'],
    init={"Genre":orderr_JP[0]},
    bind=alt.binding_select(options=orderr_JP,name="Select Genres:  ")
)

colorCondition = alt.condition(selectGenre,alt.Color("Genre:N"),alt.value('lightgray'))

JP_final = JP_line.add_selection(
    selectGenre
).encode(
    color=colorCondition
)

##other
orderr_oth = df.groupby(['Genre'])['Other_Sales'].sum().sort_values(ascending=False).to_frame().index.tolist()
line = alt.Chart(df,width=800,height=400).transform_aggregate(
    Other_Sales='sum(Other_Sales)',
    groupby=['Year','Genre']
).mark_line().encode(
    x = alt.X('Year:N'),
    y = alt.Y('Other_Sales:Q', title='Other region Sales (million $)'),
    color = alt.Color('Genre:N', title='Genre', sort=orderr_oth)
)

Other_line = line.encode(
    tooltip=['Year:N','Genre:N','Other_Sales:Q']
)

selectGenre=alt.selection_single(
    fields=['Genre'],
    init={"Genre":orderr_oth[0]},
    bind=alt.binding_select(options=orderr_oth,name="Select Genres:  ")
)

colorCondition = alt.condition(selectGenre,alt.Color("Genre:N"),alt.value('lightgray'))

Other_final = Other_line.add_selection(
    selectGenre
).encode(
    color=colorCondition
)

region_list=['North America', 'Europe', 'Japan', 'Other']
regions=st.radio('Select regions',region_list)
if(regions=="North America"):
    st.write(NA_final)
elif(regions=="Europe"):
    st.write(PAL_final)
elif(regions=="Japan"):
    st.write(JP_final)
elif(regions=="Other"):
    st.write(Other_final)

st.write("\n\n")
st.write("\n\n")
st.markdown("During 2005-2010, video games reached the peak. After that, sale performance decreased.")
st.markdown("In North America, action-adventure games are getting more popular than other genres. Shooter and action games always sell well in US. Sports games once ranked first but decreased recently.")
st.markdown("In Japan, the sales performance is quite different. Role-playing games have remained popular, and their sales far outnumber other genres. ")
st.markdown("In Europe and the rest of the world, the situation are almost the same as that in US.")

# Vis 3 
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.subheader("Let's dive deeper to see different sales performance based on the year and platform released.")
alt.data_transformers.enable('default', max_rows=None)
## US & year
US_year = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('NA_Sales',title="North America Sales (million $)"),
    color=alt.Color('NA_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.Year<2020).transform_filter(alt.datum.NA_Sales!='nan')

text_US_year=US_year.mark_text(dx=10,align='left').encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('NA_Sales'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('NA_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_US=US_year.encode(
    tooltip=['Name:N','Year:N','NA_Sales:N','Publisher:N']
).interactive()

## US & platform
US_plat = alt.Chart(df).mark_point(filled=True,size=90,width=300).encode(
    x=alt.X('Platform'),
    y=alt.Y('NA_Sales',title="North America Sales (million $)"),
    color=alt.Color('NA_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.NA_Sales!='nan')

text_US_plat=US_plat.mark_text(dx=-10,align='right').encode(
    x=alt.X('Platform'),
    y=alt.Y('NA_Sales'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('NA_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_US_plat=US_plat.encode(
    tooltip=['Name:N','Platform:N','NA_Sales:N','Publisher:N']
).interactive()

NA=((int_US+text_US_year)|(int_US_plat+text_US_plat)).resolve_scale(y='shared')

# EU & year
EU_year = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('PAL_Sales'),
    color=alt.Color('PAL_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.Year<2020).transform_filter(alt.datum.PAL_Sales!='nan')

text_EU_year=EU_year.mark_text(dx=10,align='left').encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('PAL_Sales',title='Europe Sales (million $)'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('PAL_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_EU=EU_year.encode(
    tooltip=['Name:N','Year:N','PAL_Sales:N','Publisher:N']
).interactive()

# EU & platform
EU_plat = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Platform'),
    y=alt.Y('PAL_Sales'),
    color=alt.Color('PAL_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.NA_Sales!='nan')

text_EU_plat=EU_plat.mark_text(dx=-10,align='right').encode(
    x=alt.X('Platform'),
    y=alt.Y('PAL_Sales',title='Europe Sales (million $)'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('PAL_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_EU_plat=EU_plat.encode(
    tooltip=['Name:N','Platform:N','PAL_Sales:N','Publisher:N']
).interactive()

# JP & year
JP_year = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('JP_Sales',title="Japan Sales (million $)"),
    color=alt.Color('JP_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.Year<2020).transform_filter(alt.datum.JP_Sales!='nan')

text_JP_year=JP_year.mark_text(dx=10,align='left').encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('JP_Sales'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('JP_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_JP=JP_year.encode(
    tooltip=['Name:N','Year:N','JP_Sales:N','Publisher:N']
).interactive()

# JP & platform
JP_plat = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Platform'),
    y=alt.Y('JP_Sales',title="Japan Sales (million $)"),
    color=alt.Color('JP_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.JP_Sales!='nan')

text_JP_plat=JP_plat.mark_text(dx=-10,align='right').encode(
    x=alt.X('Platform'),
    y=alt.Y('JP_Sales'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('JP_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_JP_plat=JP_plat.encode(
    tooltip=['Name:N','Platform:N','JP_Sales:N','Publisher:N','Genre:N']
).interactive()

# other & year
oth_year = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('Other_Sales',title="Other region Sales (million $)"),
    color=alt.Color('Other_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.Year<2020).transform_filter(alt.datum.JP_Sales!='nan')

text_oth_year=oth_year.mark_text(dx=10,align='left').encode(
    x=alt.X('Year',scale=alt.Scale(domain=[1979,2019])),
    y=alt.Y('Other_Sales'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('Other_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_oth=oth_year.encode(
    tooltip=['Name:N','Year:N','Other_Sales:N','Publisher:N']
).interactive()

# other & platform
oth_plat = alt.Chart(df).mark_point(filled=True,size=90,width=100).encode(
    x=alt.X('Platform'),
    y=alt.Y('Other_Sales',title="Other region Sales (million $)"),
    color=alt.Color('Other_Sales',scale=alt.Scale(scheme="blueorange")),
).transform_filter(alt.datum.Other_Sales!='nan')

text_oth_plat=oth_plat.mark_text(dx=-10,align='right').encode(
    x=alt.X('Platform'),
    y=alt.Y('Other_Sales'),
    text=alt.Text('Name')
).transform_window(
    sort=[alt.SortField('Other_Sales', order='descending')],
    sales_rank='rank(*)'
).transform_filter(
    alt.datum.sales_rank < 10
)

int_oth_plat=oth_plat.encode(
    tooltip=['Name:N','Platform:N','Other_Sales:N','Publisher:N','Genre:N']
).interactive()

NA&((int_EU+text_EU_year)|(int_EU_plat+text_EU_plat))&((int_JP+text_JP_year)|(int_JP_plat+text_JP_plat))&((int_oth+text_oth_year)|(int_oth_plat+text_oth_plat))

st.markdown("North American market has the highest sales among all the other regions.")
st.markdown("Wii Sports is far ahead of other games around the world, especially in North America and Europe. ")
st.markdown("All the Nintendo games perform really good in the global sales. Majority of games that rank top 10 in sales from 1979-2009 were published by Nintendo.")
st.markdown("Because of this, most high sales ranking games are published on the platform that is owned by Nintendo like Wii, NES, GB. X360 and PS are close behind. ")
st.markdown("The Japan market is different where people prefer role-playing games more like Pokemon series.")
st.markdown("Although Nintendo has the most high-selling games, Grand Theft by Rockstars and Call of Duty by Activision recently display their potential of popularity.")

# Vis 4 
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.subheader("Finally, let's check out how users think and feel about their favorite games.")