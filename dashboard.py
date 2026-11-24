import cleaning
import streamlit as st
import plotly.express as px
# python -m pip install statsmodels


st.title("Bike Store Sales Dashboard")

st.set_page_config(page_title="Bike Store Sales Dashboard", page_icon=":bar chart:", layout="wide")

col1,col2,col3 = st.columns(3)

target_sales = st.sidebar.slider(
    "Set Target Sales",
    min_value=300000,
    max_value=7000000,
    value=50000
)
    


with col1:
    st.metric( label="Total Sales", 
              value=f"${cleaning.kpi['total_sales']:,.2f}",
              delta=f"${(cleaning.kpi['total_sales']-target_sales)/target_sales*100:,.2f}%")


with col2:
    st.metric( label="Total Profit", value=f"${cleaning.kpi['total_profit']:,.2f}")


with col3:
    st.metric( label="Average Discount", value=f"{cleaning.kpi['avg_discount']:.2f}%")

col1,col2 = st.columns(2)

with col1:
    st.metric( label="Average Shipping Days", value=f"${cleaning.kpi['avg_shipping_days']:,.2f}")


with col2:
    st.metric( label="potential sales Loss", value=f"{cleaning.kpi['potential sales loss']:,.2f}")


col1,col2 = st.columns(2)

with col1:
    # line chart for sales by brand over time
        # st.line_chart(cleaning.brand_year_month_sales)  
        st.line_chart(cleaning.df,x="year_month",y="sales")
   

with col2:
     # bar chart for category wise sales
        st.bar_chart(cleaning.category_wise_sales,x="category_name",y="sales")
      
    


col1,col2 = st.columns(2)

with col1:
     st.dataframe(cleaning.year_month_sales,height=300)

with col2:
    #  store wise sales
    # st.bar_chart(cleaning.store_sales,x="store_name",y="sales")
    # pie chart for store wise sales
    # st.pie_chart(cleaning.store_sales,x="store_name",y="sales")
    fig = px.pie(
    cleaning.store_sales,
    names="store_name",
    values="sales",
    title="Store Wise Sales"
)

st.plotly_chart(fig)


col1,col2 = st.columns(2)
with col1:
    #  scatter plot for price vs sales
    # price_sales_df = cleaning.placed_order_table.merge(cleaning.products_df)
    fig = px.scatter(
   cleaning.price_sales_df, 
    x="list_price", 
        y="sales", 
        title="Price vs Sales ",
        trendline="ols"
    )
    st.plotly_chart(fig,use_container_width=True)
   

  