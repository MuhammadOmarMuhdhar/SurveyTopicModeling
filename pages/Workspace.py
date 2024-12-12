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
    if 'stage' not in st.session_state:
        reset_session_state()

    # Upload stage
    if st.session_state.stage == 'upload':

        st.subheader("Define the Questionnaire Topic")

        if 'topic' not in st.session_state:  # Ensure 'topic' exists in session_state
            st.session_state.topic = None

        # user_topic = st.text_input(
        # "Enter the specific topic of your survey or questionnaire:",
        # placeholder="E.g., Customer Satisfaction for Product X, Feedback on Service Y"
        # )
        predefined_topics = [
    "Customer Experiences and Market Insights",
    "Workplace Dynamics and Organizational Behavior",
    "Social and Cultural Trends",
    "Education Systems and Learning Outcomes",
    "Public Policy and Governance",
    "Health and Well-being",
    "Technology Adoption and Digital Transformation",
    "Environmental and Sustainability Practices",
    "Community Engagement and Social Impact",
    "Economic Inequality and Labor Market Trends"
]
        selected_topic = st.selectbox("Or select a predefined topic:", options=["Choose a topic"] + predefined_topics)

        # Save the topic in session_state
        if selected_topic != "Choose a topic":
            st.session_state.topic = selected_topic
        # elif user_topic:
        #     st.session_state.topic = user_topic

        # Display the topic if set
        if st.session_state.topic:
            st.success(f"Topic saved: **{st.session_state.topic}**")
        else:
            st.warning("Please provide or select a questionnaire topic.")

        st.subheader("Upload Survey Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.columns = df.columns.tolist()
                if st.button("Select Columns"):
                    st.session_state.stage = 'select_responses'
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading the file: {e}")

       

        

    # Select responses column stage
    # Select responses column stage
    elif st.session_state.stage == 'select_responses':
        st.subheader("Select the Column Containing Survey Responses")

        # Display column options for user selection
        responses_column = st.selectbox("Select the column containing survey responses", options=[''] + st.session_state.columns)

        # Create columns for navigation buttons
        c1, c2 = st.columns([1, 9])

        # Handle "Back" button logic
        if c1.button("Back"):
            st.session_state.stage = 'upload'
            st.rerun()

        # Ensure a valid column is selected
        if responses_column:
            if validate_responses_column(st.session_state.df, responses_column):
                st.session_state.responses_column = responses_column

                # Handle "Select Demographics" button logic
                if c2.button("Select Demographics"):
                    st.session_state.stage = 'select_demographics'
                    st.rerun()
            else:
                st.error("The selected column is not valid for survey responses. Please select a different column.")

    # Select demographics stage
    elif st.session_state.stage == 'select_demographics':
        st.subheader("Select Demographic Columns")
        available_columns = [col for col in st.session_state.columns if col != st.session_state.responses_column]
        st.write("Select which demographic categories you want to include in the analysis:")

        st.checkbox("Sex", key="include_sex", value=st.session_state.demographics['sex']['include'], on_change=lambda: toggle_demographic('sex'))
        if st.session_state.demographics['sex']['include']:
            sex_column = st.selectbox("Select Sex Column", available_columns, key="sex_column")
            st.session_state.demographics['sex']['column'] = sex_column

        st.checkbox("Age", key="include_age", value=st.session_state.demographics['age']['include'], on_change=lambda: toggle_demographic('age'))
        if st.session_state.demographics['age']['include']:
            age_column = st.selectbox("Select Age Column", available_columns, key="age_column")
            st.session_state.demographics['age']['column'] = age_column

        st.checkbox("Ethnicity", key="include_ethnicity", value=st.session_state.demographics['ethnicity']['include'], on_change=lambda: toggle_demographic('ethnicity'))
        if st.session_state.demographics['ethnicity']['include']:
            ethnicity_column = st.selectbox("Select Ethnicity Column", available_columns, key="ethnicity_column")
            st.session_state.demographics['ethnicity']['column'] = ethnicity_column

        c1, c2 = st.columns([1,9])
        if c1.button("Back"):
            st.session_state.stage = 'select_responses'
            st.rerun()

        if st.button("Review Data"):
            st.session_state.stage = 'review_data'
            st.rerun()

    # Review data stage
    elif st.session_state.stage == 'review_data':
        st.subheader("Review Data")

        selected_cols = [st.session_state.responses_column]
        for demographic, data in st.session_state.demographics.items():
            if data['include']:
                selected_cols.append(data['column'])

        subset_df = st.session_state.df[selected_cols].dropna()
        st.write("Selected Data:")
        st.dataframe(subset_df)

        c1, c2 = st.columns([1,9])

        if c1.button("Back"):
            st.session_state.stage = 'select_demographics'
            st.rer

        if c2.button("Analyze Data"):
            st.session_state.stage = 'analyze_data'
            st.rerun()



    # Analyze data stage
    elif st.session_state.stage == 'analyze_data':
        st.subheader("Analyze Data")
        responses_column = st.session_state.responses_column
        sex_column = st.session_state.demographics['sex']['column']
        age_column = st.session_state.demographics['age']['column']
        ethnicity_column = st.session_state.demographics['ethnicity']['column']

        columns = [responses_column, sex_column, age_column, ethnicity_column]

        df = st.session_state.df.copy()

        df = df[columns].rename(columns={responses_column: 'responses', age_column: 'age', 
                                         sex_column: 'sex', ethnicity_column: 'ethnicity'})


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
            if st.button("Go to Dashboard"):
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
