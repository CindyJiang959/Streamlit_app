import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("New Healthy Dinner")

streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boilded Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#pandas lib
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
#fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.Fruit), ['Avocado', 'Strawberries'])
fruit_to_show = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(fruit_to_show)
#streamlit.dataframe(my_fruit_list)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


streamlit.stop()

#snowflake.connector lib

def get_fruit_load_list():
  with my_cnx.cursor() as my_cnr:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_list()
  streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
