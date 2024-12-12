import google.generativeai as genai
import json 
import time
import streamlit as st

GEMINI_API_KEY = st.secrets["api_key"]

llm_cache = {} 

def generate_content_cached(prompt, model_name="gemini-1.5-flash"):
    """
    Generates content using a generative model with caching to avoid redundant calls.

    """

    genai.configure(api_key=GEMINI_API_KEY)
    
    # Check if the prompt is already cached
    if prompt in llm_cache:
        # If found, retrieve the cached output to save computation time
        output = llm_cache[prompt]
    else:
        # If not cached, wait for 6 seconds (e.g., to adhere to rate limits or for model readiness)
        time.sleep(6)
        
        # Initialize the generative model using the specified model name
        gemini_model = genai.GenerativeModel(model_name)
        
        # Generate content based on the prompt and extract the text output
        output = gemini_model.generate_content(prompt).text
        
        # Store the generated output in the cache for future use
        llm_cache[prompt] = output
    
    # Return the generated output
    return output

def summarize_text(topic, text, cached_topics):
    """
    Generates a title and summary for a cluster of survey responses based on the input text and topic.
    """
    
    template = """
        You are an advanced AI system designed to analyze and summarize clusters of open-ended survey responses. 
        These clusters are semantically similar groups derived from a broader dataset. Your primary goal is to uncover insights that are both specific to the cluster and unique compared to other clusters previously processed. 

        To achieve this, you will:
        1. Analyze the responses in the current cluster and identify key themes, patterns, or ideas.
        2. Compare the insights from this cluster against the previously processed topics to ensure uniqueness.
        3. Generate a clear and actionable output that highlights the most significant insights.

        Your output should include:
        1. A **descriptive topic title** that:
        - Clearly captures the primary theme or insight of the current cluster.
        - Differentiates this cluster from any previously processed clusters listed below.
        2. A **summary** that:
        - Explains the central themes, patterns, or ideas expressed in the current cluster.
        - Identifies commonalities in opinions, emotions, or feedback within the responses.
        - Highlights any unique or surprising insights that make this cluster distinct.
        - Provides concise, actionable insights.

        The dataset's broader topic is: {topic}

        These are the topics from clusters that have already been processed in this dataset: {cached_topics}
        As you generate the title and summary, make sure they reflect what is **distinct and valuable** about this cluster compared to the others. Avoid duplication of previously identified themes.

        Here are the responses from the current cluster:
        {text}

        Your output must strictly be a valid JSON object without any additional formatting, backticks, or newlines. Ensure it follows this exact structure:
        {{
        "title": "<Your descriptive title here>",
        "summary": "<Your detailed and actionable summary here>"
        }}
    """
    
    # Format the prompt with the input text
    try:
        prompt = template.format(topic=topic, text=text, cached_topics=cached_topics)
    except KeyError as e:
        raise ValueError(f"Error formatting template: {e}")

    # Generate the content using the cached function
    output = generate_content_cached(prompt)

    return output

def summarize_clusters(centroids, processed_df, topic):

    """
    Summarizes clusters based on the provided centroids and processed DataFrame.

    """


    polarities = []

    summaries = []

    cached_topics = []

    for cluster_label in centroids['cluster'].unique():
            # Filter data points for the current cluster
            cluster = processed_df[processed_df['cluster'] == cluster_label]

            # Extract relevant text based on the data_type

            polarity = cluster['polarity'].mean()
            
            text = " ".join(cluster['responses'])

            # Generate a summary and title for the current cluster
            cluster_summary_with_title = summarize_text(topic,text, cached_topics)

            # # Debugging: Log the raw output
            # print(f"Raw Output for Cluster {cluster_label}:\n{cluster_summary_with_title}")

            # Enhanced cleaning to remove artifacts
            if isinstance(cluster_summary_with_title, str):
                cluster_summary_with_title = cluster_summary_with_title.strip()  # Remove leading/trailing whitespace
                cluster_summary_with_title = cluster_summary_with_title.lstrip('```json').rstrip('```')  # Remove backticks and json marker
                cluster_summary_with_title = cluster_summary_with_title.strip()  # Strip again after cleaning

            # # Debugging: Log the cleaned output
            # print(f"Cleaned Output for Cluster {cluster_label}:\n{cluster_summary_with_title}")

            # Parse the cleaned JSON string
            try:
                cluster_summary_with_title = json.loads(cluster_summary_with_title)
                cached_topics.append(cluster_summary_with_title['title'])
            except json.JSONDecodeError as e:
                print(f"Error processing cluster {cluster_label}: {e}")
                continue

            summaries.append(cluster_summary_with_title)
            polarities.append(polarity)


    # Add summaries and titles to the centroids DataFrame
    centroids['Summary'] = [summary['summary'] for summary in summaries]
    centroids['Title'] = [summary['title'] for summary in summaries]
    centroids['Polarity'] = polarities

    # # Calculate the percentage of points in each cluster
    # total_points = processed_df.shape[0]
    # centroids['Percentage'] = ((centroids['count'] / total_points) * 100).round()

    # Return the centroids DataFrame with added summaries and titles
    return centroids

def SUMMARIZER(dataframes, topic = 'Thoughts about an AI advertsiment about climate change'):

    """
    Summarizes clusters for positive, negative, and overall datasets.

    Args:
        dataframes (dict): A dictionary containing processed DataFrames and centroids for positive, negative, and overall data.
        topic (str): The overarching topic to guide summarization.

    Returns:
        dict: A dictionary with summaries for positive, negative, and overall clusters.
    """

    positive_processed_df = dataframes['positive_processed_df']
    negative_processed_df = dataframes['negative_processed_df']
    processed_df = dataframes['processed_df']

    positive_centroids = dataframes['positive_centroids']
    negative_centroids = dataframes['negative_centroids']
    centroids = dataframes['centroids']

    positive_cluster_summary = summarize_clusters( positive_centroids,positive_processed_df, topic=topic)
    negative_cluster_summary = summarize_clusters( negative_centroids,negative_processed_df, topic=topic)
    cluster_summary = summarize_clusters( centroids, processed_df, topic=topic)

    return {
        'positive_cluster_summary': positive_cluster_summary,
        'negative_cluster_summary': negative_cluster_summary,
        'cluster_summary': cluster_summary
    }