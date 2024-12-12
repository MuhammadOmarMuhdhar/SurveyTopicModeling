import streamlit as st

import streamlit as st

def about_page():
    st.title("About the Project")
    
    st.markdown("""
    Welcome to **Dodora** – a tool designed to streamline the analysis of open-ended survey responses. Dodora was conceived as a solution to the challenge of making sense of large amounts of qualitative data efficiently and effectively. This tool empowers researchers, analysts, and organizations to uncover meaningful insights from unstructured text data using clustering, sentiment analysis, and summarization techniques.
    """)

    st.subheader("Purpose of the Project")
    st.markdown("""
    This project aims to:
    - Help researchers and organizations analyze open-ended survey responses effortlessly.
    - Enable the detection of themes, sentiments, and trends within qualitative data.
    - Bridge the gap between traditional survey analysis and cutting-edge machine learning techniques.
    
    By leveraging machine learning and natural language processing (NLP), Dodora provides a scalable, user-friendly platform for extracting actionable insights from complex datasets.
    """)

    st.subheader("How It Works")
    st.markdown("""
    Dodora combines advanced machine learning methods, like clustering and sentiment analysis, with interactive visualizations to make survey data analysis intuitive. Here's what the tool does:
    1. **Processes Textual Data**: Cleans and prepares the raw text for analysis.
    2. **Clusters Responses**: Groups similar responses based on semantic similarity.
    3. **Summarizes Clusters**: Generates concise, human-readable summaries for each cluster.
    4. **Visualizes Insights**: Provides interactive plots and charts to explore themes and trends.
    
    Whether it's for academic research, product reviews, or organizational feedback, Dodora adapts to your specific survey context.
    """)

    st.subheader("Why This Project?")
    st.markdown("""
    The inspiration for Dodora emerged from real-world challenges in dealing with qualitative data:
    - **Overwhelming Volumes of Text**: Traditional methods struggle with scalability.
    - **Lack of Intuitive Tools**: Existing solutions are often inaccessible to non-technical users.
    - **Time-Consuming Analysis**: Manual coding of responses takes significant time and resources.
    
    Dodora addresses these pain points, making it easier for users to focus on interpretation rather than manual processing.
    """)

    st.subheader("Key Features")
    st.markdown("""
    - **Customizable Topics**: Tailor the analysis to your specific survey type and focus area.
    - **Scalable**: Efficiently handles datasets of various sizes.
    - **Interactive Visualizations**: Explore clusters and summaries visually for better understanding.
    - **User-Friendly Interface**: Designed for both technical and non-technical users.
    """)

    st.subheader("Acknowledgments")
    st.markdown("""
    This project integrates methodologies from computational social science, machine learning, and NLP. Special thanks to the tools and frameworks, including:
    - **Streamlit**: For an intuitive and interactive web-based interface.
    - **Hugging Face**: For NLP model integration.
    - **Plotly**: For advanced visualizations.
    
    Dodora is part of a larger effort to make machine learning accessible and meaningful for diverse applications.
    """)

# Call the function to display the page
if __name__ == "__main__":
    about_page()
