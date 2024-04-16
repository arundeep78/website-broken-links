import streamlit as st



@st.experimental_fragment
def fg_set_parameters():
    st.header("Configure parameters:")
    show_success = st.checkbox("Show successful results as well",help="By default application only reports broken links. Select the checkbox, if you want result on successful links as well")
    ignore_verify_tls = st.checkbox("Ignore TLS certificate verification",help="By default application check for TLS certificate verification as well. Select this box to skip the verification.")
    rate_limit = st.number_input("Rate limit",help="Maximum requests made to website in a second. Enter an integer value.",format="%d" ,value =20,  )
    # rate_limit = st.text_input("Rate limit",help="Maximum requests made to website in a second. Enter an integer value.",value =20,max_chars=2)
    return show_success,ignore_verify_tls,rate_limit


# Streamlit UI