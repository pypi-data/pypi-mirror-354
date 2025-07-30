import requests
import base64
import json
import tensorflow as tf
import numpy as np
import os
import pickle
import logging

try:
    from phe import paillier
    PHE_AVAILABLE = True
except ImportError:
    PHE_AVAILABLE = False

from cifer.config import CiferConfig

logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class CiferClient:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api=None,
                 dataset_path=None, model_path=None, use_encryption=False):
        print("Initializing Cifer Client...")

        if isinstance(model_path, bool) and use_encryption is False:
            use_encryption = model_path
            model_path = None

        self.config = CiferConfig(
            encoded_project_id,
            encoded_company_id,
            encoded_client_id,
            base_api,
            dataset_path,
            model_path
        )

        self.api_url = self.config.base_api
        self.dataset_path = self.config.dataset_path
        self.model_path = self.config.model_path
        self.use_encryption = use_encryption
        self.epochs = 1

        if self.use_encryption:
            if not PHE_AVAILABLE:
                raise ImportError("⚠️ 'phe' library is required for encryption. Please install with: pip install phe")
            print("Homomorphic Encryption ENABLED")
            self.public_key, self.private_key = paillier.generate_paillier_keypair()
        else:
            print("Homomorphic Encryption DISABLED")

        if os.path.exists(self.dataset_path) and os.path.exists(self.model_path):
            self.model = self.load_model()
        else:
            self.model = None

        self.latest_accuracy = None

    def load_dataset(self):
        print("Loading dataset...")
        if os.path.exists(self.dataset_path):
            try:
                data = np.load(self.dataset_path)
                train_images = data["train_images"]
                train_labels = data["train_labels"]
            except Exception as e:
                print(f"❌ Error loading dataset: {e}")
                return None, None

            if train_images.ndim == 3:
                print("✅ Detected image dataset (e.g., MNIST).")
            elif train_images.ndim == 2:
                print("✅ Detected tabular dataset (e.g., Fraud Detection).")
            else:
                print(f"❌ Invalid dataset shape: {train_images.shape}")
                return None, None

            if train_images.size == 0 or train_labels.size == 0:
                print("❌ ERROR: Dataset is empty!")
                return None, None

            return train_images, train_labels
        else:
            print("❌ Dataset not found! Please check dataset path.")
            return None, None

    def load_model(self):
        print("Loading or creating model...")
        if os.path.exists(self.model_path):
            print(f"📂 Loading model from {self.model_path} ...")
            return tf.keras.models.load_model(self.model_path)
        else:
            print("❌ Model file not found, creating new model...")
            return self.create_new_model_by_dataset()

    def create_new_model_by_dataset(self):
        train_images, train_labels = self.load_dataset()
        if train_images is None or train_images.size == 0:
            raise ValueError("Cannot create model: dataset not found or invalid.")

        input_shape = train_images.shape[1:]
        print(f"🛠️ Creating new model with input shape {input_shape} ...")

        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Flatten() if len(input_shape) > 1 else tf.keras.layers.Lambda(lambda x: x),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        model.save(self.model_path)
        print(f"✅ New model created and saved at {self.model_path}")
        return model

    def train_model(self):
        print("Training model...")
        train_images, train_labels = self.load_dataset()
        if train_images is None or train_labels is None or train_images.size == 0 or train_labels.size == 0:
            print("❌ ERROR: Dataset is empty or corrupted!")
            return None, None

        if self.model is None:
            print("❌ ERROR: Model not loaded! Cannot train.")
            return None, None

        expected_shape = self.model.input_shape[1:]
        actual_shape = train_images.shape[1:]
        if expected_shape != actual_shape:
            print(f"❌ Shape mismatch: Model expects {expected_shape}, but dataset has {actual_shape}")
            return None, None

        self.model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        history = self.model.fit(train_images, train_labels, epochs=self.epochs, batch_size=32, verbose=1)

        accuracy = history.history.get("accuracy", [None])[-1]
        self.latest_accuracy = accuracy

        if accuracy is None:
            print("❌ ERROR: Accuracy not found in training history!")
            return None, None

        return self.model, accuracy

    def encrypt_weights(self, model):
        print("Encrypting model weights...")
        weights = model.get_weights()
        encrypted_weights = []
        for layer in weights:
            flat = layer.flatten()
            enc = [self.public_key.encrypt(float(x)) for x in flat]
            encrypted_weights.append(enc)
        shapes = [w.shape for w in weights]
        return encrypted_weights, shapes

    def download_models_and_aggregate(self, model_urls, output_path="aggregated_model.h5"):
        print("⬇️ Downloading models for client-side aggregation...")
        os.makedirs("downloaded_models", exist_ok=True)
        local_paths = []

        for url in model_urls:
            filename = os.path.basename(url)
            path = os.path.join("downloaded_models", filename)
            try:
                with requests.get(url, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    with open(path, "wb") as f:
                        f.write(r.content)
                local_paths.append(path)
                print(f"✅ Downloaded: {url}")
            except Exception as e:
                print(f"❌ Failed to download {url}: {e}")
                return {"status": "error", "message": str(e)}

        if len(local_paths) < 2:
            return {"status": "error", "message": "Need at least 2 models to aggregate."}

        try:
            models = [tf.keras.models.load_model(p) for p in local_paths]
            aggregated_model = tf.keras.models.clone_model(models[0])
            aggregated_model.set_weights(models[0].get_weights())

            new_weights = []
            for weights in zip(*[m.get_weights() for m in models]):
                new_weights.append(np.mean(weights, axis=0))

            aggregated_model.set_weights(new_weights)
            aggregated_model.save(output_path)
            print(f"✅ Aggregation completed and saved to {output_path}")

            # ✅ ดึง accuracy จาก meta.json
            client_accuracies = []
            for path in local_paths:
                meta_path = path.replace(".h5", ".meta.json")
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, "r") as f:
                            meta = json.load(f)
                            if "accuracy" in meta:
                                client_accuracies.append(float(meta["accuracy"]))
                    except:
                        continue

            if client_accuracies:
                avg_accuracy = float(round(np.mean(client_accuracies), 4))
                self.latest_accuracy = avg_accuracy
                print(f"📊 Avg Client Accuracy: {self.latest_accuracy}")
            else:
                self.latest_accuracy = 0.0
                print("⚠️ Could not retrieve client accuracies")

            # (Optional) ทดสอบ model accuracy กับ validation set
            try:
                (x_val, y_val), _ = tf.keras.datasets.mnist.load_data()
                x_val = x_val.astype("float32") / 255.0
                x_val = np.expand_dims(x_val, -1)
                y_val = y_val.astype("int")

                aggregated_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
                _, acc = aggregated_model.evaluate(x_val, y_val, verbose=0)
                print(f"📊 Aggregated model eval accuracy (optional): {acc}")
            except Exception as e:
                print("⚠️ Accuracy evaluation failed (optional):", str(e))

            # ✅ Upload aggregated model
            with open(output_path, "rb") as f:
                model_binary = f.read()

            files = {
                "model_file": (os.path.basename(output_path), model_binary)
            }
            data = {
                "project_id": self.config.project_id,
                "aggregation_method": "FedAvg",
                "num_clients": len(local_paths),
                "accuracy": self.latest_accuracy
            }

            try:
                upload_url = f"{self.api_url}/save_aggregated_model"
                print("📤 Uploading aggregated model to:", upload_url)
                response = requests.post(upload_url, files=files, data=data)
                print("📄 Server response:", response.text)
            except Exception as e:
                print("❌ Failed to upload aggregated model:", str(e))

            return {"status": "success", "output_path": output_path}

        except Exception as e:
            return {"status": "error", "message": str(e)}



    def upload(self):
        print("📤 Uploading trained model to server...")
        if not os.path.exists(self.model_path):
            print("❌ Model file not found:", self.model_path)
            return

        with open(self.model_path, "rb") as f:
            model_binary = f.read()

        # ตรวจสอบว่ามีไฟล์ meta อยู่คู่กับ model หรือไม่
        meta_path = self.model_path.replace(".h5", ".meta.json")
        meta_file = None
        if os.path.exists(meta_path):
            with open(meta_path, "rb") as f:
                meta_file = ("model_meta", (os.path.basename(meta_path), f.read()))

        files = {
            "model_file": (os.path.basename(self.model_path), model_binary)
        }
        if meta_file:
            files["meta_file"] = meta_file

        data = {
            "project_id": self.config.project_id,
            "client_id": self.config.client_id,
            "company_id": self.config.company_id,
            "is_encrypted": int(self.config.use_encryption),
            "encryption_key": self.encryption_key_name if self.config.use_encryption else "",
        }

        try:
            upload_url = f"{self.api_url}/upload_model"
            print("📡 POST", upload_url)
            response = requests.post(upload_url, files=files, data=data)
            print("📄 Server response:", response.text)
        except Exception as e:
            print("❌ Upload failed:", str(e))


    def aggregate(self):
        print("Downloading model URLs for client-side aggregation...")
        try:
            url = f"{self.api_url}/get_model_urls"
            response = requests.get(url, params={"project_id": self.config.project_id}, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "success":
                return {"status": "error", "message": data.get("message", "Unknown error")}

            model_urls = data.get("model_urls", [])
            if len(model_urls) < 2:
                return {"status": "error", "message": "Not enough models to aggregate"}

            result = self.download_models_and_aggregate(model_urls)
            return result

        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def run(self):
        print("🚀 Starting Federated Learning ...")

        if not os.path.exists(self.dataset_path):
            print(f"❌ Dataset not found at {self.dataset_path}")
            return

        model, accuracy = self.train_model()
        if model is None or accuracy is None:
            print("❌ ERROR: Training failed.")
            return

        print(f"✅ Training complete! Accuracy: {accuracy:.4f}")
        self.upload()
