from sentence_transformers import SentenceTransformer
import pandas as pd 
from sklearn.decomposition import PCA
from umap import UMAP

def clean_text(text_column):
    # Lowercase the text (case-insensitive model)
    cleaned_text = text_column.str.lower()

    # Normalize whitespace (remove extra spaces, tabs, newlines)
    cleaned_text = cleaned_text.str.replace(r'\s+', ' ', regex=True).str.strip()

    # Remove punctuation
    cleaned_text = cleaned_text.str.replace(r'[^\w\s]', '', regex=True)

    return cleaned_text


def get_embeddings(cleaned_text):
    """
    Generates embeddings for a given text using the SentenceTransformer model.

    """
    # Load the pre-trained SentenceTransformer model
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Generate embeddings for the input text
    embeddings = embedding_model.encode(cleaned_text)
    
    # Convert the embeddings into a DataFrame for structured use
    embeddings_df = pd.DataFrame(embeddings)

    return embeddings_df


def optimal_pca_components(raw_embeddings, variance_threshold=0.80):
    """
    Determines the minimum number of PCA components required to capture the specified variance.
    Fits the PCA model and transforms the data accordingly.

    """
    # Initialize PCA without specifying the number of components
    pca = PCA()
    pca.fit(raw_embeddings)
    
    # Compute cumulative explained variance ratio
    cumulative_variance = pca.explained_variance_ratio_.cumsum()
    
    # Find the number of components that meet or exceed the threshold
    n_components = (cumulative_variance >= variance_threshold).argmax() + 1
    
    # Fit a new PCA model with the optimal number of components
    pca_model = PCA(n_components=n_components)
    pca_transformed = pca_model.fit_transform(raw_embeddings)

    pca_df = pd.DataFrame(pca_transformed, columns=[f"PC{i+1}" for i in range(pca_model.n_components_)])
    
    return pca_df


def umap_transformation(pca_embeddings):
    """
    Applies UMAP dimensionality reduction to transform PCA embeddings into 3D space.
    
    """
    # Perform UMAP transformation
    embedding_2d = UMAP(random_state=211).fit_transform(pca_embeddings)
    embedding_df_2d = pd.DataFrame(embedding_2d, columns=['Umap_1', 'Umap_2'])
    return embedding_df_2d



def reduced_embeddings(text_column):
    """
    Generates reduced embeddings from a DataFrame based on the specified data type (either 'paper' or 'abstract').
    """

    cleaned_text = clean_text(text_column)
    embeddings = get_embeddings(cleaned_text)
    pca_reduced_embeddings = optimal_pca_components(embeddings)
    embedding_df_2d = umap_transformation(pca_reduced_embeddings)

    return embedding_df_2d





