from processing import clusters
from processing import sentiment
from processing import embeddings
import pandas as pd

def feature_engineering(df, detail):
    """
    Process the input DataFrame through sentiment analysis, embedding reduction, and clustering.

    """

    if 'responses' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'responses' column.")

    # Perform sentiment analysis
    sentiment_analysis_df = sentiment.sentiment_analysis(df)

    # Generate embeddings and reduce dimensionality
    reduced_embeddings = embeddings.reduced_embeddings(df['responses'])
    reduced_embeddings_df = pd.concat([df, reduced_embeddings], axis=1)

    # Create clusters using reduced embeddings
    labels = pd.DataFrame(clusters.create_clusters(reduced_embeddings_df, granularity=detail), columns=['cluster'])
    labels_df = pd.concat([sentiment_analysis_df, reduced_embeddings, labels], axis=1)

    # Filter out noise points (where cluster = -1)
    processed_df = labels_df[labels_df['cluster'] != -1]

    # Split processed data into positive and negative sentiment subsets
    positive_processed_df = processed_df[processed_df['polarity_categorical'] == 'positive']
    negative_processed_df = processed_df[processed_df['polarity_categorical'] == 'negative']

    # Calculate centroids (mean positions) for each cluster
    centroids = processed_df.groupby('cluster')[['Umap_1', 'Umap_2']].mean().reset_index()

    # Calculate centroids for positive and negative clusters
    positive_centroids = positive_processed_df.groupby('cluster')[['Umap_1', 'Umap_2']].mean().reset_index()
    negative_centroids = negative_processed_df.groupby('cluster')[['Umap_1', 'Umap_2']].mean().reset_index()

    # Calculate the number of points in each cluster
    cluster_counts = processed_df['cluster'].value_counts().reset_index()
    cluster_counts.columns = ['cluster', 'count']
    
    positive_cluster_counts = positive_processed_df['cluster'].value_counts().reset_index()
    positive_cluster_counts.columns = ['cluster', 'count']

    negative_cluster_counts = negative_processed_df['cluster'].value_counts().reset_index()
    negative_cluster_counts.columns = ['cluster', 'count']

    # Merge centroids with cluster counts for overall, positive, and negative clusters
    centroids = centroids.merge(cluster_counts, on='cluster')
    positive_centroids = positive_centroids.merge(positive_cluster_counts, on='cluster')
    negative_centroids = negative_centroids.merge(negative_cluster_counts, on='cluster')

    # Return results as a dictionary for better access
    return {
        'sentiment_analysis_df': sentiment_analysis_df,
        'reduced_embeddings_df': reduced_embeddings_df,
        'processed_df': processed_df,
        'positive_processed_df': positive_processed_df,
        'negative_processed_df': negative_processed_df,
        'centroids': centroids,
        'positive_centroids': positive_centroids,
        'negative_centroids': negative_centroids
    }

def PROCESSOR(df, detail, demographics=None):
    """
    Process the input DataFrame through sentiment analysis, embedding reduction, and clustering.

    Parameters:
        df (pd.DataFrame): Input DataFrame with a 'responses' column and optional demographic columns.
        detail (int): Granularity for clustering.
        demographic (list, optional): List of column names containing demographic data to include in the final processed DataFrame.

    Returns:
        pd.DataFrame: Final processed DataFrame with sentiment, embeddings, clusters, and demographics (excluding noise).


    """

    columns = df.columns

    if 'responses' not in columns:
        raise ValueError("Input DataFrame must contain a 'responses' column.")
    
    if demographics:
        for demographic in demographics:
            if demographic not in columns:
                raise ValueError(f"Input DataFrame must contain the '{demographic}' column.")
    
    dataframes = feature_engineering(df, detail, demographics)
            
    columns = df.columns

    
            
    # process age by grouping into age groups
    if 'age' in df.columns:
        age_groups = pd.cut(df['age'], bins=[0, 18, 25, 35, 45, 55, 65, 75, 85, 100], labels=['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76-85', '86-100'])
        df['age'] = age_groups
        age_group_counts = age_groups.value_counts().sort_index()


        
        

    

        

    
    
    
    


   