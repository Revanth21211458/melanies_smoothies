# Import python packages
import streamlit as st
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(""" Choose The Fruits You Want In Your Custom Smoothie!!! """ )

name_on_order = st.text_input("Name On Smoothie")
st.write("The Name On The Smoothie Will Be - ", name_on_order)

# Select Box For Selecting Fruits
#option = st.selectbox("What Is Your Favourite Fruits?", 
 #    ("Banana", "Apple", "Water Melon", "Musk Melon"),)
#st.write("Your Option is ", option)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Convert the snowpark Dataframe to a Pandas Dataframe so we can use the LOC Function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredients_list = st.multiselect('Choose Up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
        result = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON']
        if result.empty or pd.isna(result,iloc[0]):
         st.error(f"No SEARCH_ON value found for {fruit_chosen}")
        else:
         search_on = str(result.iloc[0])  # make sure it's a string
        #search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
            
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
        
        
        
        
        
        
        
        
        
