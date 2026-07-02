"""
Train a compact CNN on the MNIST dataset and export to TensorFlow.js format.
No tensorflowjs package needed — exports model.json + weights.bin directly.

Usage:
    pip install tensorflow
    python train_digit_model.py

Output:
    digit_model/model.json          — TF.js model architecture + weight manifest
    digit_model/group1-shard1of1.bin — trained weights
"""

import os
import json
import struct
import numpy as np

# Suppress TF info logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ── 1. Load MNIST ──
print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalise to [0, 1] and reshape to (N, 28, 28, 1)
x_train = x_train.astype('float32') / 255.0
x_test  = x_test.astype('float32')  / 255.0
x_train = x_train.reshape(-1, 28, 28, 1)
x_test  = x_test.reshape(-1, 28, 28, 1)

# One-hot encode labels
y_train = keras.utils.to_categorical(y_train, 10)
y_test  = keras.utils.to_categorical(y_test, 10)

print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")

# ── 2. Build a compact CNN ──
model = keras.Sequential([
    layers.Input(shape=(28, 28, 1)),
    layers.Conv2D(8,  (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.GlobalAveragePooling2D(),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ── 3. Train ──
print("\nTraining model...")
model.fit(
    x_train, y_train,
    epochs=8,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# ── 4. Evaluate ──
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\nTest accuracy: {acc*100:.2f}%")
print(f"Test loss:     {loss:.4f}")

if acc < 0.95:
    print("WARNING: Accuracy below 95%. Consider training more epochs.")

# ── 5. Export to TensorFlow.js format (manual, no tensorflowjs package needed) ──
output_dir = 'digit_model'
os.makedirs(output_dir, exist_ok=True)

print("\nExporting to TensorFlow.js format...")

# Collect all weights as float32 bytes
weight_data = bytearray()
weight_specs = []

for layer in model.layers:
    for w in layer.weights:
        # BUG FIX: on Keras 3 (TF >= 2.16), w.name is just the bare variable
        # name (e.g. "kernel", "bias") — NOT a scoped name like
        # "conv2d_3/kernel:0". Every Conv2D/Dense layer has a "kernel" and a
        # "bias", so using w.name directly causes duplicate names across
        # layers, which silently overwrite each other in the TF.js weight
        # map at load time. Scope the name with the layer name to keep it
        # unique.
        short_name = w.name.split('/')[-1].split(':')[0]
        name = f"{layer.name}/{short_name}"

        arr = w.numpy().astype(np.float32)
        shape = list(arr.shape)

        # Determine dtype string for TF.js
        dtype = 'float32'

        weight_specs.append({
            'name': name,
            'shape': shape,
            'dtype': dtype
        })

        # Append raw bytes
        weight_data.extend(arr.tobytes())

# Write binary weights file
weights_filename = 'group1-shard1of1.bin'
weights_path = os.path.join(output_dir, weights_filename)
with open(weights_path, 'wb') as f:
    f.write(weight_data)

# BUG FIX: Keras 3's get_config() output has two quirks TF.js's layer
# deserializer doesn't understand:
#   1. InputLayer config uses "batch_shape" instead of the older
#      "batch_input_shape" key TF.js expects.
#   2. "dtype" can be a policy dict (e.g. {"class_name": "DTypePolicy", ...})
#      instead of a plain string like "float32".
# Without this, tf.loadLayersModel() can throw while parsing the topology.
def sanitize_layer_config(cfg):
    cfg = dict(cfg)

    if 'batch_shape' in cfg:
        cfg['batch_input_shape'] = cfg.pop('batch_shape')

    dtype = cfg.get('dtype')
    if isinstance(dtype, dict):
        cfg['dtype'] = dtype.get('config', {}).get('name', 'float32')
    elif dtype is not None and not isinstance(dtype, str):
        cfg['dtype'] = 'float32'

    return cfg

# Build model topology
keras_config = model.get_config()
model_topology = {
    'class_name': 'Sequential',
    'config': {
        'name': keras_config['name'],
        'layers': []
    },
    'keras_version': getattr(keras, '__version__', tf.__version__),
    'backend': 'tensorflow'
}

# For Sequential models, pass the config through, sanitized per-layer.
# (Sequential's tfjs deserializer rebuilds the model by calling .add() for
# each layer in order, so no inbound_nodes graph wiring is needed here.)
for layer_cfg in keras_config['layers']:
    lc = dict(layer_cfg)
    lc['config'] = sanitize_layer_config(lc['config'])
    model_topology['config']['layers'].append(lc)

# Build the full model.json
model_json = {
    'format': 'layers-model',
    'generatedBy': 'VoicePay digit trainer',
    'convertedBy': 'manual-export',
    'modelTopology': model_topology,
    'weightsManifest': [{
        'paths': [weights_filename],
        'weights': weight_specs
    }]
}

# Write model.json
model_json_path = os.path.join(output_dir, 'model.json')
with open(model_json_path, 'w') as f:
    json.dump(model_json, f, indent=2)

# Print summary
print(f"\nTF.js model saved to {output_dir}/")
for fname in os.listdir(output_dir):
    size = os.path.getsize(os.path.join(output_dir, fname))
    print(f"  {fname}  ({size:,} bytes)")

total_params = sum(np.prod(s['shape']) for s in weight_specs)
print(f"\nTotal parameters: {total_params:,}")
print(f"Weight file size: {len(weight_data):,} bytes")
print(f"\nDone! The model is ready for VoicePay.")
print(f"Demo PIN is: 1-2-2-1")
