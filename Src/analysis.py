import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# =========================
# LOAD DATA
# =========================
df = pd.read_csv('sales_data.csv')
df_clean = df.copy()

# =========================
# CLEANING
# =========================
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.dropna(subset=['Revenue'])

df_clean['Discount'] = (
    df_clean['Discount']
    .astype(str)
    .str.replace('%', '')
)

df_clean['Discount'] = pd.to_numeric(df_clean['Discount'], errors='coerce').fillna(0)

df_clean['Date'] = pd.to_datetime(df_clean['Date'])

df_clean['Region'] = df_clean['Region'].str.strip().str.title()

# =========================
# FEATURE ENGINEERING
# =========================
df_clean['Month'] = df_clean['Date'].dt.month

# =========================
# ANALYSIS
# =========================
grp_region = df_clean.groupby('Region')['Revenue'].sum().sort_values(ascending=False)

grp_category = df_clean.groupby('Category').agg(
    Total_Revenue=('Revenue', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Units=('Units_Sold', 'mean')
)

monthly = df_clean.groupby('Month')['Revenue'].sum().sort_index()

pivot_table = pd.pivot_table(
    df_clean,
    values='Revenue',
    index='Region',
    columns='Category',
    aggfunc='sum',
    fill_value=0
)

corr = df_clean[['Revenue', 'Profit', 'Units_Sold']].corr()

# =========================
# VISUALIZATION
# =========================
plt.figure()
df_clean['Revenue'].hist(bins=20)
plt.title("Revenue Distribution")

plt.figure()
df_clean.plot.scatter(x='Units_Sold', y='Revenue')
plt.title("Units vs Revenue")

# Category bar
cat_rev = df_clean.groupby('Category')['Revenue'].sum()
plt.figure(figsize=(8,4))
cat_rev.plot(kind='bar', color='#185FA5')
plt.title("Revenue by Category")
plt.tight_layout()

# Monthly trend
plt.figure()
monthly.plot(kind='line', marker='o')
plt.title("Monthly Revenue Trend")
plt.tight_layout()

plt.show()

# =========================
# EXPORT
# =========================
summary = grp_category.reset_index()

df_clean.to_csv('sales_clean.csv', index=False)

with pd.ExcelWriter('sales_report.xlsx') as writer:
    df_clean.to_excel(writer, sheet_name='Raw', index=False)
    summary.to_excel(writer, sheet_name='Summary', index=False)

fig = px.bar(summary, x='Category', y='Total_Revenue', title='Revenue by Category')
fig.write_html('dashboard.html')

sns.set(style="whitegrid")

plt.figure()
sns.barplot(data=summary, x='Category', y='Total_Revenue', palette='viridis')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('chart.png', dpi=150)
plt.close()

# =========================
# OUTPUT
# =========================
print(grp_region)
print(grp_category)
print(monthly)
print(pivot_table)
print(corr)