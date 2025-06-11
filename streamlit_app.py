# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie")


#LAB 4 : Add an order name and assign it to a variable
st.subheader(":exclamation: LAB 4 - Add name of order")

# add a text box
var_name_of_order = st.text_input('Name of Order:')
st.write('The name of your order will be:', var_name_of_order)

# LAB 2: create multiselect and show selection
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'))

st.subheader(":exclamation: LAB 2 - Multiselect")

ingredients_list = st.multiselect ('Choose up to 5 ingredients:', my_dataframe, max_selections =5)

if ingredients_list:
    #show the list
    st.write(ingredients_list)
    st.text(ingredients_list)
    
    ingredients_string=''   

    for var_fruit_chosen in ingredients_list:
        ingredients_string +=   var_fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + var_fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    # create a sql statement with python
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + var_name_of_order + """')"""

    #show the sql statement
    #st.write(my_insert_stmt)

    #run the code up to here
    #st.stop()

    #Now we add a button
    time_to_insert = st.button('Submit Order')

    #catch the click of the button and execute the sql 
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success("Your Smoothie is ordered, " + var_name_of_order)




