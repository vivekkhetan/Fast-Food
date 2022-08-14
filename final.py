import pandas as pd
import streamlit as st
import random as rd
import matplotlib.pyplot as plt
import pydeck as pdk

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
                          'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                          'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                          'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
global df
def read_data():
    global df
    df = pd.read_csv('fast_food.csv')
    df.drop_duplicates(inplace=True)
    return df

read_data()
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@900&display=swap');

    html, body, [class*="css"]  {{
    font-family: 'Lato', sans-serif;
    }}
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('9f145ca71b9814fab19af66fc0e85485.jpeg')
def homepage():
    # Gives a general introduction to the fast food industry in America
    st.header("Fast Food in the United States")
    st.text("")
    st.text("")
    st.text("")
    st.subheader('What is the Fast Food Industry')
    st.text("")
    st.text("")
    st.write('The Fast Food industry consist and accounts for prepared food usually from a restaurant, store, food truck, '
             'or street vendor, served quickly and affordably to consumers in a take-out, disposable container. Most fast food '
             'companies work with low preparation time and preheated or precooked ingredients to reduce transaction time and cost '
             'for each purchase. '
             '\n\n'
             'The Fast Food Market started in the 1920s and has been rapidly growing and evolving with '
             'big name fast food chains such as McDonald\'s, Taco Bell, Wendy’s, Burger King, KFC, Jack in the Box, White '
             'Castle, etc. In recent years, more health conscious fast food companies such as Chipotle, Pita Pit, and '
             'BurgerFi emerged offering meals that include ingredients with less pesticides, are hormone and antibiotic-free,'
             ' and served in biodegradable or recyclable take-out containers.')
    st.text("")
    st.text("")
    st.subheader('Facts about the Fast Food Industry in the United States')
    st.text("")
    st.text("")
    st.write('The US fast food industry market size is \$296.6 billion as of 2021.'
             '\n'
             'Globally, the fast food industry generated \$797.7 billion in revenue over 2021.')
    st.text("")
    st.text("")
    st.write('According to data from the Centers for Disease Control, about a third of American adults eat fast food on any given day. '
             'That’s over 84 million people who reported that they had eaten fast food in the past 24 hours.')
    st.text("")
    st.text("")
    st.write('The fast food industry employed 3,450,120 people as of May 2020. Most of those workers live in '
             'California and Texas — that’s 384,890 and 380,090 fast food workers, respectively. ')
    st.text("")
    st.text("")
    st.write('Most Americans eat fast food 1-3 times a week.'
             '\n\n'
             '83% of American families eat at fast food restaurants at least once a week.'
             '\n\n'
             'The average American household spends 10% of their annual income on fast food.')
    st.text("")
    st.text("")
    st.subheader('Top 10 Fast Food Chains in America')
    d = df.groupby('name').count().reset_index().sort_values(by='id', ascending=False).head(10).reset_index()
    s = ""
    for i in range(10):
        st.write(str(i+1)+'. '+d.at[i, 'name'] + '\n')


def select():
    st.subheader("Select your State")
    state = st.selectbox('Select State: ',
                 states)
    st.subheader('Enter your Zipcode: ')
    zipcode = st.text_input('Enter your Zipcode: ')
    return state, zipcode

def _map():
    st.header('Fast Food Restaurants across the United States')
    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom = 8,
        pitch = 40)
    layer1 = pdk.Layer('ScatterplotLayer',
                  data = df,
                  get_position = '[longitude, latitude]',
                  get_radius = 2000,
                  get_color = [0,0,255],
                  pickable = True)
    tool_tip = {"html": "Restaurant Name:<br/> <b>{name}</b> <br/>"
                        "Address: <br/> <b> {address}",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}}
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip= tool_tip
        )

    st.pydeck_chart(map)
    st.text("")
    st.text("")
    st.text("")
    st.write('This program maps out all the fast food restaurants throughout the United States and provides the name and address'
             'of the restaurant.')
def selection():
    s = st.radio('Do you want to view by state or zipcode?', ('State', 'Zipcode'))
    return s

def rand_map(state, zipcode, s):
    st.header('Random Restaurant Generator')
    if s == "State":
        restaurant = df[df['province'] == state]
    else:
        restaurant = df[df['postalCode'] == zipcode]
    rand_rest = rd.choice(restaurant.index.tolist())
    name = restaurant['name'][rand_rest]
    _add = restaurant['address'][rand_rest]
    lat = restaurant['latitude'][rand_rest]
    lon = restaurant['longitude'][rand_rest]
    data = [[name, lon, lat]]
    data = pd.DataFrame(data, columns=['name', 'long', 'lati'])
    print(data)
    view_state1 = pdk.ViewState(
        latitude=data['lati'].mean(),
        longitude=data['long'].mean(),
        zoom = 13,
        pitch = 40)
    layer2 = pdk.Layer('ScatterplotLayer',
                  data = data,
                  get_position = '[long, lati]',
                  get_radius = 500,
                  get_color = [0,0,255],
                  pickable = True)
    tool_tip1 = {"html": f"Restaurant Name:<br/> <b>{name}</b> <br/>"
                        f"Address: <br/> <b> {_add}",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}}
    map1 = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state1,
        layers=[layer2],
        tooltip= tool_tip1
        )

    st.pydeck_chart(map1)
    st.text("")
    st.text("")
    st.text("")
    st.write('This program asks the user to input their state and their zipcode to generate and map a random fast food restaurant'
             'by either state or zipcode.')

