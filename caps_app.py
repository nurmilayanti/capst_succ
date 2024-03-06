import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import cartopy.crs as ccrs
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import altair as alt
import numpy as np
import altair as alt


st.set_page_config(layout='wide')
st.write("<div style=''><h3>Revealing Skincare Insights: Analysis of Top 3 E-commerce Trends in Indonesia</h3></div>", unsafe_allow_html=True)

df = pd.read_excel('top_3_ecommerce_edited2.1.xlsx')

produk_terjual_per_ecommerce = df.groupby('e_commerce')['prd_sales_1'].sum().reset_index(name='jumlah_produk_terjual')

# Menghitung total produk per e-commerce
produk_per_ecommerce = df['e_commerce'].value_counts().reset_index()
produk_per_ecommerce.columns = ['e_commerce', 'jumlah_produk']

# Menggabungkan data
merged_data = pd.merge(produk_terjual_per_ecommerce, produk_per_ecommerce, on='e_commerce')

# Melipatgandakan kolom menggunakan melt()
melted_data = pd.melt(merged_data, id_vars=['e_commerce'], value_vars=['jumlah_produk_terjual', 'jumlah_produk'],
                      var_name='variable', value_name='value')




chart1 = alt.Chart(melted_data).mark_bar().encode(
        x=alt.X('e_commerce:N', title='E-Commerce'),
        y=alt.Y('value:Q', title='Value', scale=alt.Scale(type='log')),  # Menggunakan skala logaritmik
        color=alt.Color('variable:N', 
                        title='Variable', 
                        scale=alt.Scale(range=['#083D53', '#0A6D99'])),
        tooltip=['value', 'e_commerce', 'variable']
    ).properties(
        width=500,
        height=400,
        title='Number of Products and Sold Products per E-commerce'
    ).interactive()



# Membuat visualisasi dengan Altair

average_discount = df.groupby('e_commerce')['prd_discount_1_dec'].mean().reset_index()
# Find e-commerce with the highest discount
ecommerce_with_highest_discount = average_discount.loc[average_discount['prd_discount_1_dec'].idxmax()]
# Streamlit App

chart2 = alt.Chart(average_discount).mark_bar().encode(
        x=alt.X('e_commerce:N', title='E-Commerce'),
        y=alt.Y('prd_discount_1_dec:Q', title='Average Discount'),
        color=alt.Color('e_commerce:N', title='E-Commerce', scale=alt.Scale(range=['#15A89B', '#156AA8', '#543AB1'])),
        tooltip=['e_commerce', 'prd_discount_1_dec']
    ).properties(
        width=600,
        height=400,
        title='Average Discounts by E-commerce'
    ).interactive()



col1, col2 = st.columns([2, 1]) 
with col1:
    st.altair_chart(chart1, use_container_width=True)
with col2:
    st.altair_chart(chart2, use_container_width=True)











##



# Ensure there's data to plot

if not df.empty:
    fig = go.Figure()

    # Scatter plot based on product sales (single plot)
    st.write('Location of Product Sales along Latitude and Longitude Coordinates')
    fig.add_trace(go.Scattergeo(
        lon=df['longitude'],
        lat=df['latitude'],
        mode='markers',
        marker=dict(
            size=10,
            opacity=0.8,
            color=df['prd_sales_1'],
            colorscale='viridis',
            colorbar=dict(
                title="Product Sales"
            )
        ),
        text=df['shop_loc']
    ))

    fig.update_geos(
        projection_type="orthographic",
        showocean=True,
        oceancolor="#0E1218",  # Warna laut yang lebih terang
        showland=True,
        landcolor="lightgray",   # Warna daratan yang lebih terang
        showcountries=True,
        countrycolor="white",    # Warna batas negara yang lebih terang
        countrywidth=1,
        showcoastlines=True,
        showframe=False,
        lataxis_range=[-10, 6],
        lonaxis_range=[90, 141]
    )

    fig.update_layout(
        #title='Product Sales Heatmap',
        width=1100,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='natural earth',
            bgcolor='rgba(2,0,0,0)'  # Set background color to transparent
            
        ),
        plot_bgcolor='rgba(0,0,0,0)' , # Set plot background color to transparent
        autosize=True,  # Mengaktifkan penyesuaian otomatis ukuran plot
    margin=dict(l=0, r=0, t=0, b=0) 
    )

    st.plotly_chart(fig)
else:
    st.write("No data available to plot.")

#####   
    
top_brands = df.groupby('merk')['prd_sales_1'].sum()
top_brands = top_brands.nlargest(5)
top_brands_df = pd.DataFrame({'Merk': top_brands.index, 'Number of Products Sold': top_brands.values})

# Kelompokkan DataFrame dan hitung total penjualan per merek per e-commerce

top_products_per_ecommerce = df.groupby(['e_commerce', 'merk'])['prd_sales_1'].sum().reset_index(name='prd_sales_1')

# Urutkan DataFrame berdasarkan e-commerce dan total penjualan secara menurun
top_products_per_ecommerce = top_products_per_ecommerce.sort_values(by=['e_commerce', 'prd_sales_1'], ascending=False)

# Ambil lima merek teratas per e-commerce
top_products_per_ecommerce = top_products_per_ecommerce.groupby('e_commerce').head(5)

plot_width = 600
plot_height = 400

# Create a Streamlit layout with two columns
col1, col2 = st.columns([2, 1]) 

# Inside col1, display the chart
with col1:
    chart = alt.Chart(top_products_per_ecommerce).mark_bar().encode(
        x='prd_sales_1:Q',
        y='merk:N',
        color=alt.Color('e_commerce:N', scale=alt.Scale(scheme='viridis')),
        tooltip=['prd_sales_1', 'merk', 'e_commerce']
    ).properties(
        width=plot_width,
        height=plot_height,
        title='Top Products per E-commerce'
    ).interactive()
    st.altair_chart(chart, use_container_width=False)

# Inside col2, display the table with adjusted right margin
with col2:
    st.write(
        """
        <div style="margin-right: 5px;">
            <h7>Top Selling Brands</h7>
            {}
        </div>
        """.format(top_brands_df.to_html()), 
        unsafe_allow_html=True
    )



st.write("<div style='text-align:center; margin-top:70px;'>Created by Nurmilayanti</div>", unsafe_allow_html=True)



