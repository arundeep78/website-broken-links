import streamlit as st
import  utils
import fragments
import time
from humanize import naturaldelta

#set streamlit UI to wide screen mode
st.set_page_config(layout="wide")

st.title("Find Broken links in your website")

# Make sure that muffet is accessible
try:
    utils.set_search_tool_path()

except:
    # st.warning("Search tool is not accessible. Application cannot work without it. Please contact developer or create a github issue.")
    st.error("The search tool is not accessible for some reason. Application cannot work without it. Please contact developer or create a github issue.")


# Input section

col1, col2 = st.columns([70,30],)

with col1:
    test_website_url = st.text_input("Enter the URL",value="https://example.com",
                    help="Enter a url of the website for which you want to find broken links.Only enter the main domain include https://")

with col2:
    # st.subheader('')
    st.text('')
    st.text('')

    submitted= st.button("Submit")
# add paramter configuration in the side bar
with st.sidebar:
  #set paramter variables
  show_success,ignore_verify_tls,rate_limit = fragments.fg_set_parameters()




# hide the button


if submitted:


    if not utils.validate_integer(rate_limit):
        st.error("Rate limit should be an integer value")
        st.stop()
    

    if rate_limit == 0:
        rate_limit = None

# Check if URL is of proper format
    if not utils.is_valid_url(test_website_url):
        st.error("Invalid URL")
        st.stop()

# Check if URL is accessible
    if not utils.is_url_accessible(test_website_url):
        st.error("URL is not accessible. Please check if URL is accessible in the browser")
        st.stop()

    # Process the website
    start = time.perf_counter()   
    results = utils.process_website(test_website_url, show_success, ignore_verify_tls, rate_limit)
    end = time.perf_counter()-start

    # show the time it took to process the website in seconds on minutes
    st.write(f"It took {naturaldelta(int(end))} to process all links on the website")

    # write a text line showing summary of results dataframe
    if len(results) == 0:

        st.header(f"Congratulations! No broken links found on website : {test_website_url}")
    else:

        # create summary variables
        
        internal_links = results[results['link_origin']==utils.LinkOrigin.INTERNAL.value]
        external_links = results[results['link_origin']==utils.LinkOrigin.EXTERNAL.value]

        count_internals_error =  len(internal_links[internal_links['error'].notnull()]) if 'error' in internal_links.columns else 0
        count_externals_error =  len(external_links[external_links['error'].notnull()]) if 'error' in external_links.columns else 0

        count_externals= count_internals =0
        if show_success:
            count_internals = len(internal_links)
            count_externals = len(external_links)

        count_total_error = count_internals_error+count_externals_error
        count_total = count_internals+count_externals


    # calculate unique counts
        count_unique_internals_error =  len(internal_links[internal_links['error'].notnull()].drop_duplicates(subset=['url'])) if 'error' in internal_links.columns else 0
        count_unique_externals_error =  len(external_links[external_links['error'].notnull()].drop_duplicates(subset=['url'])) if 'error' in external_links.columns else 0

        count_unique_externals= count_unique_internals =0
        if show_success:
            count_unique_internals = len(internal_links.drop_duplicates(subset=['url']))
            count_unique_externals = len(external_links.drop_duplicates(subset=['url']))

        count_unique_total_error = count_unique_internals_error+count_unique_externals_error
        count_unique_total = count_unique_internals+count_unique_externals


        # create a streamlit summary row and add details in 2 columns
        st.markdown("---")
        col1, col2 = st.columns([.7,.3])

        with col1:
            st.subheader("Overall broken links:")
            stmt = f"Total links: {count_total_error}{'' if count_total == 0 else '/'+ str(count_total)}"
            stmt += f" | Unique links: {count_unique_total_error}{'' if count_unique_total == 0 else '/'+ str(count_unique_total)}"
            st.write(stmt)
            
            
        with col2:
            # Add a link for the download of whole results dataframe
            st.markdown(utils.get_table_download_link(results), unsafe_allow_html=True,)
     
        if not 'error' in results.columns:
         
            # Display summary statistics of results dataframe
            st.write(results.describe().transpose())

        else:
       
            st.markdown('---')
            col3, col4, col5 = st.columns(3)
            
            with col3:
                
                # Display summary statistics of results dataframe
                st.write('Results summary')
                st.write(results.describe().transpose())            
        
        # Top 3 errors
            with col4:
                    top_n = 3
                    st.write(f"Top {top_n} errors:")
                    st.write(results['error'].value_counts().head(top_n))
        # Top 3 broken links
            with col5:
                st.write(f"Top {top_n} broken urls:")
                st.write(results['url'].value_counts().head(top_n))
                    
        
        
        st.markdown('---')
        # Display results in two columns
        col6, col7 = st.columns(2) 
        
        with col6:

            # st.subheader("Overall broken links:")
            # stmt = f"Total links: {count_total_error}{'' if count_total == 0 else '/'+ str(count_total)}"
            # stmt += f" | Unique links: {count_unique_total_error}{'' if count_unique_total == 0 else '/'+ str(count_unique_total)}"
            # st.write(stmt)
            
            st.subheader("Broken Internal links:")
            stmt = f"Total links: {count_internals_error}{'' if count_internals == 0 else '/'+ str(count_internals)}"
            stmt += f" | Unique links: {count_unique_internals_error}{'' if count_unique_internals == 0 else '/'+ str(count_unique_internals)}"
            st.write(stmt)

            # sub_heading =f"Broken Internal links: {count_internals_error}{'' if count_internals == 0 else '/'+ str(count_internals)}"
            # sub_heading += f" | {count_unique_internals_error}{'' if count_unique_internals == 0 else '/'+ str(count_unique_internals)}"
            # st.subheader(sub_heading)
            st.write(internal_links)
        
        with col7:

            st.subheader("Broken External links:")
            stmt = f"Total links: {count_externals_error}{'' if count_externals == 0 else '/'+ str(count_externals)}"
            stmt += f" | Unique links: {count_unique_externals_error}{'' if count_unique_externals == 0 else '/'+ str(count_unique_externals)}"
            st.write(stmt)
            # sub_heading =f"Broken External links: {count_externals_error}{'' if count_externals == 0 else '/'+ str(count_externals)}"
            # sub_heading += f" | {count_unique_externals_error}{'' if count_unique_externals == 0 else '/'+ str(count_unique_externals)}"
            # st.subheader(sub_heading)
            st.write(external_links)




