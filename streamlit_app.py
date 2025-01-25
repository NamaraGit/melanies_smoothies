# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(" :cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the friut you want in your custom Smoothie.
    """
)

# option = st.selectbox(
#     "What is your favorite food?",
#     ("Banana", "Strawberries", "Peaches"),
# )
# st.write("Your favorite fruit food is:", option)

name_on_order=st.text_input("Name on Smoothie:")
st.write("Name on yout smoothie will be: " , name_on_order)

#session = get_active_session()
cnx=st.connection("snowflake");
session=cnx.session();

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# OR

ingredients_list=st.multiselect("Choose upto 5 ingredients",my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string=''

    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '
        # st.write(ingredients_string)
        
        # st.text(smoothiefroot_response.json())
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruits_chosen)
        st_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

    # st.write(my_insert_stmt)

    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered, '+ name_on_order +'!' , icon="✅")


