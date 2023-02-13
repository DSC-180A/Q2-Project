import tensorflow_hub as hub
import tensorflow_text as text
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split

# Create a TF model using BERT
def create_model():
    # Input layer of text
    text_input = tf.keras.layers.Input(shape = (), dtype = tf.string, name = 'raw text')

    # Download Bert Preprocessor
    bert_preprocessor = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3', name='preprocessing')

    # Load BERT from TF Hub
    bert_encoder = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4', name='BERT_encoder')

    encoder_inputs = bert_preprocessor(text_input)
    outputs = bert_encoder(encoder_inputs)

    net = outputs['pooled_output']

    # Add a dense layer with 175 units
    net = tf.keras.layers.Dense(175)(net)
    # Add a dropout layer with 0.1 rate
    net = tf.keras.layers.Dropout(0.1)(net)
    # Add a batch normalization layer
    net = tf.keras.layers.BatchNormalization()(net)
    # Add a Relu activation layer
    net = tf.keras.layers.Activation('relu')(net)
    # Add a dropout layer with 0.1 rate
    net = tf.keras.layers.Dropout(0.1)(net)
    # Add a Dense layer with 100 units
    net = tf.keras.layers.Dense(100)(net)
    # Add a dropout layer with 0.1 rate
    net = tf.keras.layers.Dropout(0.1)(net)
    # Add a batch normalization layer
    net = tf.keras.layers.BatchNormalization()(net)
    # Add a Relu activation layer
    net = tf.keras.layers.Activation('relu')(net)
    # Add a dropout layer with 0.1 rate
    net = tf.keras.layers.Dropout(0.1)(net)
    # Add dense layer with 1 unit with relu
    net = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(net)

    # Create optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=5e-4)
    # Create loss function
    loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    # Create metrics
    metrics = tf.metrics.BinaryAccuracy()
    
    model = tf.keras.Model(text_input, net)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    return model


# Train the model based on dataframe
def train_model(df, model):
    # Create a train and test dataset from modelselection
    train_dataset, test_dataset, train_labels, test_labels = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)    
    # Overfitting
    es = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', mode='max', min_delta=0.3, restore_best_weights=True)
    # Train the model
    history = model.fit(train_dataset, train_labels, epochs=30, batch_size=64, validation_data=(test_dataset, test_labels), callbacks=[es])
    # Save the model
    model.save('data/outbert_model_2.h5')
    
    return history, train_dataset, test_dataset, train_labels, test_labels
