import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html

# Consolidated data
data = {
    'rp_ratio': {
        'Region': ['Middle East', 'CIS', 'Africa', 'S. & Cent. America', 'Asia Pacific', 'Europe', 'North America'],
        'R/P Ratio': [110.4, 70.5, 55.7, 51.7, 25.4, 14.5, 13.7]
    },
    'hydrogen_production': {
        'Region': ['North America', 'S. & Cent. America', 'Europe', 'CIS', 'Middle East', 'Africa', 'Asia Pacific', 'OECD', 'Non-OECD'],
        'Blue': [2091.6, 0, 44.1, 0, 621.9, 0, 1929.7, 2136.1, 2551.2],
        'Green': [19.4, 1.1, 31.6, 0, 0.1, 1.7, 93.6, 53.9, 93.8]
    },
    'gas_reserves': {
        'Year': list(range(1980, 2021)),
        'Reserves': [70.9, 73.5, 75.8, 77.4, 80.2, 82.4, 88.3, 90.8, 94.8, 105.5, 108.4, 114.2, 116.8, 118, 118.8, 119.1, 122.3, 125, 128.5, 131.9, 138, 152.5, 153.9, 154.6, 155, 153.4, 155.3, 162.7, 166, 169, 179.9, 181.9, 180.8, 181.3, 183.2, 181.2, 183.5, 187.8, 189.1, 190.3, 188.1]
    },
    'gas_production': {
        'Region': ['North America', 'S. & Cent. America', 'Europe', 'CIS', 'Middle East', 'Africa', 'Asia Pacific'],
        'Production': [1261.1, 162.0, 204.3, 773.6, 712.7, 253.6, 691.8]
    }
}

# Region to ISO mapping
region_to_iso = {
    'North America': ['USA', 'CAN', 'MEX'],
    'CIS': ['RUS', 'KAZ', 'UZB', 'TKM', 'KGZ', 'TJK'],
    'Middle East': ['SAU', 'IRN', 'IRQ', 'KWT', 'ARE', 'QAT', 'OMN', 'YEM', 'SYR', 'JOR', 'LBN', 'ISR'],
    'Africa': ['DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COM', 'COG', 'COD', 'DJI', 'EGY', 'GNQ', 'ERI', 'SWZ', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'CIV', 'KEN', 'LSO', 'LBR', 'LBY', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MAR', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TZA', 'TGO', 'TUN', 'UGA', 'ZMB', 'ZWE'],
    'S. & Cent. America': ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN'],
    'Asia Pacific': ['AFG', 'AUS', 'BGD', 'BTN', 'BRN', 'KHM', 'CHN', 'FJI', 'IND', 'IDN', 'JPN', 'KAZ', 'KIR', 'PRK', 'KOR', 'LAO', 'MYS', 'MDV', 'MHL', 'FSM', 'MNG', 'MMR', 'NPL', 'NZL', 'PAK', 'PLW', 'PNG', 'PHL', 'WSM', 'SGP', 'SLB', 'LKA', 'THA', 'TLS', 'TON', 'TUV', 'VUT', 'VNM'],
    'Europe': ['ALB', 'AND', 'ARM', 'AUT', 'AZE', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'KAZ', 'XKX', 'LVA', 'LIE', 'LTU', 'LUX', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TUR', 'UKR', 'GBR']
}

# Create DataFrames
df_rp = pd.DataFrame(data['rp_ratio'])
df_hydrogen = pd.DataFrame(data['hydrogen_production'])
df_gas_reserves = pd.DataFrame(data['gas_reserves'])
df_production = pd.DataFrame(data['gas_production'])

# Create map data for R/P Ratio
map_data_rp = [{'iso_alpha': iso, 'R/P Ratio': row['R/P Ratio']} 
               for _, row in df_rp.iterrows() 
               for iso in region_to_iso.get(row['Region'], [])]
map_df_rp = pd.DataFrame(map_data_rp)

# Create map data for Gas Production
map_data_production = [{'iso_alpha': iso, 'Production': row['Production']} 
                       for _, row in df_production.iterrows() 
                       for iso in region_to_iso.get(row['Region'], [])]
map_df_production = pd.DataFrame(map_data_production)

# Create figures
fig_rp = px.choropleth(map_df_rp, locations="iso_alpha", color="R/P Ratio",
                       hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.Plasma,
                       title="World Map: Reserves-to-Production (R/P) Ratio")
fig_rp.update_geos(projection_type="equirectangular")
fig_rp.update_layout(height=600, width=1200)

df_hydrogen['Total'] = df_hydrogen['Blue'] + df_hydrogen['Green']
df_hydrogen_sorted = df_hydrogen.sort_values('Total', ascending=False)
fig_hydrogen = go.Figure()
fig_hydrogen.add_trace(go.Bar(x=df_hydrogen_sorted['Region'], y=df_hydrogen_sorted['Blue'], name='Blue', marker_color='blue'))
fig_hydrogen.add_trace(go.Bar(x=df_hydrogen_sorted['Region'], y=df_hydrogen_sorted['Green'], name='Green', marker_color='green'))
fig_hydrogen.update_layout(title='Hydrogen Production by Region', xaxis=dict(title='Region'), yaxis=dict(title='Production (TWh)'), barmode='stack')

fig_gas_reserves = go.Figure()
fig_gas_reserves.add_trace(go.Scatter(x=df_gas_reserves['Year'], y=df_gas_reserves['Reserves'], mode='lines+markers', name='Gas Reserves'))
fig_gas_reserves.update_layout(title='Total World Gas Reserves (1980-2020)', xaxis_title='Year', yaxis_title='Reserves (Trillion cubic metres)')

fig_production = px.choropleth(map_df_production, locations="iso_alpha", color="Production",
                               hover_name="iso_alpha", color_continuous_scale=px.colors.sequential.YlOrRd,
                               title="Natural Gas Production by Region (2023)")
fig_production.update_geos(projection_type="natural earth")
fig_production.update_layout(height=600, width=1000)

# Create Dash app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Energy Data Visualization"),
    html.Div([html.H2("Reserves-to-Production (R/P) Ratio"), dcc.Graph(figure=fig_rp)]),
    html.Div([html.H2("Hydrogen Production by Region"), dcc.Graph(figure=fig_hydrogen)]),
    html.Div([html.H2("Total World Gas Reserves (1980-2020)"), dcc.Graph(figure=fig_gas_reserves)]),
    html.Div([html.H2("Natural Gas Production by Region (2023)"), dcc.Graph(figure=fig_production)])
])

if __name__ == '__main__':
    app.run_server(debug=True)
