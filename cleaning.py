import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
brands_path = "./brands.csv"
categories_path = "./categories.csv"
customers_path = "./customers.csv"
orders_path = "./orders.csv"
order_items_path = "./order_items.csv"
products_path = "./products.csv"
staffs_path = "./staffs.csv"
stores_path = "./stores.csv"
stocks_path = "./stocks.csv"



brands_df = pd.read_csv(brands_path)
categories_df = pd.read_csv(categories_path)
customers_df = pd.read_csv(customers_path)
orders_df = pd.read_csv(orders_path, parse_dates=['order_date', 'required_date', 'shipped_date'])
order_items_df = pd.read_csv(order_items_path)
products_df = pd.read_csv(products_path)
staffs_df = pd.read_csv(staffs_path)
stores_df = pd.read_csv(stores_path)
stocks_df = pd.read_csv(stocks_path)
# brands_df
# categories_df
# customers_df['phone']= customers_df['phone'].fillna('no phone number')
# customers_df.isnull().sum()
# orders_df.info()

# order_items_df
# products_df.drop(columns=['list_price'], inplace=True)
# staffs_df
# stores_df
# stocks_df
order_items_df['sales'] = order_items_df['quantity']*order_items_df['list_price']*(1-order_items_df['discount'])

# products_df
brands_df[brands_df.duplicated()]
order_items_df['profit'] = order_items_df['sales'] - (order_items_df['quantity']*order_items_df['discount']*100)
# order_items_df
order_items_df['discount_value'] = order_items_df['quantity']* order_items_df['list_price']*order_items_df['list_price']*order_items_df['discount']
# order_items_df
orders_df['shipping_days'] = (orders_df['shipped_date'] - orders_df['order_date']).dt.days
# orders_df
cancelled_orders = orders_df[orders_df['shipped_date'].isnull()]
total_cancelled_orders =len(cancelled_orders)
total_cancelled_orders
estimated_loss = cancelled_orders.merge(order_items_df, on='order_id', how='left')['sales'].sum()
estimated_loss
kpi = {
    "total_sales": order_items_df['sales'].sum()-estimated_loss,
    "total_profit": order_items_df['discount_value'].sum(),
    "avg_discount": order_items_df['discount'].sum()/len(orders_df),
    "avg_shipping_days": orders_df['shipping_days'].mean(),
    "potential sales loss":estimated_loss
    
}
kpi
temp_order = order_items_df.merge(orders_df)
placed_order_table = temp_order[~temp_order["shipped_date"].isna()]
placed_order_table["order_month"] = placed_order_table["order_date"].dt.month_name()
placed_order_table["order_year"] = placed_order_table["order_date"].dt.year
# placed_order_table
year_month_sales = placed_order_table.pivot_table(
    index="order_year",
    columns="order_month",
    values="sales",
    aggfunc="sum"
)
# year_month_sales
# sns.heatmap(year_month_sales)
brand_year_month_sales = placed_order_table.merge(products_df).merge(brands_df).pivot_table(
    index=["order_year","order_month"],
    columns="brand_name",
    values="sales",
    aggfunc="sum"
)
# brand_year_month_sales
# plt.figure(figsize=(15,5))
# brand_year_month_sales.plot()
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()
brand_sales = (
    placed_order_table
    .merge(products_df)
    .merge(brands_df)
)

brand_year_month_sales = brand_sales.pivot_table(
    index=["order_year", "order_month"],
    columns="brand_name",
    values="sales",
    aggfunc="sum"
)

brand_sales_long = brand_year_month_sales.reset_index().melt(
    id_vars=["order_year", "order_month"],
    var_name="brand_name",
    value_name="total_sales"
)

# brand_sales_long["year_month"] = (
#     brand_sales_long["order_year"].astype(str)
#     + "-"
#     + brand_sales_long["order_month"].astype(str).str.zfill(2)
# )

# brand_sales_long = brand_sales_long.rename(
#     columns={"total_sales": "sales"}
# )

# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.figure(figsize=(15, 5))

# sns.lineplot(
#     data=brand_sales_long,
#     x="order_month",
#     y="total_sales",
#     hue="brand_name",
#     style="order_year",
#     marker="o"
# )

# plt.title("Brand-wise Monthly Sales Trend")
# plt.xlabel("Month")
# plt.ylabel("Total Sales")
# plt.xticks(rotation=45)
# plt.legend(title="Brand / Year")
# plt.tight_layout()
# plt.show()
def month_no(month_name):
    month_dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return month_dict[month_name]





df = placed_order_table.copy()
def month_no(month_name):
    month_dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return month_dict[month_name]
df["month_no"] = df["order_month"].apply(month_no)

df["year_month"] = (
    df["order_year"].astype(str) + "-" +
    df["month_no"].astype(str).str.zfill(2)
)

# df
category_wise_sales = placed_order_table.merge(products_df).merge(categories_df).pivot_table(
    index="category_name",
     values="sales",
    aggfunc="sum"
).sort_values(by="sales", ascending=False).reset_index()
# plot(kind="bar", figsize=(10, 5), title="Sales by Category")


store_sales = placed_order_table.merge(stores_df).pivot_table(
    index="store_name",
    values="sales",
    aggfunc="sum"
).sort_values(by="sales", ascending=False).reset_index()



# price vs sales scatter plot
price_sales_df = placed_order_table.merge(products_df)
