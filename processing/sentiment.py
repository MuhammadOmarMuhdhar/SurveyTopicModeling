from textblob import TextBlob

def sentiment_analysis(df):
    """
    This function performs sentiment analysis on the 'responses' column of the given DataFrame.
    It calculates the polarity and subjectivity of each response using TextBlob, and then categorizes
    the polarity and subjectivity into descriptive labels.

    """
    # Replace NaN values with empty strings
    df['responses'] = df['responses'].fillna('').astype(str)
    
    # Calculate polarity using TextBlob
    df['polarity'] = df['responses'].apply(lambda text: TextBlob(text).sentiment.polarity)
    
    # Calculate subjectivity using TextBlob
    df['subjectivity'] = df['responses'].apply(lambda text: TextBlob(text).sentiment.subjectivity)

    # Categorize polarity as positive, neutral, or negative
    df['polarity_categorical'] = df['polarity'].apply(lambda x: 'positive' if x > 0 else ('neutral' if x == 0 else 'negative'))
    
    # Categorize subjectivity as objective or subjective
    df['subjectivity_categorical'] = df['subjectivity'].apply(lambda x: 'objective' if x == 0 else 'subjective')

    return df