def map_state(state, zipcode, s):
    st.header('Restaurants in State or Zipcode')
    if s == 'State':
        restaurant = df[df['province'] == state]
    else:
        restaurant = df[df['postalCode'] == zipcode]
    view_state = pdk.ViewState(
        latitude=restaurant['latitude'].mean(),
        longitude=restaurant['longitude'].mean(),
        zoom = 13,
        pitch = 40)
    layer1 = pdk.Layer('ScatterplotLayer',
                  data = restaurant,
                  get_position = '[longitude, latitude]',
                  get_radius = 100,
                  get_color = [0,0,255],
                  pickable = True)
    tool_tip = {"html": "Restaurant Name:<br/> <b>{name}</b> <br/>"
                        "Address: <br/> <b> {address}",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}}
    map1 = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip= tool_tip
        )

    st.pydeck_chart(map1)
    st.text("")
    st.text("")
    st.text("")
    st.write('This program asks the user to input their state and zipcode then asks them if they want to view the results by'
             'state or zipcode. After that it maps all the fast food restaurants either by state or zipcode and displays the'
             'name of the restaurant and the address.')

def stateCountBar():
    st.header('Restaurant Frequency Bar')
    sel = st.selectbox('Select you state',
                              states)
    restaurant = df.query('province == @sel')
    fig, ax = plt.subplots(figsize=(15,10))
    rest_freq = restaurant['name'].value_counts().reset_index()
    rest_freq.rename(columns={"index": "Name", "name":"Count"}, inplace=True)

    ax.bar(rest_freq.head(20)['Name'], rest_freq.head(20)['Count'])
    plt.xticks(rotation=90)
    st.pyplot(fig)
    st.text("")
    st.text("")
    st.text("")
    st.write('This program asks the user to input a state and displays a bar graph illustrating the frequency '
             'of different fast food restaurants in the state.')

def stateCountPie():
    st.header("Restaurant Pie Chart")
    sel = st.selectbox('Select you state',
                              states)
    restaurant = df.query('province == @sel')
    rest_freq = restaurant['name'].value_counts().reset_index()
    rest_freq.rename(columns={"index": "Name", "name":"Count"}, inplace=True)
    fig, axs = plt.subplots(figsize=(10,20))
    axs.pie(rest_freq.head(10)['Count'],
            labels=rest_freq.head(10)['Name'], autopct='%1.1f%%')
    axs.legend()
    st.pyplot(fig)
    st.text("")
    st.text("")
    st.text("")
    st.write('This program asks the user to input a state and displays a pie illustrating the distribution '
             'of different fast food restaurants in the state.')

def restFreq():
    st.header('Restaurant Frequency by State')
    try:
        n = st.text_input('Enter restaurant name: ').upper()
        r = df[df['name'] == n]
        if r.shape[0] >0:
            c = r.groupby('province').count()['id'].reset_index()
            c.rename(columns={"province":"State", "id":"Count"}, inplace=True)
            c.sort_values(by='Count', ascending=False, inplace=True)
            fig, ax = plt.subplots(figsize=(20,20))
            ax.bar(c['State'], c['Count'], alpha=0.5)
            ax.plot(c['State'], c['Count'], color='r')
            ax.scatter(c['State'], c['Count'], color='black')
            st.pyplot(fig)
        else:
            st.write('Invalid Restaurant')
    except:
        st.write('Invalid restaurant')
    st.text("")
    st.text("")
    st.text("")
    st.write('This program asks users to input a restaurant name and then displays a bar and line graph'
             ' displaying the total count of the selected restaurant in each state.')

def main():
    st.sidebar.title('Navigation')
    section = st.sidebar.radio('Pages:', ['Homepage', 'US Map', 'Random Restaurant', 'Restaurant by State or Zipcode',
                                          "Frequency Bar", 'Pie Chart', 'Restaurant Frequency'])
    if section == 'Homepage':
        homepage()
    if section == 'US Map':
        _map()
    if section == 'Random Restaurant':
        state, zipcode = select()
        s = selection()
        rand_map(state, zipcode, s)
    if section == 'Restaurant by State or Zipcode':
        state, zipcode = select()
        s = selection()
        map_state(state, zipcode, s)
    if section == "Frequency Bar":
        stateCountBar()
    if section == "Pie Chart":
        stateCountPie()
    if section == 'Restaurant Frequency':
        restFreq()
main()
