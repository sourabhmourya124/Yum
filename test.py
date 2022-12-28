import streamlit as st

your_name = st.text_input("Enter your name")
st.title(your_name)

print(your_name)