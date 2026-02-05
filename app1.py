# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px



st.set_page_config(page_title="Supply Chain Analytics Dashboard", layout="wide")

# --- Load data ---
df = pd.read_csv("supply_chain_data.csv")

st.title("📊 Supply Chain Analytics Dashboard")

# -------------------------------
# Q1: Total Revenue by Product Type
# -------------------------------
st.subheader("1️⃣ Total Revenue by Product Type")
df_tot_revenue = df.groupby('Product type').agg(Total_Revenue=('Revenue generated','sum')).reset_index()
df_tot_revenue['Total_Revenue'] = df_tot_revenue['Total_Revenue'].round(0)

fig1, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df_tot_revenue, x='Product type', y='Total_Revenue', palette='viridis', ax=ax)
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.0f}', (p.get_x()+p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10, fontweight='bold', xytext=(0,5), textcoords='offset points')
ax.set_title('Total Revenue by Product Type', fontsize=14, fontweight='bold')
ax.set_xlabel('Product Type')
ax.set_ylabel('Total Revenue')
plt.xticks(rotation=30)
st.pyplot(fig1)

# -------------------------------
# Q2: Price vs Number of Products Sold
# -------------------------------
st.subheader("2️⃣ Price vs Number of Products Sold")
fig2, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=df, x='Price', y='Number of products sold',
                hue='Product type', size='Revenue generated', sizes=(50,300),
                alpha=0.7, palette='tab10', ax=ax)
ax.set_title('Price vs Number of Products Sold', fontsize=14, fontweight='bold')
ax.set_xlabel('Price')
ax.set_ylabel('Number of Products Sold')
st.pyplot(fig2)

# -------------------------------
# Q3: Average Lead Time by Supplier
# -------------------------------
st.subheader("3️⃣ Average Lead Time by Supplier")
df_sup_lt = df.groupby('Supplier name').agg(Supplier_Avg_Lead_Time=("Lead time","mean")).reset_index()
df_sup_lt['Supplier_Avg_Lead_Time'] = df_sup_lt['Supplier_Avg_Lead_Time'].round(2)

fig3, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df_sup_lt, x='Supplier name', y='Supplier_Avg_Lead_Time', palette='Blues_d', ax=ax)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}', (p.get_x()+p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10, fontweight='bold', xytext=(0,4), textcoords='offset points')
ax.set_title('Average Lead Time by Supplier', fontsize=14, fontweight='bold')
ax.set_xlabel('Supplier')
ax.set_ylabel('Avg Lead Time (Days)')
plt.xticks(rotation=30)
st.pyplot(fig3)

# -------------------------------
# Q4: Stock Levels vs Products Sold
# -------------------------------
st.subheader("4️⃣ Stock Levels vs Products Sold")
fig4, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(data=df, x='Stock levels', y='Number of products sold', alpha=0.7, ax=ax)
ax.set_title('Stock Levels vs Products Sold', fontsize=13, fontweight='bold')
ax.set_xlabel('Stock Levels')
ax.set_ylabel('Number of Products Sold')
st.pyplot(fig4)

# -------------------------------
# Q5: Defect Rates by Supplier
# -------------------------------
st.subheader("5️⃣ Defect Rates by Supplier")
fig5, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df, x='Supplier name', y='Defect rates', palette='Reds', ax=ax)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%', (p.get_x()+p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10, fontweight='bold', xytext=(0,4), textcoords='offset points')
ax.set_title('Defect Rates by Supplier', fontsize=14, fontweight='bold')
ax.set_xlabel('Supplier')
ax.set_ylabel('Defect Rate (%)')
plt.xticks(rotation=30)
st.pyplot(fig5)

# -------------------------------
# Q6: Transportation Cost by Mode (Plotly)
# -------------------------------
st.subheader("6️⃣ Average Transportation Cost by Mode")
df_tx_cost = df.groupby("Transportation modes").agg(Avg_transportation_cost=("Costs","mean")).reset_index()
df_tx_cost['Avg_transportation_cost'] = df_tx_cost['Avg_transportation_cost'].round(0)
df_tx_cost_sorted = df_tx_cost.sort_values(by='Avg_transportation_cost', ascending=False)

fig6 = px.bar(
    df_tx_cost_sorted,
    x='Transportation modes',
    y='Avg_transportation_cost',
    text='Avg_transportation_cost',
    title='Average Transportation Cost by Mode',
    color='Avg_transportation_cost',
    color_continuous_scale='Blues'
)
fig6.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig6.update_layout(xaxis_title='Transportation Mode', yaxis_title='Average Transportation Cost',
                   title_font=dict(size=18), xaxis=dict(tickangle=-30), plot_bgcolor='white')
