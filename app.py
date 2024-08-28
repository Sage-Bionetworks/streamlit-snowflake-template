import numpy as np
import streamlit as st
from toolkit.queries import query_users_trend
from toolkit.utils import get_data_from_snowflake
from toolkit.widgets import ( scatter_plot_yearly_unique_users, 
    bar_plot_yearly_unique_users)

# Configure the layout of the Streamlit app page
st.set_page_config(layout="wide",
                   page_title="My Streamlit App",
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Custom CSS for styling (Optional)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add user interface elements to sidebar
plot_options = ["Dataframe", "Line plot", "Bar plot"]
selected_plot = st.sidebar.selectbox("Choose a plot type", plot_options)

def app(selected_plot):

    # 1. Retrieve the data using your queries in queries.py
    # -------------------------------------------------------------------------
    users_trend_df = get_data_from_snowflake(query_users_trend())

    # 2. Display the data using widgets in widgets.py
    # -------------------------------------------------------------------------

    if selected_plot == "Dataframe":
        st.write("### User Growth Dataframe\nHere we display the cumulative growth of unique users over the years in a straight-forward dataframe. Each row represents the total number of users up to and including that year, allowing you to see how user account creation has increased over time.")
        st.dataframe(users_trend_df,
                     hide_index=True,
                     width=600,
                     column_config={
                        "QUERY_YEAR": st.column_config.TextColumn(
                            "Year",
                        ),
                        "CUMULATIVE_USERS": st.column_config.TextColumn(
                            "Total Users"
                        )
                        }
                    )

    if selected_plot == "Line plot":
        st.write("### Yearly User Growth Trend\nThis line plot illustrates the growth trend of unique users over the years. The dots on the line represent the total number of users up to the end of each year, providing a clear view of how user growth has progressed over time.")
        st.plotly_chart(scatter_plot_yearly_unique_users(users_trend_df))

    if selected_plot == "Bar plot":
        st.write("### Yearly User Growth with Percentage of Total\nThis bar plot shows the cumulative number of unique users up to the end of each year. The overlaid line indicates the percentage of total users achieved by that year, giving you a sense of growth relative to the overall total.")
        st.plotly_chart(bar_plot_yearly_unique_users(users_trend_df))
        

if __name__ == "__main__":
    app(selected_plot)
