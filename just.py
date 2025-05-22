import streamlit as st
import plotly.graph_objects as go
import json
from streamlit_plotly_events import plotly_events
from PIL import Image
from streamlit_image_zoom import image_zoom  # Importing the image zoom functionality

# Set page configuration
st.set_page_config(layout="wide", page_title="Indian States Welcome App")

st.title("Indian States Welcome App")

# Function to load the GeoJSON for Indian states
@st.cache_data
def load_geojson():
    with open("india_states.geojson") as response:
        geojson = json.load(response)
    return geojson

geojson = load_geojson()

# List of Indian states
states = [feature['properties']['NAME_1'] for feature in geojson['features']]

# Define tourism information for each state
india_tourism_info = {
    "Andhra Pradesh": {
        "Top 10 Must-Visit Places": [
            {"name": "Tirumala Tirupati Devasthanams (Tirupati)", "image_url": r"Images\andhra\Tirupathi.jpg"},
            {"name": "Araku Valley", "image_url": r"Images\andhra\ArakuValley.jpg"},
            {"name": "Borra Caves", "image_url": r"Images\andhra\Borra-Cave.jpg"},
            {"name": "Visakhapatnam (Vizag): R.K. Beach, Kailasagiri", "image_url": r"Images\andhra\Visakhapatnam.jpg"},
            {"name": "Chilika Lake", "image_url": r"Images\andhra\Chilika-Lake.png"},
            {"name": "Sri Kalahasti Temple", "image_url": r"Images\andhra\kalahasteeswaraSwami.jpg"},
            {"name": "Nellore: Penchalakona", "image_url": r"Images\andhra\Temple.jpg"},
            {"name": "Kondapalli Fort", "image_url": r"Images\andhra\KondapalliFor.jpg"},
            {"name": "Ponduru: Famous for Handloom and Silk", "image_url": r"Images\andhra\Ponduru.jpg"},
        ],
        "Best Season to Visit": "October to March (Winter and early Spring)"
    },
    # Add more states here...
}

# Initial message
default_msg = "Click on a state in the map to see the welcome message."

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

# Set map boundaries to focus on India
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=4,
    mapbox_center={"lat": 22.9734, "lon": 78.6569},
    mapbox_bounds={"west": 68.7, "south": 8.1, "east": 97.4, "north": 37.1},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    clickmode='event+select'
)

# Display the map
# st.plotly_chart(fig, use_container_width=True)

# State Information Section
st.subheader("State Information")
st.markdown("### Click on a state in the map to see the welcome message.")

# Capture click events using plotly_events
selected_points = plotly_events(fig, key="indian_states_map")

if selected_points:
    point_index = selected_points[0].get('pointNumber')

    if point_index is not None and 0 <= point_index < len(states):
        clicked_state = states[point_index]
        state_info = india_tourism_info.get(clicked_state)

        if state_info:
            st.markdown(f"## Welcome to {clicked_state}")
            st.markdown(f"**Best Season to Visit:** {state_info['Best Season to Visit']}")
            st.markdown("### Top 10 Must-Visit Places:")

            # Unique key for each image
            def get_image_key(state, idx):
                return f"{state}_img_{idx}"

            # Display images with toggle for viewing mode
            places = state_info["Top 10 Must-Visit Places"]
            num_cols = 3  # For a 3x3 grid

            for row_idx in range(0, len(places), num_cols):
                cols = st.columns(num_cols)
                for col_idx in range(num_cols):
                    place_idx = row_idx + col_idx
                    if place_idx < len(places):
                        place = places[place_idx]
                        with cols[col_idx]:
                            st.markdown(f"**{place['name']}**")
                            # Use image_zoom for interactive zoom effect
                            #image_zoom(place['image_url'], set_full_width=True)

        else:
            st.markdown("### No information available for this state.")
    else:
        st.markdown("### Please click on a valid state.")
else:
    st.markdown(f"### {default_msg}")

# Add some spacing below the map and information
st.markdown("<br>", unsafe_allow_html=True)
