import plotly.graph_objects as go
import streamlit as st

def VISUALIZE(summaries, dfs):
    """
    Visualizes processed data, clusters, and their summaries using Plotly.

    Parameters:
        summaries (dict): Contains summary information for positive, negative, and all topic clusters.
        dataframes (dict): Contains processed DataFrames, including positive, negative, and overall clusters.
    """

    if not summaries or not dfs:
        raise ValueError("Both summaries and dataframes must be provided for visualization.")
    
    if not all(key in summaries for key in ['positive_cluster_summary', 'negative_cluster_summary', 'cluster_summary']):
        raise ValueError("Summaries must contain keys for positive, negative, and overall cluster summaries.")
    
    if not all(key in dfs for key in ['positive_processed_df', 'negative_processed_df', 'processed_df']):
        raise ValueError("Dataframes must contain keys for positive, negative, and overall processed DataFrames.")

    # Extract processed DataFrames
    positive_processed_df = dfs['positive_processed_df']
    negative_processed_df = dfs['negative_processed_df']
    processed_df = dfs['processed_df']

    # Extract cluster summaries
    positive_cluster_summary = summaries['positive_cluster_summary']
    negative_cluster_summary = summaries['negative_cluster_summary']
    cluster_summary = summaries['cluster_summary']

    # Calculate sizes for cluster centroids
    num_total_clusters = cluster_summary['cluster'].nunique()
    base_size_factor = max(1000, num_total_clusters* 75 )  
    positive_cluster_summary['Size'] = (positive_cluster_summary['count'] ** 0.5) / (cluster_summary['count'].max() ** 0.5) * base_size_factor / num_total_clusters
    negative_cluster_summary['Size'] = (negative_cluster_summary['count'] ** 0.5) / (cluster_summary['count'].max() ** 0.5) * base_size_factor / num_total_clusters
    cluster_summary['Size'] = (cluster_summary['count'] ** 0.5) / (cluster_summary['count'].max() ** 0.5) * base_size_factor / num_total_clusters

    # Calculate percentage of points in each cluster
    total_points = processed_df.shape[0]
    positive_cluster_summary['Percentage'] = ((positive_cluster_summary['count'] / total_points) * 100).round()
    negative_cluster_summary['Percentage'] = ((negative_cluster_summary['count'] / total_points) * 100).round()
    cluster_summary['Percentage'] = ((cluster_summary['count'] / total_points) * 100).round()

    # Normalize polarity values for coloring
    positive_processed_df['Normalized_Polarity'] = (positive_processed_df['polarity'] - positive_processed_df['polarity'].min()) / (positive_processed_df['polarity'].max() - positive_processed_df['polarity'].min())
    negative_processed_df['Normalized_Polarity'] = ((negative_processed_df['polarity'] - negative_processed_df['polarity'].min()) / (negative_processed_df['polarity'].max() - negative_processed_df['polarity'].min())) * -1
    processed_df['Normalized_Polarity'] = (processed_df['polarity'] - processed_df['polarity'].min()) / (processed_df['polarity'].max() - processed_df['polarity'].min())
    
    positive_cluster_summary['Normalized_Polarity'] = (positive_cluster_summary['Polarity'] - positive_cluster_summary['Polarity'].min()) / (positive_cluster_summary['Polarity'].max() - positive_cluster_summary['Polarity'].min())
    negative_cluster_summary['Normalized_Polarity'] = ((negative_cluster_summary['Polarity'] - negative_cluster_summary['Polarity'].min()) / (negative_cluster_summary['Polarity'].max() - negative_cluster_summary['Polarity'].min())) * -1
    cluster_summary['Normalized_Polarity'] = 2 * ((cluster_summary['Polarity'] - cluster_summary['Polarity'].min()) /
                                              (cluster_summary['Polarity'].max() - cluster_summary['Polarity'].min())) - 1



    # Initialize a Plotly figure
    fig = go.Figure()

    # Add positive responses (individual points)
    fig.add_trace(go.Scatter(
        x=positive_processed_df['Umap_1'],
        y=positive_processed_df['Umap_2'],
        mode='markers',
        marker=dict(
            size=5,
            color=positive_processed_df['Normalized_Polarity'],  # Color scale based on polarity
            colorscale='Blues',  # Blue color scale for positive responses
            opacity=0.8,
        ),
        name='Positive Responses',
        visible=False,
        hovertext=positive_processed_df['responses'].apply(lambda x: f"<b>Response:</b> {x}"),
        hoverinfo="text"
    ))

    # Add positive cluster centroids
    fig.add_trace(go.Scatter(
        x=positive_cluster_summary['Umap_1'],
        y=positive_cluster_summary['Umap_2'],
        mode='markers+text',
        marker=dict(
            size=positive_cluster_summary['Size'],  # Cluster size for visibility
            color=positive_cluster_summary['Normalized_Polarity'],  # Polarity-based coloring
            colorscale='Blues',  # Blue color scale
            colorbar=dict(
                title="Polarity",
                thickness=10,
                len=0.5,
            ),
            opacity=0.5
        ),
        name='Positive Topic Clusters',
        text=positive_cluster_summary['cluster'].astype(str)+ "-" + "("+ positive_cluster_summary['Percentage'].astype(str) + "%" + ")",  # Add percentage text
        hovertext="<b>Topic:</b> " + positive_cluster_summary['Title'],  # Topic title for hover info
        hoverinfo="text",
        visible=False
    ))

    # Add negative responses (individual points)
    fig.add_trace(go.Scatter(
        x=negative_processed_df['Umap_1'],
        y=negative_processed_df['Umap_2'],
        mode='markers',
        marker=dict(
            size=5,
            color=negative_processed_df['Normalized_Polarity'],  # Color scale based on polarity
            colorscale='Reds',  # Red color scale for negative responses
            opacity=0.8,
        ),
        name='Negative Responses',
        visible=False,
        hovertext=negative_processed_df['responses'].apply(lambda x: f"<b>Response:</b> {x}"),
        hoverinfo="text"
    ))

    # Add negative cluster centroids
    fig.add_trace(go.Scatter(
        x=negative_cluster_summary['Umap_1'],
        y=negative_cluster_summary['Umap_2'],
        mode='markers+text',
        marker=dict(
            size=negative_cluster_summary['Size'],  # Cluster size for visibility
            color=negative_cluster_summary['Normalized_Polarity'],  # Polarity-based coloring
            colorscale='Reds',  # Red color scale
            reversescale=True, 
            colorbar=dict(
                title="Polarity",
                thickness=10,
                len=0.5,
            ),
            opacity=0.5
        ),
        name='Negative Topic Clusters',
        text=negative_cluster_summary['cluster'].astype(str)+ "-" + "(" + negative_cluster_summary['Percentage'].astype(str) + "%" + ")",  # Add percentage text
        hovertext="<b>Topic:</b> " + negative_cluster_summary['Title'],  # Topic title for hover info
        hoverinfo="text",
        visible=False
    ))

    # Add overall topic clusters (centroids)
    fig.add_trace(go.Scatter(
        x=cluster_summary['Umap_1'],
        y=cluster_summary['Umap_2'],
        mode='markers+text',
        marker=dict(
            size=cluster_summary['Size'],  # Cluster size for visibility
            color=cluster_summary['Normalized_Polarity'],  # Color based on polarity
            colorscale='RdBu',  # Diverging color scale for polarity
            colorbar=dict(
                title="Polarity",
                thickness=10,
                len=0.5,
            ),
            opacity=0.5
        ),
        name='Topic Clusters',
        text=cluster_summary['Percentage'].astype(str) + "%",  # Add percentage text
        hovertext="<b>Topic:</b> " + cluster_summary['Title'],  # Topic title for hover info
        hoverinfo="text",
        visible=True
    ))

    # Add interactive menu buttons to toggle between views
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Topic Clusters",
                        method="update",
                        args=[
                            {"visible": [False, False, False, False, True, True]},
                            {"title": "All Topic Clusters"}
                        ]
                    ),
                    dict(
                        label="Positive Topic Clusters",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False, False, False]},
                            {"title": "Positive Topic Clusters"}
                        ]
                    ),
                    dict(
                        label="Negative Topic Clusters",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True, False, False]},
                            {"title": "Negative Topic Clusters"}
                        ]
                    )
                ],
                direction="down",
                showactive=True,
                x=1,
                xanchor="left",
                y=1,
                yanchor="bottom"
            )
        ]
    )

    # Update axis and layout styling
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            dtick=3,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            dtick=2,
            showticklabels=True
        ),
        # paper_bgcolor='white',
        # plot_bgcolor='gray',
        width=1200,
        height=800,
        title="Topic Clusters"
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)