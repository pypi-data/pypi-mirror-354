from pathlib import Path
from typing import Union, Optional, Dict, List
import math

import hexss
from hexss import json_load
from hexss.image import Image, ImageFont, PILImage
import numpy as np
import cv2


class Classification:
    def __init__(
            self,
            predictions: np.ndarray,
            class_names: Optional[List[str]],
    ):
        self.predictions = predictions
        self.class_names = class_names

        self.idx = int(np.argmax(self.predictions))
        self.name = self.class_names[self.idx]
        self.conf = float(self.predictions[self.idx])

    def expo_preds(self, base: float = math.e) -> np.ndarray:
        """
        Exponentiate predictions by `base` and normalize to sum=1.
        """
        exps = np.power(base, self.predictions.astype(np.float64))
        return exps / exps.sum()

    def softmax_preds(self) -> np.ndarray:
        """
        Standard softmax over predictions.
        """
        z = self.predictions.astype(np.float64)
        e = np.exp(z - np.max(z))
        return e / e.sum()


class Classifier:
    """
    Wraps a Keras model for image classification.
    """

    def __init__(
            self,
            model_path: Union[Path, str],
            json_data: Optional[Dict] = None,
    ):
        model_path = Path(model_path)
        try:
            from keras.models import load_model
        except ImportError:
            hexss.check_packages('tensorflow', auto_install=True)
            from keras.models import load_model  # type: ignore

        self.model = load_model(model_path)
        self._load_metadata(model_path, json_data)

    def _load_metadata(
            self,
            model_path: Path,
            json_data: Optional[Dict]
    ) -> None:
        if json_data is None:
            json_path = model_path.with_suffix('.json')
            json_data = json_load(json_path)

        # Backwards compatibility
        if 'model_class_names' in json_data and 'class_names' not in json_data:
            json_data['class_names'] = json_data.pop('model_class_names')

        # Defaults
        json_data.setdefault('img_size', (180, 180))

        if 'class_names' not in json_data:
            raise ValueError("json_data missing 'class_names'")

        self.class_names: List[str] = json_data['class_names']
        self.img_size: tuple = tuple(json_data['img_size'])

    def _prepare_image(
            self,
            image: Union[Image, PILImage.Image, np.ndarray]
    ) -> np.ndarray:
        """
        Convert input to RGB array resized to `img_size` and batch of 1.
        """
        if isinstance(image, Image):
            arr = image.numpy('RGB')
        elif isinstance(image, PILImage.Image):
            arr = np.array(image.convert('RGB'))
        elif isinstance(image, np.ndarray):
            arr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            raise TypeError(f"Unsupported image type: {type(image)}")

        arr = cv2.resize(arr, self.img_size)
        return np.expand_dims(arr, axis=0)

    def classify(
            self,
            im: Union[Image, PILImage.Image, np.ndarray]
    ) -> Classification:
        """
        Run a forward pass and return a Classification.
        """
        batch = self._prepare_image(im)
        preds = self.model.predict(batch, verbose=0)[0]
        return Classification(
            predictions=preds,
            class_names=self.class_names,
        )


class MultiClassifier:
    """
    Holds multiple Classifier instances and classifies predefined regions.
    """

    def __init__(self, base_path: Union[Path, str]):
        base_path = Path(base_path)
        config = json_load(base_path / 'frames pos.json')
        self.frames = config['frames']

        ############################ for support old data ############################
        for frame in self.frames.values():
            if "xywh" in frame:
                frame["xywhn"] = frame.pop("xywh")
            if "model_used" in frame:
                frame["model"] = frame.pop("model_used")
            if "res_show" in frame:
                frame["resultMapping"] = frame.pop("res_show")
        ###############################################################################

        self.models: Dict[str, Classifier] = {}
        for name in config['models']:
            model_file = base_path / 'model' / f"{name}.h5"
            self.models[name] = Classifier(model_file)

    def classify_all(
            self,
            im: Union[Image, PILImage.Image, np.ndarray]
    ) -> Dict[str, Classification]:
        """
        Crop each normalized frame region and classify.

        Returns a dict mapping frame keys to Classification.
        """
        img = Image(im)
        results: Dict[str, Classification] = {}

        for key, frame in self.frames.items():
            model_name = frame['model']
            crop_im = img.crop(xywhn=frame['xywhn'])
            results[key] = self.models[model_name].classify(crop_im)

        return results
