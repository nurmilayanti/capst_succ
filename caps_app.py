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
st.markdown("""
    <div style='margin-bottom:40px; text-align: justify;'>
        <h11>Berdasarkan data Kementerian Perindustrian, industri kosmetik memberikan kontribusi sebesar 3,83% terhadap Produk Domestik Bruto (PDB) pada triwulan III tahun 2023. Skincare menjadi salah satu kategori yang paling banyak dicari oleh masyarakat. Peningkatan minat terhadap produk kecantikan dipengaruhi oleh beberapa faktor, antara lain kemudahan akses informasi, tren kecantikan dan budaya populer, perubahan gaya hidup, influencer endorsement, inovasi produk kecantikan, kesadaran kesehatan kulit, dan diversifikasi produk.</h11>
    </div>
""", unsafe_allow_html=True)
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
                        scale=alt.Scale(range=['#156AA8', '#15A89B'])),
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



st.markdown("""
    <div style='margin-bottom:40px; text-align: justify;'>
        <h11>Pada diagram batang sisi kiri merepresentasikan banyaknya produk dengan keyword skincare di 3 e-commerce (Tokopedia, Shopee dan Lazada) serta jumlah produk yang terjual di masing-masing e-commerce tersebut. Sedangkan pada diagram sisi kanan mencoba untuk menggali terkait salah satu faktor yang memepengaruhi besarnya jumlah produk yang terjual degan melihat nilai rata-rata dari discount per e-commerce.</h11>
    </div>
""", unsafe_allow_html=True)







##



# Ensure there's data to plot


##

df.loc[df['shop_loc'].str.contains('makassar', case=False), 'shop_loc'] = 'makassar'
df.loc[df['shop_loc'].str.contains('surakarta', case=False), 'shop_loc'] = 'surakarta'   
df.loc[df['shop_loc'].str.contains('kediri', case=False), 'shop_loc'] = 'kediri' 
df.loc[df['shop_loc'].str.contains('pontianak', case=False), 'shop_loc'] = 'pontianak' 
df.loc[df['shop_loc'].str.contains('yogyakarta', case=False), 'shop_loc'] = 'yogyakarta' 
df.loc[df['shop_loc'].str.contains('balikpapan', case=False), 'shop_loc'] = 'kota balikpapan' 
# df.loc[df['shop_loc'].str.contains('madiun', case=False), 'shop_loc'] = 'madiun' 
# df.loc[df['shop_loc'].str.contains('dilayani toko', case=False), 'shop_loc'] = 'kediri' 
# Mengganti kata 'Bandung' menjadi 'Kota Bandung' dalam kolom 'lokasi'
df['shop_loc'] = df['shop_loc'].str.replace(r'\bbandung\b|\bkota kota bandung\b', 'kota bandung', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bkab. kota bandung\b', 'kab. bandung', regex=True)
df.loc[df['shop_loc'].str.contains(r'\bkota kota bandung\b', case=False), 'shop_loc'] = 'kota bandung'
df['shop_loc'] = df['shop_loc'].str.replace(r'\bbandar lampung\b|\bkota bandar lampung\b', 'kota bandar lampung', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bjakarta pusat\b|\bkota jakarta pusat\b', 'jakarta pusat', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bjakarta timur\b|\bkota jakarta timur\b', 'jakarta timur', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bjakarta barat\b|\bkota jakarta barat\b', 'jakarta barat', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bjakarta utara\b|\bkota jakarta utara\b', 'jakarta utara', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bjakarta selatan\b|\bkota jakarta selatan\b', 'jakarta selatan', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bbogor\b|\bkota bogor\b', 'kota bogor', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bsurabaya\b|\bkota surabaya\b', 'kota surabaya', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\btangerang selatan\b|\bkota tangerang selatan\b', 'kota tangerang selatan', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\btangerang\b|\bkota tangerang\b', 'kota tangerang', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bkab.ciamis\b|\bkab. ciamis\b', 'kab. ciamis', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bmedan\b|\bkota medan\b', 'kota medan', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bsemarang\b|\bkota semarang\b', 'kota semarang', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bdepok\b|\bkota depok\b', 'kota depok', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bbekasi\b|\bkota bekasi\b', 'kota bekasi', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bpalembang\b|\bkota palembang\b', 'kota palembang', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bcimahi\b|\bkota cimahi\b', 'kota cimahi', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bcirebon\b|\bkota cirebon\b', 'kota cirebon', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bmadiun\b|\bkota madiun\b', 'kota madiun', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bmalang\b|\bkota malang\b', 'kota malang', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\btasikmalaya\b|\bkota tasikmalaya\b', 'kota tasikmalaya', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bkota jakarta\b', 'jakarta', regex=True)
df['shop_loc'] = df['shop_loc'].str.replace(r'\bkab. kota\b', 'kab. ', regex=True)


col1, col2 = st.columns([2, 1]) 

with col1:
    st.write('Product Sales Distribution by Shop Locations')
    if not df.empty:

        all_locations = df['shop_loc'].unique()
        selected_locations = st.multiselect('Select Shop Locations:', all_locations)

        
        if selected_locations:  # Cek apakah ada lokasi yang dipilih
            # Filter DataFrame berdasarkan lokasi yang dipilih
            filtered_df = df[df['shop_loc'].isin(selected_locations)]

            if not filtered_df.empty:
                fig = go.Figure()

                # Membuat diagram batang berdasarkan penjualan produk untuk lokasi toko yang dipilih
                st.write(f'Product Sales for {selected_locations}')
                fig.add_trace(go.Bar(
                    x=filtered_df['shop_loc'],
                    y=filtered_df['prd_sales_1'],
                    marker_color='#8AEC78'
                ))

                fig.update_layout(
                    xaxis=dict(title='Shop Location'),
                    yaxis=dict(title='Product Sales'),
                    width=600,
                    height=500
                )

                st.plotly_chart(fig)
            else:
                st.write("No data available for the selected shop locations.")
        else:
            st.write("Please select at least one shop location.")
    else:
        st.write("No data available to plot.")
with col2:
    st.markdown("""
    <div style='margin-top:200px; text-align: justify;'>
        <h11>Diagram batang disamping mereprsentasikan jumlah sales untuk setiap lokasi yang memungkinkan untuk membandingkan sales antar lokasi.</h11>
    </div>
""", unsafe_allow_html=True)



################

if not df.empty:
    fig = go.Figure()

    # Scatter plot based on product sales (single plot)
    st.write('Product Sales Location by Region')
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
        <div style="margin-right: 5px; margin-bottom: 230px;">
            <h7>Top Selling Brands</h7>
            {}
        </div>
        """.format(top_brands_df.to_html()), 
        unsafe_allow_html=True
    )

 


st.markdown("""
    <div style='text-align: justify;'>
        <h11>Diagram batang menunjukkan perbedaan produk terlaris di setiap platform e-commerce. Terdapat variasi produk terpopuler antara Lazada, Shopee, dan Tokopedia. Hal ini menunjukkan bahwa preferensi konsumen yang berbeda-beda di setiap platform. pada tabel diseblah kanan menunjukkan top 5 brand dari keseluruhan e-commerce yang menunjukkan bahwa produk yang berasal dari Korea Selatan mampu mengungguli produk-produk lainnya hal ini dapat dipengaruhi oleh korean wave.</h11>
    </div>
""", unsafe_allow_html=True)
st.write("<div style='text-align:center; margin-top:70px;'>Created by Nurmilayanti <a href>https://www.linkedin.com/in/nurmilayanti-ii/</a href></div>", unsafe_allow_html=True)


