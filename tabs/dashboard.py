import streamlit as st
from data_loader import fetch_data
import plotly.express as px

#  Function to display the Dashboard page
def display_dashboard():
    listing = fetch_data("listing")

    # List unique property types and put in a multiselect box
    property_types = listing['PROPERTY_TYPE'].unique()
    prop = st.multiselect('Property types:', property_types)

    # Creates the filter logic
    if prop: 
        filtered_listing = listing[(listing['PROPERTY_TYPE'].isin(prop))]
    else: 
        filtered_listing = listing.copy()  # Show all listings if no filters applied
    
    # Calculate KPIs for filtered data
    avg_price = filtered_listing['PRICE'].mean()
    min_price = filtered_listing['PRICE'].min()
    max_price = filtered_listing['PRICE'].max()
    total_listings = len(filtered_listing)
    avg_review_score = filtered_listing['REVIEW_SCORES_RATING'].mean()
    avg_review_score_acc = filtered_listing['REVIEW_SCORES_ACCURACY'].mean()
    total_reviews = filtered_listing['NUMBER_OF_REVIEWS'].sum()
    bookable = filtered_listing['INSTANT_BOOKABLE'].sum() 
    ## Calculate bookable rate for filtered data
    if total_listings > 0:
        bookable_rate = round((filtered_listing['INSTANT_BOOKABLE'].sum() / total_listings), 2) * 100
    else:
        bookable_rate = 0.0  # Handle division by zero if no listings match the filter

    # Create columns for KPIs (first layer)
    price_col, book_col, rate_col = st.columns(3)

    with price_col:
        price_col.markdown(f"""
        <div style='text-align: center;'>
            <h2 style='margin-bottom: 5px; font-size: 25px;'>AVERAGE PRICE</h2>
            <p style='font-size: 50px; margin: 0; color: {'#2945E8'};'><b>${avg_price:.2f}</b></p>
            <p style='font-size: 18px; margin: 0;'>Minimum Price: ${min_price}</p>
            <p style='font-size: 18px; margin: 0;'>Maximum Price: ${max_price}</p>
            <p style='margin-top: 10px; font-size: 14px;'><em>Out of <b>{total_listings:,}</b> total number of listings.</em></p>
        </div>
    """,unsafe_allow_html=True)


    with book_col:
        book_col.markdown(f"""
        <div style='text-align: center;'>
            <h2 style='margin-bottom: 5px; font-size: 25px;'>BOOKABLE LISTINGS</h2>
            <p style='font-size: 50px; margin: 0;color: {'#2945E8'};'><b>{bookable_rate:.0f}%</b></p>
            <p style='margin-top: 10px; font-size: 14px;'><em><b>{bookable:.0f}</b> listings out of <b>{total_listings}</b> may be booked right away.</em></p>
            
        </div>
    """, unsafe_allow_html=True)

    with rate_col:
         # Determine color based on average review score
        if avg_review_score >= 4.0:
            rating_color = "green"
        elif avg_review_score >= 3.0:
            rating_color = "orange"
        else:
            rating_color = "red"

        rate_col.markdown(f"""
            <div style='text-align: center;'>
                <h2 style='margin-bottom: 5px; font-size: 25px;'>AVERAGE REVIEW SCORES</h2>
                <p style='font-size: 50px; margin: 0; color: {rating_color};'><b>{avg_review_score:.2f}</b></p>
                <p style='margin-top: 10px; font-size: 14px;'><em>Average review accuracy of <b>{avg_review_score_acc:.2f}</b>.</em></p>
                <p style='margin-top: 10px; font-size: 14px;'><em>Out of <b>{total_reviews:,}</b> total number of reviews.</em></p>
            </div>
        """, unsafe_allow_html=True)
    st.write("---")

    # Create columns for dynamic figures (second layer)
    scat_col, bar_col = st.columns((3,2))

    # Column that displays a dynamic scatter plot

    with scat_col:
        st.markdown("""<div style='text-align: center;'>
            <h2 style='margin-top: 0; margin-bottom: 0; font-size: 20px;'><b>SCATTER PLOT GENERATOR</b></h2>
        </div>
    """, unsafe_allow_html=True)
        
        # Creates a list numerical field for the select box
        column_list =  ["Price","Rating Score", "Accuracy Score", "Cleanliness Score", "Check-in Score", "Communication Score", "Location Score", "Value Score","Number of Bathroom(s)",
                                "Number of Bedroom(s)", "Accommodation Size"]
        # Creates a dictionary of string names and numerical column names
        column_mapping = {
                    "Price": "PRICE",
                    "Rating Score": "REVIEW_SCORES_RATING",
                    "Accuracy Score": "REVIEW_SCORES_ACCURACY",
                    "Cleanliness Score": "REVIEW_SCORES_CLEANLINESS",
                    "Check-in Score": "REVIEW_SCORES_CHECKIN",
                    "Communication Score": "REVIEW_SCORES_COMMUNICATION",
                    "Location Score": "REVIEW_SCORES_LOCATION",
                    "Value Score": "REVIEW_SCORES_VALUE",
                    "Number of Bathroom(s)": "BATHROOMS",
                    "Number of Bedroom(s)": "BEDROOMS",
                    "Accommodation Size": "ACCOMMODATES"
        }
        
        # Creates a select box for the x axis of scatter plot
        xcolumn_select = st.selectbox(
        "Select the first numerical field:",
        column_list,
        index=0
        )   
        x_column = column_mapping[xcolumn_select]

        # Creates a select box for the y axis of scatter plot
        ycolumn_select = st.selectbox(
        "Select the second numerical field:",
        column_list,
        index=1
        )   
        y_column = column_mapping[ycolumn_select]
        
        # Creates the scatter plot
        fig2 = px.scatter(listing,
                        x=x_column,
                        y=y_column,
                        labels={y_column: ycolumn_select, x_column: xcolumn_select},
                        size_max=5  
                )
        
        fig2.update_traces(marker_color='#2945E8')
        fig2.update_layout(
            title_text="",
            title_x=0.5,
            margin=dict(l=10, r=10, b=10, t=0), 
            xaxis_title = xcolumn_select,
            yaxis_title = ycolumn_select
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Column that displays the dynamic bar graph
    with bar_col:
        st.markdown("""<div style='text-align: center;'>
            <h2 style='margin-top: 0; margin-bottom: 0; font-size: 20px;'><b>LISTING DISTRIBUTION</b></h2>
        </div>
        """, unsafe_allow_html=True)


        # # Creates a list categorical field for the select box
        dim_list =  ["Property type", "Room type", "Host response time"]
        # Creates a dictionary of string names and numerical column names
        dim_mapping = {
            "Property type": "PROPERTY_TYPE",
            "Room type": "ROOM_TYPE",
            "Host response time": "HOST_RESPONSE_TIME"
        }

        # Creates a select box for the bar graph field
        dim_select = st.selectbox(
            "Select a categorical field:",
        dim_list,
        index=0
        )  
        dim = dim_mapping[dim_select]

        # Sorts the categorical field based on count
        data_sorted = listing[dim].value_counts().reset_index()
        data_sorted.columns = [dim, 'Count']
        data_sorted = data_sorted.sort_values(by = 'Count', ascending = True)

        # Creates the bar chart
        fig = px.bar(data_sorted, 
                    x='Count', 
                    y=dim, 
                    labels={'Count': 'Count', dim: dim_select},
                    color_discrete_sequence=['#2945E8']) 

        fig.update_layout(
            title_text="",
            title_x=1,
            margin=dict(l=10, r=10, b=10, t=0),
            xaxis_title='Number of Property Listings',
            yaxis_title=None,
            xaxis_tickangle=0,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")

