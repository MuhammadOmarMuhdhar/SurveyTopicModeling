import streamlit as st

def home_page():

    # st.sidebar.markdown("## About Me")
    
    # # Add an optional profile image (local or online)
    # st.sidebar.image("head-shot.jpg", use_container_width=False, width=200)
    # st.sidebar.markdown("")


    # About Me Content
    st.sidebar.markdown("""                     
    This prototype represents my first attempt in exploring how machine learning and NLP can be used to address the challenge of analyzing qualitative
                        survey data at scale. 

    I'd love to hear your thoughts and suggestions to improve this tool!  
                        

    Let’s connect:  
    - [LinkedIn](https://www.linkedin.com/in/muhammad-omar-muhdhar/)  
    - [Email Me](muhammad_muhdhar@berkeley.edu)
    """)

    # Set page title
    st.title("Survey Topic Modeling Tool")

    # Introduction Section
    st.markdown("""
    **This prototype tool is designed to transform open-ended survey responses into clear quantitative insights.**

    By leveraging natural language processing, unsupervised machine learning algorithms, and advanced large language models, this tool 
    enables the large-scale analysis of qualitative data. It organizes unstructured survey responses into coherent and semantically meaningful clusters, 
    providing concise summaries and insights that uncover key themes and highlight underlying patterns in responses.

    The goal is to bridge the gap between traditional manual analysis of open-ended surveys and modern machine learning techniques, 
    offering an intuitive platform for extracting objective insights from complex qualitative data.
""")
    

    # Use Cases Section
    st.subheader("Use Cases")
    st.markdown("""
    - **Academic Research**: Extract meaningful insights from large-scale qualitative datasets for social science, education, or behavioral studies.
    - **Employee Engagement**: Analyze workforce sentiment, uncover recurring themes, and measure feedback on workplace initiatives.
    - **Education Feedback**: Review student or parent feedback on courses or programs to improve curriculum and teaching strategies.
    - **Customer Feedback**: Identify key themes, pain points, and sentiments from customer reviews, surveys, or support tickets.
                
    """)

    # Navigation Instructions
    st.subheader("How to Get Started")
    st.markdown("""
    1. Navigate to the **Workspace** page to upload your survey data.
    2. Select the column containing survey responses and configure optional demographic settings.
    3. Process the data to view clusters, summaries, and sentiment analysis.
    4. Explore insights through interactive visualizations on the results page.
    """)
    

# Run the function if the file is executed directly
if __name__ == "__main__":
    home_page()
