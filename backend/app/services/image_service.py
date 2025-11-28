import numpy as np
from PIL import Image
import io
from typing import List, Dict, Tuple
from app.services.data_loader import data_loader

# Try importing tensorflow, handle if missing (for lightweight envs)
try:
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    from tensorflow.keras.preprocessing import image as keras_image
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Image recognition will be limited.")

class ImageService:
    def __init__(self):
        self.model = None
        if TF_AVAILABLE:
            try:
                # Load pre-trained MobileNetV2
                self.model = MobileNetV2(weights='imagenet')
                print("MobileNetV2 loaded successfully.")
            except Exception as e:
                print(f"Error loading MobileNetV2: {e}")

    def identify_product(self, image_bytes: bytes) -> Dict:
        if not TF_AVAILABLE or self.model is None:
            return {
                "error": "Image recognition model not available.",
                "identified_item": None,
                "lines": []
            }

        try:
            # Preprocess image
            img = Image.open(io.BytesIO(image_bytes)).resize((224, 224))
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            # Predict
            preds = self.model.predict(img_array)
            decoded = decode_predictions(preds, top=3)[0]
            
            # Get top prediction
            top_item = decoded[0][1] # e.g., 'running_shoe'
            confidence = float(decoded[0][2])

            # Simplify label (remove underscores, etc)
            search_term = top_item.replace('_', ' ')

            # Search in local data
            matching_lines = data_loader.search_products(search_term)
            
            # If no direct match, try splitting words (e.g. "running shoe" -> "shoe")
            if not matching_lines:
                for word in search_term.split():
                    if len(word) > 3: # Avoid small words
                        matching_lines.extend(data_loader.search_products(word))
            
            # Deduplicate
            unique_lines = {line['line_name']: line for line in matching_lines}.values()

            return {
                "identified_item": search_term,
                "confidence": confidence,
                "lines": list(unique_lines)
            }

        except Exception as e:
            print(f"Error identifying image: {e}")
            return {
                "error": str(e),
                "identified_item": None,
                "lines": []
            }

image_service = ImageService()
