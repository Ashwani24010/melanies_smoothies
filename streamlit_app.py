# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests 

# Write directly to the app
st.title(f"Customize Your Smoothie :balloon:")
st.write(
  """Choose the fruits you want in your custome Smoothie!
  """
)

name_of_order = st.text_input("Name of your Smoothie:")
st.write("The name of your Smoothie will be: ", name_of_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredient_string = ''
    for fruits_chosen in ingredients_list:
        ingredient_string += fruits_chosen + ' '
        smoothiefruit_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
        sf_df = st.dataframe(data=smoothiefruit_response.json(),use_container_width=True)
    st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredient_string + """','"""+name_of_order+"""')"""
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie ordered is """+name_of_order+""" !""", icon="✅")
      
