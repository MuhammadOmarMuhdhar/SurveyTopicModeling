import streamlit as st

def documentation():


    st.sidebar.markdown("")
    st.sidebar.markdown("")

    # Separator for clarity
    st.sidebar.markdown("### Share Your Feedback")

    # Feedback Form Fields
    name = st.sidebar.text_input("Your Name", key="name_input")
    email = st.sidebar.text_input("Your Email", key="email_input")
    message = st.sidebar.text_area("Your Feedback or Suggestions", key="message_input")

    # Submit Button
    if st.sidebar.button("Submit Feedback", key="submit_feedback_button"):
        if name and email and message:
            # Save feedback to a text file
            with open("feedback.txt", "a") as file:
                file.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n{'-'*40}\n")

            st.sidebar.success("Thank you for your feedback! Your message has been saved.")
        else:
            st.sidebar.error("Please fill in all fields before submitting.")


    st.title("Documentation")

    st.markdown("""

    This page provides a quick guide to using this prototype to analyze open-ended survey responses. Here, you'll find explanations of the 
    tool's functionality, the technologies powering it, and step-by-step instructions for each stage of the workflow.
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
    with st.expander("Sentence-Transformers for Embedding Generation"):
        st.markdown("""
                    Embeddings are a way to represent textual data numerically, enabling machines to understand and process semantic meaning and similarity. They convert words, sentences, and paragraphs into high-dimensional vectors, which capture their contextual relationships. For example, the embeddings for "king" and "queen" reflect their semantic similarity in the context of ruling, while distinguishing their differences in terms of gender. 
                    
                    This project uses [Sentence-Transformers](https://huggingface.co/sentence-transformers), a pre-trained model from Hugging Face, to generate these embeddings. A key feature of this model is its ability to understand context, enabling it to differentiate between homonyms or polysemous words. For instance, "Apple" as a fruit and "Apple" as a company are recognized as having distinct meanings, depending on their usage in a sentence.

                    Additionally, Sentence-Transformers can generate embeddings for entire sentences or paragraphs rather than just individual words. For instance, it can determine the similarity between two sentences like “The car is fast” and “The vehicle is speedy” while accounting for their contextual alignment. This capability makes it particularly useful for creating embeddings to be used for clustering textual data.
        """)

    with st.expander("HDBSCAN for Clustering"):
        st.markdown("""
            To group similar responses, the tool employs `HDBSCAN` (Hierarchical Density-Based Spatial Clustering of Applications with Noise). This unsupervised learning method is well-suited for
            analyzing textual data as it dynamically adjusts cluster thresholds, allowing for flexible and accurate grouping of embedded responses.
        """)

    with st.expander("Gemini for Summarization"):
        st.markdown("""
            Once clusters are formed, Google's large language model (LLM) `Gemini` is used to generate concise, contextual summaries of each cluster. LLMs excel at capturing the key themes and nuances of the 
            clustered responses, providing insights into the patterns within responses at the topic cluster level.
        """)


    st.subheader("Troubleshooting")
    st.markdown("""
    - **File Upload Issues**:
       - Ensure the uploaded file is in CSV format with valid column names.
    - **Processing Delays**:
       - This tool uses the free version of Gemini, datasets may take longer to process due to API rate limits. Try using a smaller subset of the data.
    - **Visualization Not Displaying**:
       - Check your browser's console for errors and report them as feedback.
    """)

    st.markdown("""
        The complete source code for this project is available on GitHub. You can explore it, report issues, or contribute to its development:


        [![GitHub](https://img.shields.io/badge/Source-GitHub-blue)](https://github.com/MuhammadOmarMuhdhar/SurveyTopicModeling)
    """)

# Call the function to display the documentation page
if __name__ == "__main__":
    documentation()
