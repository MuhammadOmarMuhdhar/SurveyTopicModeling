import streamlit as st

def documentation():
    st.title("Documentation")

    st.subheader("Introduction")
    st.markdown("""
                This tool is designed to simplify the analysis of open-ended survey responses. By integrating machine learning and 
                natural language processing (NLP), it uncovers trends, sentiments, and patterns from qualitative data at a *topic* level, enabling deeper insights and actionable outcomes for researchers and organizations.
    """)

    st.markdown("""
                The tool bridges the gap between traditional manual survey analysis and modern machine learning techniques, offering a scalable, 
                intuitive platform for extracting insights from even the most complex datasets. Whether you’re working with customer feedback, 
                employee engagement surveys, or academic research, Dodora adapts to your needs and delivers results efficiently.
    """)


    st.subheader("Workflow")
    st.markdown("""

    1. **Upload Your Data**:
       - Upload a CSV file containing survey responses.
       - Ensure the file includes a column with textual responses and optional demographic data.

    2. **Configure Settings**:
       - Select the column with responses.
       - Optionally, specify demographic columns for group-level insights.

    3. **Process Data**:
       - Click on "Process Data" to start clustering and summarization.
       - Wait for the tool to process responses using HDBSCAN and Transformer models.

    4. **View Results**:
       - Explore clusters and summaries in the interactive visualization.
       - Use the provided insights for research, decision-making, or reporting.
    
    """)

    st.subheader("Core Technologies")
    st.markdown("""
 
    
    - **Hugging Face Transformers**:
      - Used for generating sentence embeddings and summarization.
      - Models like `distilbert` or `sentence-transformers` capture the semantic meaning of responses.

    - **HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise)**:
      - Groups similar responses into clusters based on their embeddings.
      - Handles noise (outliers) effectively, ensuring robust clustering.

    - **Gemini Embeddings**:
      - Converts textual data into high-dimensional vectors for clustering.

    - **Plotly**:
      - Provides interactive scatter plots for visual exploration of clusters.
      - Visualizes cluster sizes, polarity-based coloring, and textual summaries.

    - **Sentiment Analysis**:
      - Analyzes the sentiment of responses (positive, negative, neutral) for each cluster.

    - **Streamlit**:
      - Powers the interactive web application, providing an intuitive user interface.
    """)

    st.subheader("Troubleshooting")
    st.markdown("""
    - **File Upload Issues**:
       - Ensure the uploaded file is in CSV format with valid column names.
    - **Processing Delays**:
       - Large datasets may take longer to process. Try using a smaller subset of the data.
    - **Visualization Not Displaying**:
       - Check your browser's console for errors and ensure Plotly is properly installed.
    """)

    st.subheader("Acknowledgments")
    st.markdown("""
    This project leverages powerful open-source technologies to deliver its functionality:
    - **Streamlit** for the interactive user interface.
    - **Hugging Face Transformers** for embeddings and summarization.
    - **HDBSCAN** for clustering survey responses.
    - **Plotly** for creating interactive visualizations.

    A special thanks to the contributors and researchers whose tools and models have made this project possible.
    """)

# Call the function to display the documentation page
if __name__ == "__main__":
    documentation()
