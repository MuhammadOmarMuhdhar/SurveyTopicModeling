import streamlit as st
import pandas as pd
from processing import processor
from summary import summary
from visuals import visualize

def reset_session_state():
    """Resets the session state variables."""
    st.session_state.update({
        'stage': 'home',
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

    if st.session_state.stage == 'home':

        if "selected_button" not in st.session_state:
            st.session_state.selected_button = None


        st.subheader('Topic Modeler')

        st.markdown('''
                    
        This prototype tool leverages unsupervised machine learning methods and language models to process and extract quantitative insights 
        from open-ended qualitative human data such as survey responses, legal documents, and social media posts. The output is an interactive dashboard 
        that allows you to explore the results. 
        - Understand the tool’s purpose in the **About** tab
        - Learn more about how to use the tool and how it works in the **Documentation** tab.
        - Explore practical examples of the tool in use in the **Case Studies** tab.
        ''')

        st.markdown('''
        ### Get Started

        This prototype is optimized for smaller datasets and won't match the speed of production-grade tools. Its primary purpose is to support exploratory 
        analysis while gathering user feedback to guide future improvements and the creation of a final version.

        We greatly value your input—please share any thoughts, suggestions, or ideas for improvement to help us refine and enhance this tool.
                    
         To get started, select the type of data you wish to analyze below.
        ''')

        st.session_state.selected_button = st.radio(
            "Choose the type of data to analyze:",
            ('Open-ended Surveys', 'Documents')
        )

       
        # st.session_state.selected_button = option

        # # Display which option was selected
        # if st.session_state.selected_button:
        #     st.success(f"Selected: {st.session_state.selected_button}")
        # else:
        #     st.info("No option selected yet.")

        

        # # Display the user's selection
        # st.write(f"You selected: {option}")

        # Continue Button
        if st.button('Continue'):
            if st.session_state.selected_button == 'Open-ended Surveys':
                st.session_state.stage = 'survey'
                st.rerun()
            elif st.session_state.selected_button == 'Documents':
                st.session_state.stage = 'Documents'
                st.rerun()
            else:
                st.warning("Please select an option before continuing.")
        
    # **Upload Stage**
    elif st.session_state.stage == 'survey':

        st.subheader("Survey Topic Modelor")
        
        st.markdown('''
            The Survey Topic Modeler is designed to analyze open-ended survey responses. It clusters responses into meaningful topics, 
            performs sentiment analysis, and generates concise summaries to uncover actionable insights. 

            Examples of what you can use it for:
            - Analyzing course evaluations to identify common themes and areas for improvement.
            - Summarizing customer feedback to inform product development or service enhancements.
            - Gaining insights from employee surveys to shape workplace policies and culture.

            For more information on how it works and how to use it, please see the Documentation tab.
            ''')
        
        # st.markdown(
        # "We value your feedback! Please share your thoughts, suggestions, or any ideas for improvement to help us refine this tool and make it even more useful."
        #     )
        
        st.subheader("Survey Topic")

        st.markdown('''
            Select the type of survey and briefly describe its topic to guide the summarization process.
            ''')

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

        if 'survey_flow' not in st.session_state:
            st.session_state.survey_flow = {
                'broad': {'include': False, 'column': None},
                'sub': {'include': False, 'column': None},
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

                if responses_column == '':
                    st.info("Select the column containing open-ended survey responses")
                    return False
                if responses_column is None:
                    st.error("Please select a column for survey responses.")
                    return False
                if responses_column not in df.columns :
                    st.error(f"The selected column '{responses_column}' does not exist in the DataFrame.")
                    return False
                if df[responses_column].dtype != 'object':
                    st.error(f"The column '{responses_column}' does not contain text data.")
                    return False
                if responses_column is not None: 
                    st.session_state.responses_column = responses_column
                    st.success(f"Responses column selected: **{responses_column}**")

                st.subheader("Organize Survey Flow")
                st.write("""
                    This step is optional and allows you to tailor your analysis based on specific segments of your data.
                    """)

                st.markdown(''' 
                    ##### Broad Grouping 
                    Select a primary grouping criterion (e.g. treatment variable if you're doing an experiment).
                        ''')
                broad_grouping = st.selectbox("Select main grouping criterion", ['']+  st.session_state.columns)
                if broad_grouping:
                    unique_values = st.session_state.df[broad_grouping].nunique()
                    if unique_values > 5:
                        st.error(f"The selected column '{broad_grouping}' has more than 5 unique values, which may be too computationally expensive for this prototype.")
                        return False  # Prevent proceeding if too many unique values
                    else:
                        # Proceed with the survey flow
                        st.session_state.survey_flow['broad'] = {'include': True, 'column': broad_grouping}
                        st.success(f"Column '{broad_grouping}' added as the broad grouping.")

                if broad_grouping: 
                    st.markdown('''
                        ##### Subgrouping
                        After selecting a main grouping, you can refine your analysis by adding a secondary criterion (e.g. differences in 
                        "Age" or "Gender" within "Treatment vs. Control").
                        ''')
                    subgroup_by1 = st.selectbox("Select first subgroup criterion (optional)", [''] +  st.session_state.columns)
                    if subgroup_by1 is broad_grouping:
                        st.error('this is the same as your broader grouping')
                        return False
                    elif subgroup_by1:
                        st.session_state.survey_flow['sub'] = {'include': True, 'column': subgroup_by1}
                
            except Exception as e:
                st.error(f"Error processing file: {e}")

        # Adjust column widths to reduce the gap
        col1, col2 = st.columns([.13, 1.15])  # You can tweak these values for more precise spacing

        with col1:
            if st.button("Back"):
                st.session_state.stage = 'home'
                st.rerun()

        with col2:
            if st.button("Continue"):
                if st.session_state.topic and st.session_state.responses_column:
                    st.session_state.stage = 'review_data'
                    st.rerun()
                else:
                    st.warning("Ensure topic, data, and responses column are selected before reviewing data.")

    # **Review Data Stage**
    elif st.session_state.stage == 'review_data':
        st.subheader("Review Data")

        # Prepare columns and data
        columns = []
        responses_column = st.session_state.responses_column
        if not responses_column:
            st.error("Responses column not specified.")
            st.stop()
        else: 
            columns.append(responses_column)

        broad_grouping = st.session_state.survey_flow['broad']
        if broad_grouping['include'] and broad_grouping['column']:
            columns.append(broad_grouping['column'])

        sub = st.session_state.survey_flow['sub']
        if sub['include'] and sub['column']:
            columns.append(sub['column'])

        st.markdown( '''
                ##### Overall Dataset
        ''')

        df = st.session_state.df[columns]

        st.dataframe(df)

        st.markdown( '''
                ##### Grouped data
        ''')

        if 'groupings' not in st.session_state:
            st.session_state.groupings = {}

        unique_broad_grouping = df[broad_grouping['column']].unique()
        # Iterate over the unique broad groupings
        for group in unique_broad_grouping:
            # Create a subset of the DataFrame for the current broad grouping
            grouping = df[df[broad_grouping['column']] == group]
            
            # Save this subset to session state
            st.session_state.groupings[group] = {'broad_grouping': grouping}

            # Extract the unique values of the subgrouping column
            unique_sub_grouping = df[sub['column']].unique()
            
            # Iterate over the unique subgrouping values
            for subgroup in unique_sub_grouping:
                # Create a subset for the current subgroup
                subgroups = grouping[grouping[sub['column']] == subgroup]
                
                # Save the subgroup to session state
                if group not in st.session_state.groupings:
                    st.session_state.groupings[group] = {}

                st.session_state.groupings[group][subgroup] = subgroups
                
                # Optionally, display the subgroups
                st.write(f"Group: {group}, Subgroup: {subgroup}")
                st.write(subgroups)


        col1, col2 = st.columns([.13, 1.15])

        if col1.button("Back"):
            st.session_state.stage = 'upload'
            st.rerun()

        if col2.button("Continue"):
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
