"""
import streamlit as st
import plotly.graph_objects as go
import json
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide", page_title="Indian States Welcome App")

st.title("Indian States Welcome App")

# Load the GeoJSON for Indian states
@st.cache_data
def load_geojson():
    with open("india_states.geojson") as response:
        geojson = json.load(response)
    return geojson

geojson = load_geojson()

# List of all Indian states from the geojson (to match codes)
states = [feature['properties']['NAME_1'] for feature in geojson['features']]

# Define the tourism information for each state
india_tourism_info = {
    "Andhra Pradesh": {
        "Top 10 Must-Visit Places": [
            {"name": "Tirumala Tirupati Devasthanams (Tirupati)", "image_url":r"Images\andhra\Tirupathi.jpg"},
            {"name": "Araku Valley", "image_url":r"Images\andhra\ArakuValley.jpg"},
            {"name": "Borra Caves", "image_url": r"Images\andhra\Borra-Cave.jpg"},
            {"name": "Visakhapatnam (Vizag): R.K. Beach, Kailasagiri", "image_url":r"Images\andhra\Visakhapatnam.jpg"},
            {"name": "Chilika Lake", "image_url":r"Images\andhra\Chilika-Lake.png"},
            {"name": "Sri Kalahasti Temple", "image_url":r"Images\andhra\kalahasteeswaraSwami.jpg"},
            {"name": "Nellore: Penchalakona", "image_url":r"Images\andhra\Temple.jpg"},
            {"name": "Kondapalli Fort", "image_url": r"Images\andhra\KondapalliFor.jpg"},
            {"name": "Ponduru: Famous for Handloom and Silk","image_url": r"Images\andhra\Ponduru.jpg"},
            #{"name": "Ananthagiri Hills", "image_url": "https://example.com/ananthagiri.jpg"}
        ],
        "Best Season to Visit": "October to March (Winter and early Spring)"
    },
    # Add more states here...
}

# Initial message
default_msg = "Click on a state in the map to see the welcome message."

# Layout: Left side map, right side message
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Indian States Map")

    # Create Plotly Choropleth map
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=states,
        z=[1] * len(states),
        featureidkey="properties.NAME_1",
        colorscale="Viridis",
        showscale=False,
        marker_opacity=0.5,
        marker_line_width=0.5
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 22.9734, "lon": 78.6569},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode='event+select'
    )

    # Capture click events using plotly_events
    selected_points = plotly_events(fig)

with col2:
    st.subheader("State Information")
    if selected_points:
        point_index = selected_points[0].get('pointNumber')

        if point_index is not None and 0 <= point_index < len(states):
            clicked_state = states[point_index]
            state_info = india_tourism_info.get(clicked_state)

            if state_info:
                st.markdown(f"## Welcome to {clicked_state}")
                st.markdown(f"**Best Season to Visit:** {state_info['Best Season to Visit']}")
                st.markdown("### Top 10 Must-Visit Places:")
                
                # Display images in a 3x3 grid
                cols = st.columns(3)
                for i, place in enumerate(state_info["Top 10 Must-Visit Places"]):
                    with cols[i % 3]:  # Cycle through columns
                        st.markdown(f"- {place['name']}")
                        st.image(place['image_url'], width=200)  # Display the image for each place
            else:
                st.markdown("### No information available for this state.")
        else:
            st.markdown("### Please click on a valid state.")
    else:
        st.markdown(f"### {default_msg}")
"""