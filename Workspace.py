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
        },
        'topic': None
    })


def main():
    """Main function to run the Streamlit app."""

    # Feedback Form in Sidebar
    st.sidebar.markdown("")
    st.sidebar.markdown("")
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

        survey_topic = st.text_input("In 1-5 words, describe the topic of the questionnaire:", "e.g. student study habits" )

        if len(survey_topic.split()) > 5:
            st.error("Please describe the topic in 1-5 words.")
            return False
        elif survey_type != "Choose" and survey_topic != "e.g. student study habits" and survey_topic != "":
            topic = f"This questionnaire is a {survey_type.lower()} focused on '{survey_topic.strip()}'."
            st.session_state.topic = topic

        if st.session_state.topic:
            st.success(f"Topic saved: **{st.session_state.topic}**")
        else:
            st.info("Please select a topic before proceeding.")

        # File Upload Section
        st.subheader("Upload Survey Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is None:
            st.info("Please upload a CSV file with 500 rows or fewer. This limitation helps manage computational resources.")

        if 'demographics' not in st.session_state:
            st.session_state.demographics = {
                'sex': {'include': False, 'column': None},
                'age': {'include': False, 'column': None},
                'ethnicity': {'include': False, 'column': None}
            }

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if len(df) > 500:
                    st.error(
                        "This CSV has more than 500 rows of data"
                    )
                    return False
                st.session_state.df = df
                st.session_state.columns = df.columns.tolist()
                st.success("Data uploaded successfully!")

                # Select Response Column
                responses_column = st.selectbox(
                    "Select the column containing survey responses",
                    [''] + st.session_state.columns
                )

                if responses_column is None:
                    st.error("Please select a column for survey responses.")
                    return False
                if responses_column not in df.columns:
                    st.error(f"The selected column '{responses_column}' does not exist in the DataFrame.")
                    return False
                if df[responses_column].dtype != 'object':
                    st.error(f"The column '{responses_column}' does not contain text data.")
                    return False
                if responses_column is not None: 
                    st.session_state.responses_column = responses_column
                    st.success(f"Responses column selected: **{responses_column}**")

                # Demographics section

                def toggle_demographic(demographic):
                    """Toggles the inclusion of a demographic variable."""
                    st.session_state.demographics[demographic]['include'] = not st.session_state.demographics[demographic]['include']

                st.write("Select demographic categories to include in the analysis (optional):")

                # Checkbox for "Sex"
                sex_column = None
                st.checkbox(
                    "Sex",
                    key="include_sex",
                    on_change=lambda: st.session_state.demographics.update({
                        'sex': {'include': not st.session_state.demographics['sex']['include']}
                    })
                )
                if st.session_state.demographics['sex']['include']:
                    sex_column = st.selectbox("Select Sex Column", st.session_state.columns, key="sex_column")
                    if sex_column is None:
                        st.error("Please select a column for sex, or uncheck the checkbox.")
                        st.stop()  # Stops the app execution
                    st.session_state.demographics['sex']['column'] = sex_column

                # Checkbox for "Age"
                age_column = None
                st.checkbox(
                    "Age",
                    key="include_age",
                    on_change=lambda: st.session_state.demographics.update({
                        'age': {'include': not st.session_state.demographics['age']['include']}
                    })
                )
                if st.session_state.demographics['age']['include']:
                    age_column = st.selectbox("Select Age Column", st.session_state.columns, key="age_column")
                    if age_column is None:
                        st.error("Please select a column for age, or uncheck the checkbox.")
                        st.stop()
                    if df[age_column].dtype not in ['int64', 'float64']:  # Correct condition
                        st.error(f"The column '{age_column}' does not contain numerical data.")
                        st.stop()
                    st.session_state.demographics['age']['column'] = age_column

                # Checkbox for "Ethnicity"
                ethnicity_column = None
                st.checkbox(
                    "Ethnicity",
                    key="include_ethnicity",
                    on_change=lambda: st.session_state.demographics.update({
                        'ethnicity': {'include': not st.session_state.demographics['ethnicity']['include']}
                    })
                )
                if st.session_state.demographics['ethnicity']['include']:
                    ethnicity_column = st.selectbox("Select Ethnicity Column", st.session_state.columns, key="ethnicity_column")
                    if ethnicity_column is None:
                        st.error("Please select a column for ethnicity, or uncheck the checkbox.")
                        st.stop()
                    if df[ethnicity_column].dtype != 'object':  # Text data is typically 'object'
                        st.error(f"The column '{ethnicity_column}' does not contain text data.")
                        st.stop()
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

        # Prepare columns and data
        responses_column = st.session_state.get('responses_column')
        if not responses_column:
            st.error("Responses column not specified.")
            st.stop()

        demographics = st.session_state.get('demographics', {})
        sex_column = demographics.get('sex', {}).get('column')
        age_column = demographics.get('age', {}).get('column')
        ethnicity_column = demographics.get('ethnicity', {}).get('column')

        columns = [responses_column]
        rename_mapping = {responses_column: 'responses'}

        # Add optional demographic columns
        if demographics.get('age', {}).get('include', False):
            columns.append(age_column)
            rename_mapping[age_column] = 'age'

        if demographics.get('sex', {}).get('include', False):
            columns.append(sex_column)
            rename_mapping[sex_column] = 'sex'

        if demographics.get('ethnicity', {}).get('include', False):
            columns.append(ethnicity_column)
            rename_mapping[ethnicity_column] = 'ethnicity'

        # Check for missing columns in DataFrame
        columns = [col for col in columns if col]
        missing_cols = [col for col in columns if col not in st.session_state.df.columns]

        if missing_cols:
            st.error(f"Missing columns in DataFrame: {', '.join(missing_cols)}")
            st.stop()

        # Filter and rename DataFrame
        df = st.session_state.df[columns].rename(columns=rename_mapping)

        st.dataframe(df)

        if st.button("Back"):
            st.session_state.stage = 'upload'
            st.rerun()

        if st.button("Analyze"):
            st.session_state.stage = 'analyze_data'
            st.rerun()

        
        # if "email_submitted" not in st.session_state:
        #     st.session_state.email_submitted = False

        # if not st.session_state.email_submitted:

        #     with st.form("email_form"):
        #         email = st.text_input("This may take a few minutes, enter email to recieve notification when done", placeholder="example@example.com")
        #         updates_opt_in = st.checkbox("I’m interested in receiving updates about this tool.")
        #         submit_email = st.form_submit_button("Notify me when complete")

        #     if submit_email:
        #         if email:
        #             # # Store the email in Google Sheets
        #             # store_email_in_sheets(email, updates_opt_in)
        #             # st.info("Thank you! You will be notified by email once the summarization is complete.")
        #             st.session_state.email_submitted = True  # Mark email as submitted
        #         else:
        #             st.error("Please enter a valid email address.")

        

    # **Analyze Data Stage**
    elif st.session_state.stage == 'analyze_data':
        st.subheader("Analyzing Data")

        # Prepare columns and data
        responses_column = st.session_state.responses_column
        demographics = st.session_state.get('demographics', {})
        sex_column = demographics.get('sex', {}).get('column')
        age_column = demographics.get('age', {}).get('column')
        ethnicity_column = demographics.get('ethnicity', {}).get('column')

        columns = [responses_column]
        rename_mapping = {responses_column: 'responses'}

        # Add optional demographic columns
        if demographics.get('age', {}).get('include', False):
            columns.append(age_column)
            rename_mapping[age_column] = 'age'

        if demographics.get('sex', {}).get('include', False):
            columns.append(sex_column)
            rename_mapping[sex_column] = 'sex'

        if demographics.get('ethnicity', {}).get('include', False):
            columns.append(ethnicity_column)
            rename_mapping[ethnicity_column] = 'ethnicity'

        df = st.session_state.df[columns].rename(columns=rename_mapping)

        # Initialize progress bar and steps
        progress_bar = st.progress(0)
        progress_text = st.empty()  # Placeholder for progress updates
        total_steps = 2
        step = 0

        # Check if processing is already done
        if 'processed_dfs' not in st.session_state or 'summaries' not in st.session_state:
            try:
                # Step 1: Data Processing
                step += 1
                progress_text.text(f"Step {step} of {total_steps}: Processing and clustering data...")
                processed_dfs = processor.feature_engineering(df, detail='default')
                st.session_state.processed_dfs = processed_dfs
                progress_bar.progress(step / total_steps)
                st.success("Data processed successfully!")

                # Step 2: Cluster Summarization
                step += 1
                progress_text.text(f"Step {step} of {total_steps}: Summarizing clusters... This may take a few minutes please do not close the browser.")
                topic = st.session_state.get('topic', 'No topic specified')
                summaries = summary.SUMMARIZER(processed_dfs, topic=topic)
                st.session_state.summaries = summaries
                progress_bar.progress(step / total_steps)
                st.success("Clusters summarized successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                progress_bar.empty()
                return
        else:
            # If already processed, retrieve from session state
            processed_dfs = st.session_state.processed_dfs
            summaries = st.session_state.summaries
            st.info("Data already processed. Skipping to visualization.")

        # Display processed data
        with st.expander("Show processed data"):
            st.write(processed_dfs['processed_df'])

        with st.expander("Show cluster summaries"):
            st.write(summaries['cluster_summary'])

        # Finalize progress bar
        progress_text.text("All steps completed!")
        progress_bar.empty()

        # Transition to the dashboard
        if st.button("Go to Scatterplot"):
            with st.spinner("Loading visuals..."):
                st.session_state.stage = 'dashboard'
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

        st.markdown(
            """
            ### How to explore the scatterplot

            - **Visualization**: Below is a visual representation of clusters, each grouping semantically similar responses. Hover over a cluster to see its title, generated by a large language model summarizing shared themes.

            - **Cluster Summaries**: Expand the sections above to view positive and negative summaries, highlighting key themes for each cluster.
            """
        )

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
