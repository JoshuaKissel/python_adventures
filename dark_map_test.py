token = "pk.eyJ1Ijoiam9zaC1hdC10cmFmZmljdmlzaW9uLWRvdC1jb20iLCJhIjoiY2t1OG8weG56NXg4MjJvcG1obXZ5YWpkMyJ9.k0l3DwPOzhvTXROGhLgU-A"
 # you will need your own token

import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

import plotly.express as px

fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()