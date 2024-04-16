import streamlit as st


input_name = st.text_input("Enter your name:", key="name")

with st.form("test_form"):

    text_input = st.text_input("Enter text:")
    int_input = st.number_input("Enter integer:")
    submitted = st.form_submit_button("Submit")


if submitted:
    st.write(input_name + " " +text_input + str(int_input))
