import streamlit as st
import pandas as pd
from processing import processor
from summary import summary
from visuals import visualize

def reset_session_state():
    """Resets the session state variables."""
    st.session_state.update({
        'stage': 'upload',
        'df': None,
        'columns': [],
        'responses_column': None,
        'demographics': {
            'sex': {'include': False, 'column': None},
            'age': {'include': False, 'column': None},
            'ethnicity': {'include': False, 'column': None}
        }
    })

def validate_responses_column(df, column):
    """Validates the selected column for survey responses."""
    if column is None:
        st.error("Please select a column for survey responses.")
        return False
    if column not in df.columns:
        st.error(f"The selected column '{column}' does not exist in the DataFrame.")
        return False
    if not pd.api.types.is_string_dtype(df[column]):
        st.warning(f"The column '{column}' does not contain text data. Are you sure this is the correct column?")
    return True

def toggle_demographic(demographic):
    """Toggles the inclusion of a demographic variable."""
    st.session_state.demographics[demographic]['include'] = not st.session_state.demographics[demographic]['include']

def main():
    """Main function to run the Streamlit app."""

    # Feedback Form in Sidebar
    st.sidebar.markdown("### Share Your Feedback")
    name = st.sidebar.text_input("Your Name", key="name_input")
    email = st.sidebar.text_input("Your Email", key="email_input")
    message = st.sidebar.text_area("Your Feedback or Suggestions", key="message_input")

    if st.sidebar.button("Submit Feedback", key="submit_feedback_button"):
        if name and email and message:
            st.sidebar.success("Thank you for your feedback!")
            # Here, you can implement functionality to store feedback, e.g., saving to a database
        else:
            st.sidebar.error("Please fill in all fields before submitting.")

    # Initialize session state variables if not present
    if 'stage' not in st.session_state:
        reset_session_state()

    # **Upload Stage**
    if st.session_state.stage == 'upload':

        st.subheader("Survey Topic Modelor")
        
        st.markdown(
        "This prototype tool leverages large language models to process and translate open-ended qualitative data—such as survey responses, product reviews, and user feedback into an insightful visualization, providing qualitative insights on patterns and trends in the responses at the topic level."
                    )
        
        st.markdown(
        "We value your feedback! Please share your thoughts, suggestions, or any ideas for improvement to help us refine this tool and make it even more useful."
            )
        
        st.subheader("Questionnaire Topic")

        # Ensure topic is initialized
        if 'topic' not in st.session_state:
            st.session_state.topic = None

        # Topic Selection
        type_of_questionnaire = [
            "Academic Research Survey",
            "Employee Engagement Survey",
            "Customer Feedback Survey",
            "Education Feedback Survey",
            "Market Research Survey",
            "Product Review Survey",
            "Public Policy Opinion Survey",
            "Event or Conference Feedback Survey",
            "Political Attitudes and Trends Survey",
            "Economic and Labor Market Insights Survey",
            "Brand Perception Survey",
            "Training and Development Feedback Survey",
        ]
        
        survey_type = st.selectbox("What type of quiestionnaire is this:", ["Choose"] + type_of_questionnaire)

        survey_topic = st.text_input("In 1-5 words, describe the topic of the questionnaire:")

        if len(survey_topic.split()) > 5:
            st.error("Please describe the topic in 1-5 words.")
            return False
        elif survey_type != "Choose" and survey_topic != "":
            topic = f"This questionnaire is a {survey_type.lower()} focused on '{survey_topic.strip()}'."
            st.session_state.topic = topic

        if st.session_state.topic:
            st.success(f"Topic saved: **{st.session_state.topic}**")
        else:
            st.warning("Please select a topic before proceeding.")

        # File Upload Section
        st.subheader("Upload Survey Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if 'demographics' not in st.session_state:
            st.session_state.demographics = {
                'sex': {'include': False, 'column': None},
                'age': {'include': False, 'column': None},
                'ethnicity': {'include': False, 'column': None}
            }

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.columns = df.columns.tolist()
                st.success("Data uploaded successfully!")

                # Select Response Column
                st.subheader("Select the Column Containing Survey Responses")
                responses_column = st.selectbox(
                    "Select the column containing survey responses",
                    [''] + st.session_state.columns
                )

                if responses_column:
                    if validate_responses_column(st.session_state.df, responses_column):
                        st.session_state.responses_column = responses_column
                        st.success(f"Responses column selected: **{responses_column}**")
                    else:
                        st.error("The selected column is not valid. Please select a different column.")

                # Demographics section
                st.subheader("Select Demographic Columns")
                available_columns = [col for col in st.session_state.columns if col != st.session_state.responses_column]

                st.write("Select demographic categories to include in the analysis:")
                st.checkbox("Sex", key="include_sex", on_change=lambda: toggle_demographic('sex'))
                if st.session_state.demographics['sex']['include']:
                    sex_column = st.selectbox("Select Sex Column", available_columns, key="sex_column")
                    st.session_state.demographics['sex']['column'] = sex_column

                st.checkbox("Age", key="include_age", on_change=lambda: toggle_demographic('age'))
                if st.session_state.demographics['age']['include']:
                    age_column = st.selectbox("Select Age Column", available_columns, key="age_column")
                    st.session_state.demographics['age']['column'] = age_column

                st.checkbox("Ethnicity", key="include_ethnicity", on_change=lambda: toggle_demographic('ethnicity'))
                if st.session_state.demographics['ethnicity']['include']:
                    ethnicity_column = st.selectbox("Select Ethnicity Column", available_columns, key="ethnicity_column")
                    st.session_state.demographics['ethnicity']['column'] = ethnicity_column

                # Navigate to Review Data
                if st.session_state.topic and 'responses_column' in st.session_state and st.session_state.responses_column:
                    if st.button("Review Data"):
                        st.session_state.stage = 'review_data'
                        st.rerun()
                else:
                    st.warning("Ensure topic, data, and responses column are selected before reviewing data.")
            except Exception as e:
                st.error(f"Error processing file: {e}")

    # **Review Data Stage**
    elif st.session_state.stage == 'review_data':
        st.subheader("Review Data")

        selected_cols = [st.session_state.responses_column]
        for demo, data in st.session_state.demographics.items():
            if data['include']:
                selected_cols.append(data['column'])

        subset_df = st.session_state.df[selected_cols].dropna()
        st.write("Selected Data:")
        st.dataframe(subset_df)

        if st.button("Back"):
            st.session_state.stage = 'upload'
            st.rerun()

        if st.button("Analyze Data"):
            st.session_state.stage = 'analyze_data'
            st.rerun()

    # **Analyze Data Stage**
    elif st.session_state.stage == 'analyze_data':
        st.subheader("Analyze Data")
        responses_column = st.session_state.responses_column
        sex_column = st.session_state.demographics['sex']['column']
        age_column = st.session_state.demographics['age']['column']
        ethnicity_column = st.session_state.demographics['ethnicity']['column']

        columns = [responses_column, sex_column, age_column, ethnicity_column]

        # Copy the original DataFrame
        df = st.session_state.df.copy()

        # Ensure demographic columns are only included if they exist
        columns = [st.session_state.responses_column]  # Start with responses column
        rename_mapping = {st.session_state.responses_column: 'responses'}

        # Check and add optional demographic columns
        if 'age' in st.session_state.demographics and st.session_state.demographics['age']['include']:
            columns.append(st.session_state.demographics['age']['column'])
            rename_mapping[st.session_state.demographics['age']['column']] = 'age'

        if 'sex' in st.session_state.demographics and st.session_state.demographics['sex']['include']:
            columns.append(st.session_state.demographics['sex']['column'])
            rename_mapping[st.session_state.demographics['sex']['column']] = 'sex'

        if 'ethnicity' in st.session_state.demographics and st.session_state.demographics['ethnicity']['include']:
            columns.append(st.session_state.demographics['ethnicity']['column'])
            rename_mapping[st.session_state.demographics['ethnicity']['column']] = 'ethnicity'

        # Filter and rename the DataFrame safely
        df = df[columns].rename(columns=rename_mapping)


        progress_bar = st.progress(0)
        progress_text = st.empty()  # Text placeholder for progress updates

        total_steps = 2
        step = 0

        try:
            # Step 1: Data Processing
            step += 1
            progress_text.text(f"Step {step} of {total_steps}: Processing and clustering data...")
            processing_message = st.empty()
            # processing_message.text("Data is being processed...")

            try:
                # Process the data
                processed_dfs = processor.feature_engineering(df, detail='default')
                progress_bar.progress(step / total_steps)

                # Display processed data
                processing_message.empty()
                with st.expander("Show processed data"):
                    st.write(processed_dfs['processed_df'])
                st.success("Data processed successfully!")
            except Exception as e:
                processing_message.empty()
                st.error(f"Error during data processing: {e}")
                progress_bar.empty()
                if st.button("Back"):
                    st.session_state.stage = 'review_data'
                    st.rerun()
                raise e  # Exit if processing fails

            # Step 2: Cluster Summarization
            step += 1
            progress_text.text(f"Step {step} of {total_steps}: Summarizing clusters...This may take a few minutes.")
            summarizer_message = st.empty()
            # summarizer_message.text("Summarizing clusters... This may take a few minutes.")

            try:
                # Summarize the clusters
                topic = st.session_state.get('topic', 'No topic specified')
                summaries = summary.SUMMARIZER(processed_dfs, topic=topic)
                progress_bar.progress(step / total_steps)

                # Display cluster summaries
                summarizer_message.empty()
                with st.expander("Show cluster summaries"):
                    st.write(summaries['cluster_summary'])
                st.success("Clusters summarized successfully!")
            except Exception as e:
                summarizer_message.empty()
                st.error(f"Error during summarization: {e}")
                progress_bar.empty()
                if st.button("Back"):
                    st.session_state.stage = 'review_data'
                    st.rerun()
                raise e  # Exit if summarization fails

            # Finalize progress bar and text
            progress_text.text("All steps completed!")
            progress_bar.empty()

             # Save results to session state for dashboard
            st.session_state.processed_dfs = processed_dfs
            st.session_state.summaries = summaries

            # Option to move to the dashboard
            if st.button("Go to Scatterplot"):
                with st.spinner("Loading visuals..."):
                    st.session_state.stage = 'dashboard'
                    st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {e}")
            progress_text.text("An error occurred during processing.")
            progress_bar.empty()
            if st.button("Back"):
                st.session_state.stage = 'review_data'
                st.rerun()
        

    # Dashboard stage

    elif st.session_state.stage == 'dashboard':
        st.subheader("Dashboard")

        processed_dfs = st.session_state.processed_dfs
        summaries = st.session_state.summaries

        # # Display the processed data
        # with st.expander("Show processed data"):
        #     st.write(st.session_state.processed_dfs['processed_df'])

        # Display the cluster summaries
        with st.expander("Positive Cluster summaries"):
            positive_cluster_summary = summaries['positive_cluster_summary'][['cluster', 'Summary']]
            st.write(positive_cluster_summary)

        with st.expander("Negative Cluster summaries"):
            negative_cluster_summary = summaries['negative_cluster_summary'][['cluster', 'Summary']]                      
            st.write(negative_cluster_summary)
            

        # Display the topic
        
        # Call the visualization function
        try:
            visualize.VISUALIZE(summaries, processed_dfs)  # This renders the plot using st.plotly_chart inside VISUALIZE
        except Exception as e:
            st.error(f"An error occurred during visualization: {e}")

        # Reset session state
        if st.button("Start Over"):
            reset_session_state()
            st.rerun()

if __name__ == "__main__":
    main()
