import pandas as pd
import numpy as np
import joblib
# import gensim
import os
import sklearn
from sklearn.neighbors import KDTree
# import gensim.models.word2vec as w2v
import streamlit as st
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import streamlit as st

vector = joblib.load("model1.pkl")
kd_model = joblib.load("yumkdtree.pkl")

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield

st.title('Retaurants')



@st.cache
def load_data():
    restaurant_data_updated = pd.read_csv("restaurantdata.csv")
    
    return restaurant_data_updated

data_load_state = st.text('Loading data...')
restaurant_data_updated = load_data()
data_load_state.text("Done! (using st.cache)")

# st.bar_chart(restaurant_data_updated, x = "item_updated", y= "price")

text = st.text_input("Enter the name of Dish: ")
data = vector.wv[text].reshape(1,-1)

distance , idx = kd_model.query(data , k = 10)
dic = {}
for i , value in list(enumerate(idx[0])):
    output = st.empty()
    with st_capture(output.code):
        sleep(0.1)  
        print("restaurant : {}".format(restaurant_data_updated['restaurant'][value]))
        sleep(0.1) 
        print("Distance : {}".format(distance[0][i]))
        sleep(0.1) 
        print("Item :{}".format(restaurant_data_updated['item_updated'][value]))
        sleep(0.1) 
        print("price : {}".format(restaurant_data_updated['price'][value]))
        dic[restaurant_data_updated['restaurant'][value]] =restaurant_data_updated['price'][value]

output = st.empty()
with st_capture(output.code):
    for key, value in dic.items():
        if value == max(dic.values()):
            print("The expensive restaurant for this item is:", key, ",which costs:$",max(dic.values()))
    for key, value in dic.items():
        if value == min(dic.values()):
            print("The cheapest restaurant for this item is ", key, ",which costs:$",min(dic.values()))


# if __name__ == '__main__':
#     distance , idx = kd_model.query(data , k = 10)
#     for i , value in list(enumerate(idx[0])):
#         print("restaurant : {}".format(restaurant_data_updated['restaurant'][value]))
#         print("Distance : {}".format(distance[0][i]))
#         print("Item :{}".format(restaurant_data_updated['item_updated'][value]))
#         print("price : {}".format(restaurant_data_updated['price'][value]))



