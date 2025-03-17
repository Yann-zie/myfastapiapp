import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Initialize the VADER Sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Initialize the HuggingFace pipeline for RoBERTa sentiment analysis
try:
    roberta_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
except Exception as e:
    print(f"Error initializing RoBERTa pipeline: {e}")
    roberta_analyzer = None

# Function to perform sentiment analysis using VADER
def analyze_sentiment_vader(text):
    sentiment = vader_analyzer.polarity_scores(text)
    return sentiment

# Function to perform sentiment analysis using RoBERTa
def analyze_sentiment_roberta(text):
    if not roberta_analyzer:
        raise RuntimeError("RoBERTa analyzer not initialized.")
    sentiment = roberta_analyzer(text)
    return sentiment

# Function to perform combined sentiment analysis
def analyze_sentiment_combined(text):
    vader_sentiment = analyze_sentiment_vader(text)
    roberta_sentiment = analyze_sentiment_roberta(text)
    
    vader_score = vader_sentiment['compound']
    roberta_label = roberta_sentiment[0]['label']
    roberta_score = roberta_sentiment[0]['score']
    
    combined_result = {
        "VADER Sentiment": vader_score,
        "RoBERTa Sentiment": roberta_label,
        "RoBERTa Score": roberta_score
    }
    return combined_result

# Function to choose sentiment analysis method
def get_sentiment(text, method='combined'):
    if method == 'vader':
        return analyze_sentiment_vader(text)
    elif method == 'roberta':
        return analyze_sentiment_roberta(text)
    elif method == 'combined':
        return analyze_sentiment_combined(text)
    else:
        raise ValueError("Sentiment analysis method must be 'vader', 'roberta', or 'combined'.")

# Function to plot VADER Sentiment Scores
def plot_vader_sentiment(df):
    try:
        vader_scores = df['Sentiment'].apply(lambda x: json.loads(x)["VADER Sentiment"])
        plt.figure(figsize=(8, 6))
        plt.hist(vader_scores, bins=20, color='skyblue', edgecolor='black')
        plt.title("VADER Sentiment Scores Distribution", fontsize=16)
        plt.xlabel("VADER Sentiment Score", fontsize=14)
        plt.ylabel("Frequency", fontsize=14)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error plotting VADER sentiment scores: {e}")

# Function to plot RoBERTa Sentiment Labels with proper names
def plot_roberta_sentiment(df):
    try:
        # Map RoBERTa labels from numbers to meaningful names
        label_mapping = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        
        # Extract RoBERTa sentiment labels and replace numbers with names
        roberta_labels = df['Sentiment'].apply(lambda x: label_mapping[json.loads(x)["RoBERTa Sentiment"]])
        
        # Count occurrences of each sentiment category
        label_counts = roberta_labels.value_counts()

        # Plot using Seaborn
        plt.figure(figsize=(8, 6))
        sns.barplot(x=label_counts.index, y=label_counts.values, palette="coolwarm")
        plt.title("RoBERTa Sentiment Labels Distribution", fontsize=16, fontweight='bold')
        plt.xlabel("Sentiment Category", fontsize=14)
        plt.ylabel("Frequency", fontsize=14)
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error plotting RoBERTa sentiment labels: {e}")

# Function to load conversation logs from prompts.csv
def load_conversation_logs(file_path="prompts.csv"):
    try:
        # Load CSV file
        df = pd.read_csv(file_path)
        
        # Ensure the 'Prompt' column exists
        if 'Prompt' not in df.columns:
            raise KeyError("The CSV file must contain a 'Prompt' column.")
        
        # Perform sentiment analysis on each prompt
        df['Sentiment'] = df['Prompt'].apply(lambda x: json.dumps(analyze_sentiment_combined(x)))
        return df
    except Exception as e:
        print(f"Error loading conversation logs: {e}")
        return pd.DataFrame()

# Main function to generate reports
def generate_sentiment_reports():
    try:
        # Load prompts from the CSV file
        df = load_conversation_logs("prompts.csv")
        
        if df.empty:
            print("No data to process.")
            return
        
        # Display the first few rows of the processed DataFrame
        print("Processed DataFrame:")
        print(df.head())
        
        # Plot VADER Sentiment Scores
        plot_vader_sentiment(df)
        
        # Plot RoBERTa Sentiment Labels
        plot_roberta_sentiment(df)
    except Exception as e:
        print(f"Error generating sentiment reports: {e}")

# Call the main function
generate_sentiment_reports()
