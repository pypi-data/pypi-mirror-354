import urllib.request
from pathlib import Path
import onnxruntime as ort
import numpy as np


class ImageSimilarityONNX:
    def __init__(self):
        model = "mobilenetv2-12"
        # model = "mobilenetv2-7"
        self.model_path = (
            Path.home() / ".cache" / "condenser_models" / f"{model}.onnx"
        )
        self.model_url = f"https://github.com/onnx/models/raw/refs/heads/main/validated/vision/classification/mobilenet/model/{model}.onnx"

        self._ensure_model()
        self.session = ort.InferenceSession(
            str(self.model_path), providers=["CPUExecutionProvider"]
        )
        self.input_name = self.session.get_inputs()[0].name

    def _ensure_model(self):
        if not self.model_path.exists():
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Downloading MobileNetV2 model to {self.model_path}...")
            urllib.request.urlretrieve(self.model_url, self.model_path)
            print("Download complete.")

    def _preprocess(self, img: np.ndarray):
        img = img.resize((224, 224))
        img = np.array(img).astype(np.float32)
        img = img / 127.5 - 1.0  # Scale to [-1, 1]
        img = np.transpose(img, (2, 0, 1))  # Channels first
        return img[None, ...]

    def _embed(self, img: np.ndarray):
        x = self._preprocess(img)
        emb = self.session.run(None, {self.input_name: x})[0].squeeze()
        norm = np.linalg.norm(emb)
        return emb / norm if norm > 0 else emb

    def __call__(self, img) -> np.ndarray:
        return self._embed(img)


onnx_model = ImageSimilarityONNX()