st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# Q7: Shipping Times vs Costs by Carrier (Plotly)
# -------------------------------
st.subheader("7️⃣ Shipping Times vs Costs by Carrier")
fig7 = px.scatter(
    df,
    x='Shipping times',
    y='Shipping costs',
    color='Shipping carriers',
    size='Shipping costs',
    hover_data=['Shipping carriers', 'Shipping times', 'Shipping costs'],
    title='Shipping Times vs Shipping Costs by Carrier',
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig7.update_traces(marker=dict(size=12, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
fig7.update_layout(xaxis_title='Shipping Times (Days)', yaxis_title='Shipping Costs ($)',
                   title_font=dict(size=18), plot_bgcolor='white')
st.plotly_chart(fig7, use_container_width=True)

# -------------------------------
# Q8: High-Risk SKU Identification
# -------------------------------
st.subheader("8️⃣ High-Risk SKU Identification")
# Standardize metrics
df['Stock_norm'] = (df['Stock levels'] - df['Stock levels'].min()) / (df['Stock levels'].max() - df['Stock levels'].min())
df['Sales_norm'] = (df['Number of products sold'] - df['Number of products sold'].min()) / (df['Number of products sold'].max() - df['Number of products sold'].min())
df['LeadTime_norm'] = (df['Lead time'] - df['Lead time'].min()) / (df['Lead time'].max() - df['Lead time'].min())
df['RiskScore'] = df['Stock_norm']*0.4 + (1 - df['Sales_norm'])*0.4 + df['LeadTime_norm']*0.2
def risk_zone(score):
    if score > 0.7:
        return "High Risk"
    elif score > 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"
df['RiskZone'] = df['RiskScore'].apply(risk_zone)

fig8, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=df, x='Stock levels', y='Number of products sold', hue='RiskZone',
                size='Lead time', sizes=(50,300),
                palette={"Low Risk":"green","Medium Risk":"orange","High Risk":"red"},
                alpha=0.7, ax=ax)
top_risk = df[df['RiskZone']=="High Risk"].sort_values('RiskScore', ascending=False)
for idx,row in top_risk.head(5).iterrows():
    ax.text(row['Stock levels'], row['Number of products sold'], row['SKU'], fontsize=9, fontweight='bold')
ax.set_title("High-Risk SKU Identification")
st.pyplot(fig8)

# -------------------------------
# Q9: Products Prioritized for Replenishment
# -------------------------------
st.subheader("9️⃣ Products Prioritized for Replenishment")
df['Stock_norm'] = 1 - ((df['Stock levels'] - df['Stock levels'].min()) / 
                        (df['Stock levels'].max() - df['Stock levels'].min()))
df['Order_norm'] = (df['Order quantities'] - df['Order quantities'].min()) / \
                   (df['Order quantities'].max() - df['Order quantities'].min())
df['LeadTime_norm'] = (df['Lead time'] - df['Lead time'].min()) / \
                      (df['Lead time'].max() - df['Lead time'].min())
df['PriorityScore'] = df['Stock_norm']*0.4 + df['Order_norm']*0.4 + df['LeadTime_norm']*0.2
def priority_zone(score):
    if score > 0.7:
        return "High Priority"
    elif score > 0.4:
        return "Medium Priority"
    else:
        return "Low Priority"
df['PriorityZone'] = df['PriorityScore'].apply(priority_zone)

fig9, ax = plt.subplots(figsize=(12,7))
sns.scatterplot(data=df, x='Stock levels', y='Order quantities', size='Lead time', hue='PriorityZone',
                palette={"Low Priority":"green", "Medium Priority":"orange", "High Priority":"red"},
                sizes=(50,500), alpha=0.7, ax=ax)
top_priority = df[df['PriorityZone']=="High Priority"].sort_values('PriorityScore', ascending=False)
for idx,row in top_priority.head(5).iterrows():
    ax.text(row['Stock levels'], row['Order quantities'], row['SKU'], fontsize=9, fontweight='bold')
ax.set_title("Products Prioritized for Replenishment")
ax.set_xlabel("Stock Levels")
ax.set_ylabel("Order Quantities")
st.pyplot(fig9)

# -------------------------------
# Q10: Top 5 Products Sold by Quantity
# -------------------------------
st.subheader("🔟 Top 5 Products Sold by Quantity")
df_sku_sold = df.groupby("SKU").agg(Total_Qty_Sold=("Number of products sold","sum")).reset_index()
df_sku_sold = df_sku_sold.sort_values(by='Total_Qty_Sold', ascending=False).head(5)

fig10 = px.bar(df_sku_sold, x='SKU', y='Total_Qty_Sold', text='Total_Qty_Sold',
               color='Total_Qty_Sold', color_continuous_scale='Viridis', title='Top 5 Products Sold by Quantity')
fig10.update_traces(texttemplate='%{text:,}', textposition='outside')
fig10.update_layout(xaxis_title='SKU', yaxis_title='Total Quantity Sold', xaxis_tickangle=-30, plot_bgcolor='white')
st.plotly_chart(fig10, use_container_width=True)
