import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import plotly.io as pio
import plotly.graph_objects as go
import calendar
# Set Theme
custom_theme = {
    'layout': {
        'title': {
            'font': {'size': 20, 'color': 'blue'}, 
            'x': 0.5, 
            'xanchor': 'center'
        },
        'paper_bgcolor': '#1f1f1f', 
        'plot_bgcolor': '#1f1f1f',   
        'geo': {
            'bgcolor': '#f3e9dc', 
            'lakecolor': '#999999', 
            'showlakes': True,
            'landcolor': '#2f2f2f'  
        },
        'colorway': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA'], 
        'margin': {'l': 10, 'r': 10, 'b': 30, 't': 30} 
    }
}


pio.templates['custom_map'] = go.layout.Template(custom_theme)
pio.templates.default = 'custom_map'
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.markdown(
    """
    <style>
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Car Sales Dashboard")
with st.sidebar:
    st.header("Yearly Car Sales Analysis")
    years = list(range(2015, 2013, -1))
    months_list = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
    ]
    selected_sales_month = st.selectbox(label='Select Sales Month', options=months_list,key='sales-month')
    selected_year = st.selectbox(label='Select Car Manufacturing Year   ', options=years,key='car-year')
data = pd.read_csv('Modified-Data.csv')
data['saledate'] = pd.to_datetime(data['saledate'], utc=True)
month_number = {name: i+1 for i, name in enumerate(months_list)}
selected_month_number = month_number[selected_sales_month]
filtered_data = data[
    (data['saledate'].dt.month == selected_month_number) & 
    (data['saledate'].dt.year == selected_year)
]
state_occurrences = filtered_data['state'].value_counts().reset_index()
state_occurrences.columns = ['state', 'occurrences']
state_counts = filtered_data['state'].value_counts().reset_index()
state_counts.columns = ['state_abbr', 'count']
col1,gap,col2,col3 = st.columns([3,0.5,2,5])
seccol1, gap, seccol2 = st.columns([4, 0.5, 2])
top_colors = filtered_data['color'].value_counts().head(5).reset_index()
top_colors.columns = ['color', 'count']
with col1:
    max_count = top_colors['count'].max()  
    st.markdown("<h3 style='color: #5e3023; font-size: 16px; font-weight: 1000;'>Top 5 Most Sold Car Colors</h3>", unsafe_allow_html=True)
    
    for index, row in top_colors.iterrows():
        color_name = row['color']
        color_count = row['count']
        progress_rate = color_count / max_count * 100  
        tablecol1, tablecol2, tablecol3 = st.columns([1, 3, 1])
        tablecol1.write(f"**{color_name}**")
        tablecol2.markdown(f"""
            <div style="background-color: #dab49d; border-radius: 5px; width: 100%; height: 15px; position: relative; margin-top:8px;">
                <div style="background-color: #5e3023; width: {progress_rate}%; height: 100%; border-radius: 5px;"></div>
            </div>
        """, unsafe_allow_html=True)
        tablecol3.write(f"{color_count}")
    seller_sales = filtered_data.groupby('seller')['sellingprice'].sum().reset_index()
    seller_sales_sorted = seller_sales.sort_values(by='sellingprice', ascending=False).reset_index(drop=True)
    max_value = min(len(seller_sales), 5)
    print(len(seller_sales))
    if max_value > 1:
        rank = st.slider('Select the Rank of Best Seller', min_value=1, max_value=max_value, value=1)
        max_seller = seller_sales_sorted.iloc[rank - 1]  
        seller_with_max_sales = max_seller['seller']
        max_total_sales = max_seller['sellingprice']
        semicol1,gap,semicol2=st.columns([3,0.01,2])
        with semicol1:
            st.markdown(f"""
                <div style="margin-top: 20px;margin-bottom:20px">
                    <strong>Best Sellers:</strong><br>{seller_with_max_sales}
                </div>
                """, unsafe_allow_html=True)
        with semicol2:
            st.markdown(f"""
                <div style="margin-top: 20px;margin-bottom:20px">
                    <strong>Highest Total Sales Amount:</strong><br>{max_total_sales:,.2f}
                </div>
                """, unsafe_allow_html=True)   
    elif max_value == 1:
        rank = 1
        max_seller = seller_sales_sorted.iloc[rank - 1]  
        seller_with_max_sales = max_seller['seller']
        max_total_sales = max_seller['sellingprice']
        semicol1,gap,semicol2=st.columns([3,0.01,2])
        with semicol1:
            st.markdown(f"""
                <div style="margin-top: 20px;margin-bottom:20px">
                    <strong>Best Sellers:</strong><br>{seller_with_max_sales}
                </div>
                """, unsafe_allow_html=True)
        with semicol2:
            st.markdown(f"""
                <div style="margin-top: 20px;margin-bottom:20px">
                    <strong>Highest Total Sales Amount:</strong><br>{max_total_sales:,.2f}
                </div>
                """, unsafe_allow_html=True)   

with col2:
    filtered_data['day'] = filtered_data['saledate'].dt.day
    num_days_in_month = calendar.monthrange(selected_year, selected_month_number)[1]
    days_with_sales = filtered_data['day'].nunique()
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=days_with_sales,
        gauge={'axis': {'range': [0, num_days_in_month]}, 'bar': {'color': "#5e3023"}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(
        width=220,  
        height=200, 
        font_color="#5e3023",
        title_font_color="#5e3023",
        title_font_size=20,
        title={'text': 'Days with Sales'},
    )
    st.plotly_chart(fig)
    total_sales = filtered_data['sellingprice'].sum() 
    total_MMR = filtered_data['mmr'].sum()  
    sales_to_MMR_ratio = (total_sales / total_MMR) * 100 
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sales_to_MMR_ratio, 
        gauge={'axis': {'range': [0, 150]}, 'bar': {'color': "#5e3023"}}, 
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        width=220,  
        height=200,  
        font_color="#5e3023",
        title_font_color="#5e3023",
        title_font_size=20,
        title={'text': 'Saleprice to MMR Ratio'},  
    )

    st.plotly_chart(fig)
with col3:
    fig = px.choropleth(
        state_counts,
        locations='state_abbr',  
        locationmode='USA-states',  
        color='count',  
        scope='usa',  
        color_continuous_scale='brwnyl', 
        labels={'count': 'State Counts'},  
        title='US State Density Map by Value Counts',
        hover_data={'state_abbr': True, 'count': True},
    )
    fig.update_layout(
        dragmode=False, 
        autosize=False, 
        width=950,  
        height=450,  
        plot_bgcolor="brown",
        geo=dict(
            scope='usa',
            showcountries=True,
            showlakes=True,
            lakecolor='rgb(255, 255, 255,0)',
            projection_scale=1,  
            center=dict(lat=38.0, lon=-97.0),
        )
    )
    st.plotly_chart(fig)

with seccol1:
    num_days_in_month = calendar.monthrange(selected_year, selected_month_number)[1]
    all_days = pd.DataFrame({'day': range(1, num_days_in_month + 1)})
    grouped_data = filtered_data.groupby(['day', 'transmission']).size().reset_index(name='count')
    merged_data = all_days.merge(grouped_data, on='day', how='left').fillna({'count': 0, 'transmission': 'No Sales'})
    fig = px.bar(
        merged_data, 
        x='day', 
        y='count', 
        color='transmission',
        barmode='stack',
        labels={'day': 'Day of the Month', 'count': 'Number of Cars Sold'},
        title=f"Cars Sold by Transmission Type in {selected_sales_month} {selected_year}",
        color_discrete_map={'automatic': '#5e3023', 'manual': '#dab49d', 'No Sales': '#e0e0e0'}
    )
    fig.update_layout(
        xaxis=dict(tickmode='linear'), 
        bargap=0.2,  
        width=1200,
        height=450,
        font_color="deeppink",
        title_font_color="#5e3023",
        title_font_size=20,
        legend_title_font_color="#5e3023",
        showlegend=False,
    )

    st.plotly_chart(fig)


top_model = filtered_data['model'].value_counts().head(5).reset_index()
top_model.columns = ['model', 'count']
with seccol2:
    max_count = top_model['count'].max()  
    st.markdown("<h3 style='color: #5e3023; font-size: 16px; font-weight: 1000;'>Top 5 Most Sold Car Models</h3>", unsafe_allow_html=True)
    for index, row in top_model.iterrows():
        color_name = row['model']
        color_count = row['count']
        progress_rate = color_count / max_count * 100 
        tablecol1, tablecol2, tablecol3 = st.columns([1, 3, 1])
        tablecol1.write(f"**{color_name}**")
        tablecol2.markdown(f"""
            <div style="background-color: #dab49d; border-radius: 5px; width: 100%; height: 15px; position: relative; margin-top:8px;">
                <div style="background-color: #5e3023; width: {progress_rate}%; height: 100%; border-radius: 5px;"></div>
            </div>
        """, unsafe_allow_html=True)
        tablecol3.write(f"{color_count}")
    semicolumn1,semicolumn2 = st.columns(2)
    with semicolumn1:
        total_sales = filtered_data['sellingprice'].sum()
        st.markdown(f"""
            <div style="margin-top: 20px;">
                Total Sales:<br><strong>${total_sales:,.2f}</strong>
            </div>
            """, unsafe_allow_html=True)
    with semicolumn2:
        total_MMR = filtered_data['mmr'].sum()
        st.markdown(f"""
            <div style="margin-top: 20px;">
                Total MMR:<br><strong>${total_MMR:,.2f}</strong>
            </div>
            """, unsafe_allow_html=True)