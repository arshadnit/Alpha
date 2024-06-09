import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px



df=pd.read_csv('Desktop/Alpha2.csv')



# Read the CSV file from the URL
try:
    df = pd.read_csv(csv_url)
    st.write("CSV file loaded successfully.")
    st.write(df.head())
    st.write("Columns in the DataFrame:", df.columns)
except Exception as e:
    st.write("Error loading CSV file:", e)

# Ensure 'region' column exists before using it
if 'region' in df.columns:
    region = st.sidebar.multiselect("Choose Region", df['region'].unique())
else:
    st.write("The 'region' column does not exist in the DataFrame.")




st.set_page_config(layout='wide',initial_sidebar_state='expanded')

st.title(' :shirt: :dress: :shoe: Alpha')
#st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#************ Sidebar **************

st.sidebar.header("Filters")

region=st.sidebar.multiselect("Choose Region", df['region'].unique())
gender=st.sidebar.multiselect("Choose Gender", df['product_gender_target'].unique())



#Filtering data based on region and gender

filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df['region'].isin(region)]
if gender:
    filtered_df = filtered_df[filtered_df['product_gender_target'].isin(gender)]

if region and gender:
    filtered_df = filtered_df[(filtered_df['region'].isin(region)) & (filtered_df['product_gender_target'].isin(gender))]

if not region and not gender:
    filtered_df = df.copy()



#************* Section 1 *****************

clothing_type_df=filtered_df['clothing_type'].value_counts().reset_index()
clothing_type_df.columns = ['Clothing Type', 'Sales']

product_category_df=filtered_df['product_category'].value_counts().reset_index()
product_category_df.columns = ['Category', 'Sales']


col1, col2 = st.columns((2))

with col1:
    st.subheader("Clothing Type")
    fig=px.bar(clothing_type_df, x="Clothing Type", y="Sales", template='seaborn')
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Product Type")
    fig=px.pie(product_category_df, names="Category", values="Sales", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)


cl1, cl2=st.columns(2)

with cl1:
    with st.expander("Clothing Type - ViewData"):
        st.write(clothing_type_df.style.background_gradient(cmap='Blues'))
        csv=clothing_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", csv, "clothing_type.csv", "text/csv", help="Click here to download") 


with cl2:
    with st.expander("Product Type - ViewData"):
        st.write(product_category_df.style.background_gradient(cmap='Oranges'))
        csv=product_category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", csv, "product_type.csv", "text/csv", help="Click here to download") 


#******************** Section 2 ************************

st.subheader("Shipping Time")

average_shipping_time_df = df.groupby('region')['usually_ships_within'].mean().reset_index()
fig = px.violin(df, x='region', y='usually_ships_within', color='region', 
                title='Distribution of Shipping Times by Region',
                labels={'region': 'Region', 'usually_ships_within': 'Shipping Time (days)'},
                template='seaborn')

st.plotly_chart(fig, use_container_width=True)


with st.expander("Average Shipping Time - ViewData"):
    st.write(average_shipping_time_df.style.background_gradient(cmap='Blues'))
    csv=average_shipping_time_df .to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", csv, "shipping_time.csv", "text/csv", help="Click here to download") 


#******************* Section 3 ******************************

chart1, chart2, chart3=st.columns((3))

colors_df= filtered_df['product_color'].value_counts().head(5).reset_index()
colors_df.columns = ['Color', 'Sales']

top_brands_df= filtered_df['brand_name'].value_counts().head(5).reset_index()
top_brands_df.columns = ['Brand', 'Sales']

materials_df= filtered_df['product_material'].value_counts().head(5).reset_index()
materials_df.columns = ['Material', 'Sales']


with chart1:
    st.subheader("Top 5 Colors")
    fig = px.histogram(colors_df, x='Color', y='Sales',
                   labels={'Color': 'Color', 'Sales': 'Number of Sales'},
                   template='seaborn')
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Top 5 Brands")
    fig = px.pie(top_brands_df, values='Sales', names='Brand', hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

with chart3:
    st.subheader("Top 5 Materials")
    fig = px.line(materials_df, x='Material', y='Sales',
                   labels={'Material': 'Material', 'Sales': 'Number of Sales'},
                   template='seaborn')
    st.plotly_chart(fig, use_container_width=True)


ch1, ch2, ch3=st.columns((3))

with ch1:
    with st.expander("Top 5 Colors - ViewData"):
        st.write(colors_df.style.background_gradient(cmap='Blues'))
        csv=colors_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", csv, "top5colors.csv", "text/csv", help="Click here to download") 


with ch2:
    with st.expander("Top 5 Brands - ViewData"):
        st.write(top_brands_df.style.background_gradient(cmap='Oranges'))
        csv=top_brands_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", csv, "top5brands.csv", "text/csv", help="Click here to download") 

with ch3:
    with st.expander("Top 5 Materials - ViewData"):
        st.write(materials_df.style.background_gradient(cmap='Oranges'))
        csv=materials_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", csv, "top5materials.csv", "text/csv", help="Click here to download") 



#**************Section 4************************

st.subheader("Europe Market Analysis")

df_europe = df[df['region'] == 'Europe']

average_price_per_country_brand = df_europe.groupby(['seller_country', 'brand_name'])['seller_price'].mean().reset_index()

top_10_countries = df_europe['seller_country'].value_counts().nlargest(10).index

top_brand_per_country = {}
for country in top_10_countries:
    top_brand_per_country[country] = df_europe[df_europe['seller_country'] == country]['brand_name'].value_counts().nlargest(1).index

fig = px.line(title='Average Price per Country and Brand in Europe')

for country in top_10_countries:
    for brand in top_brand_per_country[country]:
        data = average_price_per_country_brand[(average_price_per_country_brand['seller_country'] == country) & (average_price_per_country_brand['brand_name'] == brand)]
        if not data.empty:
            fig.add_scatter(x=data['seller_country'], y=data['seller_price'], mode='lines+markers', name=f'{country} - {brand}')


fig.update_xaxes(title='Country')
fig.update_yaxes(title='Average Price')
fig.update_layout(xaxis=dict(tickangle=45))


st.plotly_chart(fig, use_container_width=True)


with st.expander("Europe Market Analysis"):
    csv_data = average_price_per_country_brand.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Data as CSV", data=csv_data, file_name="europe_market_analysis.csv", mime="text/csv")
