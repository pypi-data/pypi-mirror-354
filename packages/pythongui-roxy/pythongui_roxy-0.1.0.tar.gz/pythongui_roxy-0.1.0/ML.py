# ML

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

latent_dim = 4  # 잠재변수 차원 (AutoEncoder에 필요)

def load_data(csv_path):
    df = pd.read_csv(csv_path, encoding='cp949')

    X_pose = df[["x", "y", "z", "Rx", "Ry", "Rz"]].values
    X_angles = df[["theta1", "theta2", "theta3", "theta4", "theta5", "theta6"]].values

    X_all = np.hstack([X_pose, X_angles])
    Y = X_angles

    scaler_X = MinMaxScaler().fit(X_all)
    X_all_scaled = scaler_X.transform(X_all)

    scaler_Y = MinMaxScaler().fit(Y)
    Y_scaled = scaler_Y.transform(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(X_all_scaled, Y_scaled,
                                                        test_size=0.1, random_state=0)

    return X_train, X_test, Y_train, Y_test, scaler_X, scaler_Y


def build_encoder():
    input_ = layers.Input(shape=(12,))
    x = layers.Dense(256, activation='relu')(input_)
    x = layers.Dense(128, activation='relu')(x)
    z = layers.Dense(latent_dim)(x)
    return models.Model(inputs=input_, outputs=z, name="Encoder")

def build_decoder():
    input_ = layers.Input(shape=(6 + latent_dim,))
    x = layers.Dense(128, activation='relu')(input_)
    x = layers.Dense(256, activation='relu')(x)
    out = layers.Dense(6)(x)
    return models.Model(inputs=input_, outputs=out, name="Decoder")

def build_autoencoder_model(encoder, decoder):
    input_all = tf.keras.Input(shape=(12,))
    pose_input = input_all[:, :6]
    post_processing = encoder(input_all)
    decoder_input = tf.concat([pose_input, post_processing], axis=-1)
    output = decoder(decoder_input)
    return tf.keras.Model(inputs=input_all, outputs=output)

def train_model(csv_path, model_type="autoencoder", save_decoder_path="ik_decoder.h5"):
    X_train, X_test, Y_train, Y_test, scaler_X, scaler_Y = load_data(csv_path)

    if model_type == "autoencoder":
        encoder = build_encoder()
        decoder = build_decoder()
        model = build_autoencoder_model(encoder, decoder)
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), 
              epochs=50, batch_size=1024)

    decoder.save(save_decoder_path)
    return decoder, scaler_X, scaler_Y

def predict_random_ik(pose, decoder, scaler_X, scaler_Y, num_variations=10):
    results = []
    pose = np.array(pose).reshape(1, -1)
    pose_min = scaler_X.data_min_[:6]
    pose_max = scaler_X.data_max_[:6]
    pose_scaled = (pose - pose_min) / (pose_max - pose_min)

    for _ in range(num_variations):
        z = np.random.normal(0, 1, size=(1, latent_dim))
        input_decoder = np.hstack([pose_scaled, z])
        pred_scaled = decoder.predict(input_decoder, verbose=0)
        pred_real = scaler_Y.inverse_transform(pred_scaled)
        results.append(pred_real[0])

    return results

def load_decoder_model(model_path):
    return load_model(model_path)