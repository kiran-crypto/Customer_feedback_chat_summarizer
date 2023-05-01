import pandas as pd
import streamlit as st
import altair as alt

st.title("Sales Analysis")

# Define some CSS styles
css = """
h1 {
    font-size: 50px;
    font-weight: bold;
    color: #FF5733;
    text-align: center;
    margin-top: 50px;
}

.selectbox {
    font-size: 30px;
    color: #333333;
    text-align: center;
    margin-top: 30px;
}

.button {
    font-size: 30px;
    color: #FFFFFF;
    background-color: #FF5733;
    border-radius: 10px;
    text-align: center;
    margin-top: 50px;
    padding: 10px 30px;
    transition: all 0.5s;
}

.button:hover {
    background-color: #FFFFFF;
    color: #FF5733;
    border: 2px solid #FF5733;
}
"""

# Apply the CSS styles to the page
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load the data
input_df = pd.read_csv('bnbdata.csv')

# Define the available products and ages
products = sorted(input_df['Product'].unique().tolist())
ages = sorted(input_df['Age'].unique().tolist())

# Define the input selectors
selected_product = st.selectbox("Select a product", products, key='product_selector', help="Choose a product to analyze.", format_func=lambda x: f"Product: {x}", index=0)
selected_age = st.selectbox("Select an age", ages, key='age_selector', help="Choose an age group to analyze.", format_func=lambda x: f"Age: {x}", index=0)
selected_gender = st.radio("Select a gender", ['All', 'Male', 'Female'], key='gender_selector', help="Choose a gender to analyze.", format_func=lambda x: f"Gender: {x}")

# Filter the data based on the selected filters
if selected_gender == 'All':
    filtered_df = input_df[(input_df['Product'] == selected_product) & (input_df['Age'] == selected_age)]
else:
    filtered_df = input_df[(input_df['Product'] == selected_product) & (input_df['Age'] == selected_age) & (input_df['Gender'] == selected_gender)]

# Remove duplicates from the filtered data
filtered_df = filtered_df.drop_duplicates()

# Show the details of the selected filters
if st.button("Show Details", key='show_details_button', help="Click to show the details of your selection."):
    st.write("Data for product:", selected_product, ", age:", selected_age, ", and gender:", selected_gender)

    # Add a JavaScript transition to the details section
    js = """
    <script>
        var details = document.getElementById("details");
        details.style.opacity = 0;
        setTimeout(function() {
            details.style.transition = "opacity 0.5s";
            details.style.opacity = 1;
        }, 100);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

    # Add the details section
    st.markdown('<div id="details">', unsafe_allow_html=True)
    st.write(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)

# Calculate the total revenue and units sold for the selected filters
total_revenue = filtered_df['Revenue'].sum()
total_units_sold = filtered_df['Units Sold'].sum()


