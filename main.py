import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Menampilkan semua baris dan kolom
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def project():
    # Latar Belakang
    # Latar Belakang
    st.markdown("<h1 style='text-align: center;'>Segmentasi Pelanggan dengan RFM</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left;'>Latar Belakang</h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Segmentasi pelanggan adalah langkah penting dalam memahami perilaku konsumen dan menciptakan strategi pemasaran yang lebih efektif. Dalam proyek ini, kami akan melakukan analisis segmentasi pelanggan menggunakan metode RFM (Recency, Frequency, Monetary) untuk mengelompokkan pelanggan berdasarkan tiga faktor utama: kapan terakhir kali mereka membeli (Recency), seberapa sering mereka membeli (Frequency), dan seberapa banyak mereka menghabiskan uang (Monetary).</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Metode RFM ini akan diterapkan pada dataset penjualan yang mencakup berbagai saluran penjualan dan produk untuk mengidentifikasi segmen-segmen pelanggan yang dapat digunakan untuk perencanaan pemasaran lebih lanjut.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>   </div>", unsafe_allow_html=True)

    # Eksplorasi Data
    with st.expander("Data Understanding"):
        st.write('**OrderNumber**: A unique identifier for each order.')
        st.write('**Sales Channel**: The channel through which the sale was made (In-Store, Online, Distributor, Wholesale).')
        st.write('**WarehouseCode**: Code representing the warehouse involved in the order.')
        st.write('**ProcuredDate**: Date when the products were procured.')
        st.write('**OrderDate**: Date when the order was placed.')
        st.write('**ShipDate**: Date when the order was shipped.')
        st.write('**DeliveryDate**: Date when the order was delivered.')
        st.write('**SalesTeamID**: Identifier for the sales team involved.')
        st.write('**_CustomerID**: Identifier for the customer.')
        st.write('**StoreID**: Identifier for the store.')
        st.write('**_ProductID**: Identifier for the product.')
        st.write('**Order Quantity**: Quantity of products ordered.')
        st.write('**Discount Applied**: Applied discount for the order.')
        st.write('**Unit Cost**: Cost of a single unit of the product.')
        st.write('**Unit Price**: Price at which the product was sold.')

        # Load the data
        df = pd.read_csv('US_Regional_Sales_Data.csv')
        st.markdown("<h4 style='text-align: justify;'>📊 Datasets</h2>", unsafe_allow_html=True)
        st.dataframe(df)
        info_df = pd.DataFrame({"Kolom": df.columns,"Non-Null Count": df.notnull().sum().values,
                                "Tipe Data": df.dtypes.values})
        st.markdown("<h4 style='text-align: justify;'>📋 Informasi Struktur Datasets</h2>", unsafe_allow_html=True)
        st.dataframe(info_df)

    # Mengonversi kolom yang diperlukan menjadi tipe data numerik
    df['Order Quantity'] = pd.to_numeric(df['Order Quantity'], errors='coerce')
    df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
    df['Discount Applied'] = pd.to_numeric(df['Discount Applied'], errors='coerce')
    df['Unit Cost'] = pd.to_numeric(df['Unit Cost'], errors='coerce')

    # Mengonversi OrderDate ke datetime
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])

    # Membuat kolom 'Sales per Order' dan 'Profit per Order'
    df['Sales per Order'] = round(df['Order Quantity'] * df['Unit Price'] * (1 - df['Discount Applied']), 2)
    df['Profit per Order'] = round(df['Sales per Order'] - (df['Order Quantity'] * df['Unit Cost']), 2)

    # Sales Dashboard Performance
    with st.expander("Simple EDA"):
        total_revenue = df['Sales per Order'].sum()
        total_orders = df['OrderNumber'].nunique()
        sales_volume = df['Order Quantity'].sum()
        total_profit = df['Profit per Order'].sum()
        total_customers = df['_CustomerID'].nunique()

        # Formatting for large numbers with K, M, B suffix
        def format_large_numbers(num):
            if num >= 1e9:
                return f"${num/1e9:.2f}B"
            elif num >= 1e6:
                return f"${num/1e6:.2f}M"
            elif num >= 1e3:
                return f"${num/1e3:.2f}K"
            else:
                return f"${num:.2f}"

        st.markdown("<h4 style='text-align: center;'>Sales Dashboard Performance</h4>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: left;'>Summary</h6>", unsafe_allow_html=True)

        # Metrik Total
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Revenue", format_large_numbers(total_revenue))
        col2.metric("Total Orders", f"{total_orders:,}")
        col3.metric("Sales Volume", f"{sales_volume:,}")
        col4.metric("Total Profit", format_large_numbers(total_profit))
        col5.metric("Total Customers", f"{total_customers}")

        # Menambahkan filter untuk memilih periode waktu
        min_date = pd.to_datetime(df['OrderDate']).min()
        max_date = pd.to_datetime(df['OrderDate']).max()
        start_date = st.date_input("Select Start Date", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("Select End Date", max_date, min_value=min_date, max_value=max_date)

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        df_filtered = df[(df['OrderDate'] >= start_date) & (df['OrderDate'] <= end_date)]

        # Visualizations (Sales Trend, Customers Trend, Sales Volume by Sales Channel)
        sales_trend = df_filtered.groupby(df_filtered['OrderDate'].dt.to_period('M'))['Sales per Order'].sum().reset_index()
        sales_trend['OrderDate'] = sales_trend['OrderDate'].dt.strftime('%b %Y')  # Convert Period to string
        fig_sales_trend = px.line(sales_trend, x='OrderDate', y='Sales per Order', title="Sales Trend", labels={'OrderDate': 'Date', 'Sales per Order': 'Revenue'})
        st.plotly_chart(fig_sales_trend)

        # Line Chart: Customers Trend
        customers_trend = df_filtered.groupby(df_filtered['OrderDate'].dt.to_period('M'))['_CustomerID'].nunique().reset_index()
        customers_trend['OrderDate'] = customers_trend['OrderDate'].dt.strftime('%b %Y')  # Convert Period to string
        fig_customers_trend = px.line(customers_trend, x='OrderDate', y='_CustomerID', title="Customers Trend", labels={'OrderDate': 'Date', '_CustomerID': 
                                                                                                                        'Number of Customers'})
        st.plotly_chart(fig_customers_trend)

        # Treemap: Sales Volume by Sales Channel and Product ID
        df_sales_volume = df_filtered.groupby(['Sales Channel', '_ProductID'])['Order Quantity'].sum().reset_index()
        fig_sales_volume = px.treemap(df_sales_volume, path=['Sales Channel', '_ProductID'], values='Order Quantity', color='Order Quantity', 
                                      title="Sales Volume by Sales Channel and Product")
        fig_sales_volume.update_traces(hovertemplate="<b>%{label}</b><br>Sales Channel: %{parent}<br>_ProductID: %{id}<br>Order Quantity Sum: %{value}")
        st.plotly_chart(fig_sales_volume)

    # RFM Analysis
    st.markdown("<h2 style='text-align: left;'>Analisis RFM</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left;'>Perhitungan RFM Score</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Analisis RFM dilakukan untuk mengelompokkan pelanggan berdasarkan tiga faktor utama: Recency, Frequency, dan Monetary. Berikut adalah cara perhitungan RFM Score yang digunakan dalam analisis ini:</div>", unsafe_allow_html=True)

    st.markdown("<ul><li><h5 style='text-align: left;'>Recency Score</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Skor Recency dihitung berdasarkan selisih hari antara tanggal terakhir pembelian dan tanggal referensi (misalnya 1 Januari 2021). Semakin baru pembelian, semakin tinggi skor yang diberikan (maksimal skor 5).</div>", unsafe_allow_html=True)

    st.markdown("<ul><li><h5 style='text-align: left;'>Frequency Score</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Skor Frequency dihitung berdasarkan seberapa sering pelanggan melakukan pembelian. Semakin sering pembelian, semakin tinggi skor yang diberikan, dengan skor tertinggi 5.</div>", unsafe_allow_html=True)

    st.markdown("<ul><li><h5 style='text-align: left;'>Monetary Score</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Skor Monetary dihitung berdasarkan total pengeluaran pelanggan. Semakin besar pengeluaran, semakin tinggi skor yang diberikan, dengan skor tertinggi 5.</div>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: left;'>RFM Score</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>RFM Score dihitung dengan menggabungkan skor Recency, Frequency, dan Monetary. Misalnya, jika skor Recency adalah 4, skor Frequency adalah 5, dan skor Monetary adalah 3, maka RFM Score pelanggan tersebut adalah 453.</div>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: left;'>Segmentasi Pelanggan berdasarkan RFM Score</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Berdasarkan RFM Score, pelanggan dapat dikelompokkan ke dalam beberapa segmen, antara lain:</div>", unsafe_allow_html=True)
    st.markdown("<ul><li>Champions (Skor 511 - 555): Pelanggan dengan skor tinggi di semua kategori.</li><li>Loyal (Skor 451 - 510): Pelanggan yang setia dan sering bertransaksi.</li><li>Potential (Skor 351 - 450): Pelanggan yang potensial namun perlu lebih banyak interaksi.</li><li>At Risk (Skor 151 - 350): Pelanggan yang berisiko hilang namun masih memiliki potensi tinggi.</li><li>Uncategorized (Skor di bawah 150): Pelanggan yang tidak masuk ke kategori lainnya.</li></ul>", unsafe_allow_html=True)

    # Create RFM Table
    rfm_table = df.groupby('_CustomerID').agg(Last_Transaction=('OrderDate', 'max'),Frequency=('OrderNumber', 'nunique'),
                    Monetary=('Sales per Order', 'sum')).reset_index()

    rfm_table['Recency'] = (pd.to_datetime('2021-01-01') - rfm_table['Last_Transaction']).dt.days

    recency_percentiles = np.percentile(rfm_table['Recency'], [20, 40, 60, 80])
    rfm_table['R Score'] = pd.cut(rfm_table['Recency'], bins=[0, recency_percentiles[0], recency_percentiles[1], recency_percentiles[2], 
                                                              recency_percentiles[3], np.inf], labels=[5, 4, 3, 2, 1], right=False)

    frequency_percentiles = np.percentile(rfm_table['Frequency'], [20, 40, 60, 80])
    rfm_table['F Score'] = pd.cut(rfm_table['Frequency'], bins=[0, frequency_percentiles[0], frequency_percentiles[1], frequency_percentiles[2], 
                                                                frequency_percentiles[3], np.inf], labels=[1, 2, 3, 4, 5], right=False)

    monetary_percentiles = np.percentile(rfm_table['Monetary'], [20, 40, 60, 80])
    rfm_table['M Score'] = pd.cut(rfm_table['Monetary'], bins=[0, monetary_percentiles[0], monetary_percentiles[1], monetary_percentiles[2], 
                                                               monetary_percentiles[3], np.inf], labels=[1, 2, 3, 4, 5], right=False)

    rfm_table['RFM Score'] = rfm_table['R Score'].astype(str) + rfm_table['F Score'].astype(str) + rfm_table['M Score'].astype(str)

    def customer_segment(rfm_score):
        if rfm_score >= "511" and rfm_score <= "555":
            return "Champions"
        elif rfm_score >= "451" and rfm_score <= "510":
            return "Loyal"
        elif rfm_score >= "351" and rfm_score <= "450":
            return "Potential"
        elif rfm_score >= "151" and rfm_score <= "350":
            return "At Risk"
        else:
            return "Uncategorized"

    rfm_table['Customer Segment'] = rfm_table['RFM Score'].apply(customer_segment)

    # Display RFM Table with range sliders for Recency, Frequency, and Monetary
    recency_range = st.slider("Select Recency Range", min_value=int(rfm_table['Recency'].min()), max_value=int(rfm_table['Recency'].max()), 
                              value=(int(rfm_table['Recency'].min()), int(rfm_table['Recency'].max())), key="recency_slider")
    frequency_range = st.slider("Select Frequency Range", min_value=int(rfm_table['Frequency'].min()), max_value=int(rfm_table['Frequency'].max()), 
                                value=(int(rfm_table['Frequency'].min()), int(rfm_table['Frequency'].max())), key="frequency_slider")
    monetary_range = st.slider("Select Monetary Range", min_value=int(rfm_table['Monetary'].min()), max_value=int(rfm_table['Monetary'].max()), 
                               value=(int(rfm_table['Monetary'].min()), int(rfm_table['Monetary'].max())), key="monetary_slider")

    # Filter the data based on the sliders
    filtered_rfm = rfm_table[
        (rfm_table['Recency'] >= recency_range[0]) & (rfm_table['Recency'] <= recency_range[1]) &
        (rfm_table['Frequency'] >= frequency_range[0]) & (rfm_table['Frequency'] <= frequency_range[1]) &
        (rfm_table['Monetary'] >= monetary_range[0]) & (rfm_table['Monetary'] <= monetary_range[1])
    ]

    # Display filtered data
    st.write("Filtered RFM Table based on the selected ranges:")
    st.dataframe(filtered_rfm)

    # Merge RFM data into the main dataframe for visualization
    df = df.merge(rfm_table[['_CustomerID', 'Customer Segment']], on='_CustomerID', how='left')

    # Visualizations based on the selected segment
    segment_filter = st.multiselect(
        "Select Customer Segment", 
        options=["Champions", "Loyal", "Potential", "At Risk", "Uncategorized"],
        default=["Champions", "Loyal"])

    # Memfilter data berdasarkan pilihan multi select
    if segment_filter:
        df = df[df['Customer Segment'].isin(segment_filter)]

    # Visualizations (Sales Volume by Product, Segment Distribution, etc.)
    tabs = st.tabs(["Customer Segment Distribution", "Sales Volume by Product", "Sales Volume by Channel", "Sales vs Order", "Sales and Profit by Segment"])

    with tabs[0]:
        # Aggregate Customer IDs by Customer Segment
        customer_count = df.groupby('Customer Segment')['_CustomerID'].nunique().reset_index()

        # Create a pie chart for Customer Segment Distribution
        fig2 = px.pie(customer_count, names="Customer Segment", values="_CustomerID", 
                      title="Customer Segment Distribution", 
                      labels={'_CustomerID': 'Number of Customers'})
        st.plotly_chart(fig2)

    with tabs[1]:
        # Aggregate Order Quantity by Product ID and Customer Segment
        sales_by_product = df.groupby(['_ProductID', 'Customer Segment'])['Order Quantity'].sum().reset_index()

        # Create a bar chart for Sales Volume by Product and Customer Segment
        fig1 = px.bar(sales_by_product, x="_ProductID", y="Order Quantity", 
                      color="Customer Segment", 
                      title="Sales Volume by Product and Customer Segment", 
                      labels={'Order Quantity': 'Sales Volume'},
                      color_discrete_map={"At Risk": "darkred", "Potential": "orange", "Champions": "green", "Uncategorized": "purple", "Loyal": "blue"})
        
        # Customize the layout for better clarity
        fig1.update_layout(xaxis_title="Product ID",yaxis_title="Sales Volume",xaxis_tickangle=-45)
        st.plotly_chart(fig1)

    with tabs[2]:
        # Aggregate Order Quantity by Sales Channel and Customer Segment
        sales_by_channel = df.groupby(['Sales Channel', 'Customer Segment'])['Order Quantity'].sum().reset_index()
        
        # Create a bar chart with better coloring
        fig3 = px.bar(sales_by_channel, x="Sales Channel", y="Order Quantity", 
                      color="Customer Segment", 
                      title="Sales Volume by Sales Channel and Customer Segment", 
                      labels={'Order Quantity': 'Sales Volume'},
                      color_discrete_map={"At Risk": "darkred", "Potential": "orange", "Champions": "green", "Uncategorized": "purple", "Loyal": "blue"})
        
        # Customize the layout for better clarity
        fig3.update_layout(xaxis_title="Sales Channel",yaxis_title="Sales Volume",barmode='stack', xaxis_tickangle=-45)
        st.plotly_chart(fig3)

    with tabs[3]:
        # Aggregate data by Customer Segment and Customer ID
        customer_order_sales = df.groupby(['_CustomerID', 'Customer Segment']).agg(
            distinct_orders=('OrderNumber', 'nunique'),total_sales=('Sales per Order', 'sum')).reset_index()
        # Create scatter plot with distinct orders on x-axis and total sales on y-axis
        fig4 = px.scatter(customer_order_sales, 
                        x='distinct_orders', 
                        y='total_sales', 
                        color='Customer Segment', 
                        title="Distribution of Sales and Order Quantity by Customer Segment", 
                        labels={'distinct_orders': 'Distinct Order Count', 'total_sales': 'Total Sales'})
        # Customize the scatter plot for better visibility
        fig4.update_layout(xaxis_title="Distinct Order Count",yaxis_title="Total Sales",showlegend=True)
        st.plotly_chart(fig4)

    with tabs[4]:
        # Aggregate Sales per Order and Profit per Order by Customer Segment
        df_segmented = df.groupby("Customer Segment")[["Sales per Order", "Profit per Order"]].sum().reset_index()
        # Create a bar chart for Sales and Profit by Customer Segment
        fig5 = px.bar(df_segmented, 
                    x="Customer Segment", 
                    y=["Sales per Order", "Profit per Order"], 
                    title="Total Sales and Profit by Customer Segment", 
                    labels={'Customer Segment': 'Customer Segment', 
                            'value': 'Amount', 
                            'variable': 'Metrics'},
                    barmode='group')  # Group bars by Customer Segment

        # Customize the layout for better clarity
        fig5.update_layout(
            xaxis_title="Customer Segment",
            yaxis_title="Amount",
            showlegend=True
        )
        st.plotly_chart(fig5)

    st.markdown("<h2 style='text-align: left;'>Recommendation</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: justify;'>Fokuskan di saluran In-Store dan Online:</div>", unsafe_allow_html=True)
    st.markdown("<ul><li><div style='text-align: justify;'>Berikan pengalaman belanja yang menyenangkan di In-Store dan Online. Tawarkan produk-produk favorit yang sering dibeli, seperti di In-Store ada produk ID 23,27,37,17 dan 4 serta di Onlien ada product ID 12,4,23,39 dan 29. Pastikan produk-produk ini menjadi prioritas dalam promosi dan penyediaan stok.</div>", unsafe_allow_html=True)
    st.markdown("<ul><li><div style='text-align: justify;'>Evaluasi produk yang jarang dibeli dan tawarkan promo atau bundling produk terlaris untuk meningkatkan minat beli.</div>", unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: justify;'>Mempertahankan Champions dan Loyal:</div>", unsafe_allow_html=True)
    st.markdown("<ul><li><div style='text-align: justify;'>Champions : Lakukan upselling dan cross-selling produk terlaris di saluran In-Store dan Online. Tawarkan exclusive deals dan pengalaman premium untuk menjaga loyalitas mereka. Misalnya, produk ID 36 dan 41 bisa menjadi produk unggulan dalam program loyalitas. Untuk menjaga keterlibatan mereka, beri konten eksklusif seperti preview produk baru atau undangan acara khusus.</div>", unsafe_allow_html=True)
    st.markdown("<ul><li><div style='text-align: justify;'>Loyal : Tingkatkan frekuensi pembelian dengan loyalty program dan penawaran yang dipersonalisasi, serta exclusive bundles untuk produk-produk yang mereka minati seperti ID 21, 23, dan 25.</div>", unsafe_allow_html=True)
   
    st.markdown("<h5 style='text-align: justify;'>Meningkatkan Segmen At Risk ke Potential atau Loyal dan Segmen Potential ke Loyal atau Champions:</div>", unsafe_allow_html=True)
    st.markdown("<ul><li><div style='text-align: justify;'>At Risk : Terapkan kampanye retensi dengan promosi produk yang mereka minati, seperti produk id 23 dan 41. Gunakan pendekatan personal seperti email automation dan push notifications dengan penawaran berbasis waktu yang relevan.</div>", unsafe_allow_html=True)
    st.markdown("<ul><li><div style='text-align: justify;'>Potential : Fokuskan promosi pada produk ID 15, 22, dan 38 untuk menarik minat segmen At Risk dan mengkonversinya menjadi Loyal atau Champions. Perbaiki pengalaman di saluran In-Store dan Online dengan penawaran menarik dan relevansi produk untuk meningkatkan penjualan dan frekuensi pembelian.</div>", unsafe_allow_html=True)
   
# Menjalankan aplikasi
if __name__ == "__main__":
    project()