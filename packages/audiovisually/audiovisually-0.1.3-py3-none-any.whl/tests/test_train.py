import pytest
import pandas as pd
import os
import shutil

# Use a small output dir for test models
TEST_OUTPUT_DIR = "./test_model_output"
RETRAINED_OUTPUT_DIR = "./retrained_model_output"

@pytest.fixture
def small_train_df():
    return pd.DataFrame({
        "Sentence": ["I am happy", "I am sad", "I am angry", "I am surprised"],
        "Label": ["happiness", "sadness", "anger", "surprise"]
    })

@pytest.fixture
def small_val_df():
    return pd.DataFrame({
        "Sentence": ["I am disgusted", "I am neutral"],
        "Label": ["disgust", "neutral"]
    })

def teardown_module(module):
    # Clean up test model output directories after tests
    if os.path.exists(TEST_OUTPUT_DIR):
        shutil.rmtree(TEST_OUTPUT_DIR)
    if os.path.exists(RETRAINED_OUTPUT_DIR):
        shutil.rmtree(RETRAINED_OUTPUT_DIR)

# (1) - Test: train_new_transformer_model basic functionality
def test_train_new_transformer_model_basic(small_train_df):
    from audiovisually.train import train_new_transformer_model
    trainer = train_new_transformer_model(
        small_train_df,
        model_name="distilroberta-base",
        output_dir=TEST_OUTPUT_DIR,
        epochs=1,
        batch_size=2,
        learning_rate=1e-4,
        eval_split=0.5,
        patience=1
    )
    assert hasattr(trainer, "model")
    assert os.path.exists(TEST_OUTPUT_DIR)
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "config.json"))

# (2) - Test: train_new_transformer_model with custom label list
def test_train_new_transformer_model_custom_labels(small_train_df):
    from audiovisually.train import train_new_transformer_model
    label_list = ["happiness", "sadness", "anger", "surprise"]
    trainer = train_new_transformer_model(
        small_train_df,
        model_name="distilroberta-base",
        output_dir=TEST_OUTPUT_DIR,
        epochs=1,
        batch_size=2,
        label_list=label_list,
        patience=1
    )
    assert hasattr(trainer, "model")
    assert trainer.model.config.num_labels == len(label_list)

# (3) - Test: train_new_transformer_model with validation_df
def test_train_new_transformer_model_with_validation(small_train_df, small_val_df):
    from audiovisually.train import train_new_transformer_model
    trainer = train_new_transformer_model(
        small_train_df,
        model_name="distilroberta-base",
        output_dir=TEST_OUTPUT_DIR,
        epochs=1,
        batch_size=2,
        validation_df=small_val_df,
        patience=1
    )
    assert hasattr(trainer, "model")

# (4) - Test: retrain_existing_model basic functionality
def test_retrain_existing_model_basic(small_train_df):
    from audiovisually.train import train_new_transformer_model, retrain_existing_model
    # First, train a model to get a model directory
    trainer1 = train_new_transformer_model(
        small_train_df,
        model_name="distilroberta-base",
        output_dir=TEST_OUTPUT_DIR,
        epochs=1,
        batch_size=2,
        patience=1
    )
    # Now retrain using the saved model, to a separate directory
    trainer2 = retrain_existing_model(
        TEST_OUTPUT_DIR,
        small_train_df,
        output_dir=RETRAINED_OUTPUT_DIR,
        epochs=1,
        batch_size=2,
        patience=1
    )
    assert hasattr(trainer2, "model")
    # Clean up retrained model directory immediately after test
    if os.path.exists(RETRAINED_OUTPUT_DIR):
        shutil.rmtree(RETRAINED_OUTPUT_DIR)

# (5) - Test: get_model_info returns expected keys
def test_get_model_info_keys():
    from audiovisually.train import get_model_info
    info = get_model_info("distilroberta-base")
    assert isinstance(info, dict)
    for key in ["model_name", "architecture", "num_labels", "id2label", "label2id", "vocab_size", "max_length"]:
        assert key in info