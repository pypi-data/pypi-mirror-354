# This file is part of the Audiovisually project.
# Here we can find some prediction functions to make our model(s) work.
# The current functions are:

# 1. classify_emotions: Classifies emotions in text using an emotion classification model.

# Feel free to add any functions you find useful.

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification
from transformers import pipeline

## (1) Classify emotions with custom model
def classify_emotions(
    model_path, 
    data, 
    text_column='Sentence', 
    output_column='Predicted Emotion'
):
    """
    Classify emotions in text using a custom model.

    Args:
        model_path (str): Path to the trained emotion classification model.
        data (pd.DataFrame or str): DataFrame or string containing sentences to classify.
        text_column (str): Name of the column with text to classify (if DataFrame).
        output_column (str): Name of the column to store predictions.

    Returns:
        pd.DataFrame or str: DataFrame with predicted emotions or predicted emotion string.
    
    Example:
        >>> from audiovisually.predict import classify_emotions
        >>> df = pd.DataFrame({'Sentence': ['I am happy', 'I am sad']})
        >>> model_path = 'path/to/your/model'
        >>> result_df = classify_emotions(model_path, df)
        >>> classify_emotions(model_path, "I am happy")
    """
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    label_map = ['anger', 'sadness', 'disgust', 'fear', 'surprise', 'neutral', 'happiness']

    # Handle string input
    if isinstance(data, str):
        if not data.strip():
            return ""
        inputs = tokenizer([data], return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        predicted_id = outputs.logits.argmax(dim=1).item()
        return label_map[predicted_id]

    # Handle DataFrame input
    if isinstance(data, pd.DataFrame):
        if data.empty:
            print(f"Warning: Input DataFrame is empty. Returning an empty DataFrame with '{output_column}' column.")
            data[output_column] = []
            return data

        sentences = data[text_column].tolist()
        predicted_emotions = [''] * len(sentences)

        non_empty_indices = [i for i, sentence in enumerate(sentences) if pd.notna(sentence) and str(sentence).strip()]
        non_empty_sentences = [sentences[i] for i in non_empty_indices]

        if non_empty_sentences:
            inputs = tokenizer(non_empty_sentences, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
            predicted_ids = outputs.logits.argmax(dim=1).tolist()
            predicted_labels = [label_map[idx] for idx in predicted_ids]
            for i, label in enumerate(predicted_labels):
                predicted_emotions[non_empty_indices[i]] = label

        data[output_column] = predicted_emotions
        return data

    return f"Input must be a DataFrame or a string."

## (2) Classify emotions with Hugging Face pipeline
def classify_emotions_huggingface(
    data, 
    model_name="j-hartmann/emotion-english-distilroberta-base",
    text_column='Sentence',
    output_column='Predicted Emotion'
):
    """
    Classify emotions in text using a Hugging Face model.

    Args:
        data (pd.DataFrame or str): DataFrame or string containing sentences to classify.
        model_name (str): Hugging Face model name.
        text_column (str): Name of the column with text to classify (if DataFrame).
        output_column (str): Name of the column to store predictions.

    Returns:
        pd.DataFrame or str: DataFrame with predicted emotions or predicted emotion string.

    Example:
        >>> from audiovisually.predict import classify_emotions_huggingface
        >>> df = pd.DataFrame({'Sentence': ['I am happy', 'I am sad']})
        >>> result_df = classify_emotions_huggingface(df)
        >>> classify_emotions_huggingface("I am happy")
    """
    try:
        classifier = pipeline("text-classification", model=model_name, top_k=None)
    except Exception as e:
        print(f"Error loading pipeline with model '{model_name}': {e}")
        if isinstance(data, pd.DataFrame):
            data[output_column] = [''] * len(data)
            return data
        else:
            return ""

    # Handle string input
    if isinstance(data, str):
        if not data.strip():
            return ""
        try:
            prediction = classifier([data])
            label = prediction[0][0]['label']
            if label == 'joy':
                label = 'happiness'
            return label
        except Exception as e:
            print(f"Error during classification: {e}")
            return ""

    # Handle DataFrame input
    if isinstance(data, pd.DataFrame):
        if data.empty:
            print(f"Warning: Input DataFrame is empty. Returning an empty DataFrame with '{output_column}' column.")
            data[output_column] = []
            return data

        sentences = data[text_column].tolist()
        predicted_emotions = [''] * len(sentences)

        non_empty_indices = [i for i, sentence in enumerate(sentences) if pd.notna(sentence) and str(sentence).strip()]
        non_empty_sentences = [sentences[i] for i in non_empty_indices]

        if non_empty_sentences:
            try:
                predictions = classifier(non_empty_sentences)
                predicted_labels = [pred[0]['label'] for pred in predictions]
                predicted_labels = ['happiness' if label == 'joy' else label for label in predicted_labels]
                for i, label in enumerate(predicted_labels):
                    predicted_emotions[non_empty_indices[i]] = label
            except Exception as e:
                print(f"Error during classification: {e}")

        data[output_column] = predicted_emotions
        return data

    return f"Input must be a DataFrame or a string."
