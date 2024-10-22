import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load Excel file
file_path = 'Quantace - Performance Oct 2024.xlsx'
xls = pd.ExcelFile(file_path)

# Load the two worksheets
basket_df = pd.read_excel(xls, sheet_name='Quantace - Daily Returns %')
index_df = pd.read_excel(xls, sheet_name='Index Daily Returns %')

# Convert the Date column to datetime format
basket_df['Date'] = pd.to_datetime(basket_df['Date'], format='%d-%m-%Y')
index_df['Date'] = pd.to_datetime(index_df['Date'], format='%d-%m-%Y')

# Set Date as the index for easier filtering later
basket_df.set_index('Date', inplace=True)
index_df.set_index('Date', inplace=True)

# Streamlit app
# st.title('Quantace Baskets vs Benchmark Index')

# Dropdowns for selecting the basket and the benchmark index
selected_basket = st.selectbox('Select Quantace Basket:', basket_df.columns[1:])
selected_index = st.selectbox('Select Benchmark Index:', index_df.columns[1:])

# Filter data based on the selected basket and index
basket_data = basket_df[[selected_basket]].dropna()
index_data = index_df[[selected_index]].dropna()

# Align the index data to the same start date as the basket data
start_date = basket_data.index.min()
index_data = index_data[index_data.index >= start_date]

# Ensure dates match between basket and index
basket_data = basket_data[basket_data.index.isin(index_data.index)]
index_data = index_data[index_data.index.isin(basket_data.index)]

# Calculate cumulative returns
basket_cum_returns = (1 + basket_data).cumprod() - 1
index_cum_returns = (1 + index_data).cumprod() - 1

# Create Plotly figure
fig = go.Figure()

# Add the basket cumulative returns (red line)
fig.add_trace(go.Scatter(x=basket_cum_returns.index, y=basket_cum_returns[selected_basket], 
                         mode='lines', name=f'{selected_basket} (Basket)', line=dict(color='red')))

# Add the index cumulative returns (blue line)
fig.add_trace(go.Scatter(x=index_cum_returns.index, y=index_cum_returns[selected_index], 
                         mode='lines', name=f'{selected_index} (Index)', line=dict(color='blue')))

# Update layout
fig.update_layout(title=f'Cumulative Returns: {selected_basket} vs {selected_index}',
                  xaxis_title='Date', yaxis_title='Cumulative Return',
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Display the plot
st.plotly_chart(fig)

# Calculate the difference between the basket and index cumulative returns
cumulative_return_diff = basket_cum_returns[selected_basket] - index_cum_returns[selected_index]

# Create a new Plotly figure for the difference
fig_diff = go.Figure()

# Add the difference line (green line)
fig_diff.add_trace(go.Scatter(x=cumulative_return_diff.index, y=cumulative_return_diff, 
                              mode='lines', name='Basket - Index (Difference)', 
                              line=dict(color='green')))

# Update layout for the difference plot
fig_diff.update_layout(title=f'Cumulative Return Difference: {selected_basket} - {selected_index}',
                       xaxis_title='Date', yaxis_title='Cumulative Return Difference',
                       legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Display the difference plot
st.plotly_chart(fig_diff)

