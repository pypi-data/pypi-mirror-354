import cv2
import yaml
from pathlib import Path
from typing import Any, Dict, Union, Tuple, List
from PIL import Image
import numpy as np
import os
from mmllm_face_refinement.face_detector import YoloFaceDetector
from mmllm_face_refinement.llm_analyzer import GeminiAnalyzer, LlavaAnalyzer
import tempfile

__all__ = ['Detector', 'infer_faces', 'preprocess_frame']

def preprocess_frame(img: Union[np.ndarray, str]) -> np.ndarray:
    """
    Preprocess an image for face detection and return a uint8 RGB numpy array.
    Args:
        img: np.ndarray (BGR or RGB) or image path
    Returns:
        blob: np.ndarray (RGB, uint8)
    """
    if isinstance(img, str):
        img = cv2.imread(img)
        if img is None:
            raise FileNotFoundError(f"Image file not found or unreadable: {img}")
    if not isinstance(img, np.ndarray):
        raise ValueError("Input must be a numpy array or image path")
    if img.shape[-1] != 3:
        raise ValueError("Input image must have 3 channels (BGR or RGB)")
    # Convert BGR to RGB if needed
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

class Detector:
    def __init__(self, model_paths: dict = None, config_path: str = None):
        if config_path is None:
            config_path = str(Path(__file__).parent.parent / 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        # Optionally override model paths
        if model_paths:
            self.config['yolo']['model_path'] = model_paths.get('yolo', self.config['yolo']['model_path'])
        self.detector = YoloFaceDetector(
            model_path=self.config['yolo'].get('model_path'),
            confidence_threshold=self.config['yolo']['confidence_threshold'],
            iou_threshold=self.config['yolo']['iou_threshold'],
            device=self.config['yolo']['device']
        )
        # LLM analyzers (lazy init)
        self.llm_analyzers = None

    def infer_faces_yolo(self, img, preprocess: bool = False) -> List[Dict[str, Any]]:
        """
        Internal: Detect faces in an image using YOLO face detector.
        Args:
            img: np.ndarray (RGB, uint8) if preprocess=False, else raw image or path
            preprocess: whether to preprocess the image (default: False)
        Returns:
            detections: list of detection dicts (with bbox, confidence, etc)
        """
        if preprocess:
            blob = preprocess_frame(img)
        else:
            blob = img
            if not (isinstance(blob, np.ndarray) and blob.dtype == np.uint8 and blob.shape[-1] == 3):
                raise ValueError("When preprocess=False, img must be a uint8 RGB numpy array (blob)")
        detections = self.detector.detect(blob)
        return detections

    def infer_faces(self, img, preprocess: bool = False, llm_config: dict = None, full_output: bool = False):
        """
        Detect faces and run LLM analysis on each face. Only include faces accepted by at least one LLM (is_face==True).
        Args:
            img: np.ndarray (RGB, uint8) if preprocess=False, else raw image or path
            preprocess: whether to preprocess the image (default: False)
            llm_config: dict with LLM config (optional)
            full_output: if True, include all LLM results in output
        Returns:
            List of [x, y, w, h] (int) or [x, y, w, h, llm_results] if full_output
        """
        detections = self.infer_faces_yolo(img, preprocess=preprocess)
        results = []
        if llm_config is None:
            llm_config = self.config.get('llm', {})
        # Lazy init analyzers
        if self.llm_analyzers is None:
            self.llm_analyzers = {}
            if llm_config.get('gemini', {}).get('enabled', False):
                self.llm_analyzers['gemini'] = GeminiAnalyzer(
                    model=llm_config['gemini']['model'],
                    max_tokens=llm_config['gemini']['max_tokens'],
                    temperature=llm_config['gemini']['temperature'],
                    prompt_template=llm_config['gemini']['prompt_template']
                )
            if llm_config.get('llava', {}).get('enabled', False):
                self.llm_analyzers['llava'] = LlavaAnalyzer(
                    model=llm_config['llava']['model'],
                    device=llm_config['llava']['device'],
                    prompt_template=llm_config['llava']['prompt_template']
                )
        for det in detections:
            x1, y1, x2, y2 = None, None, None, None
            if isinstance(det, dict) and 'bbox' in det:
                x1, y1, x2, y2 = map(int, det['bbox'])
            elif isinstance(det, (list, tuple)) and len(det) >= 4:
                x1, y1, x2, y2 = map(int, det[:4])
            else:
                continue  # skip invalid detection
            w = x2 - x1
            h = y2 - y1
            llm_results = {}
            accepted = False
            for llm_name, analyzer in self.llm_analyzers.items():
                try:
                    if isinstance(img, str):
                        crop, meta = self.detector.crop_face(img, det, padding=0.2, annotate=False)
                    elif isinstance(img, np.ndarray):
                        crop_arr = img[y1:y2, x1:x2, :]
                        crop = Image.fromarray(crop_arr)
                        meta = {'original_bbox': [x1, y1, x2, y2], 'confidence': det['confidence'], 'landmarks': det['landmarks']}
                    else:
                        llm_results[llm_name] = {'error': 'Unsupported image type for cropping'}
                        continue
                    # Save crop to a temp file
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmpfile:
                        crop_path = tmpfile.name
                        crop.save(crop_path)
                    llm_result = analyzer.analyze(crop_path, meta)
                    llm_results[llm_name] = llm_result
                    if llm_result.get('is_face', False):
                        accepted = True
                except Exception as e:
                    llm_results[llm_name] = {'error': str(e)}
            if accepted:
                if full_output:
                    results.append([x1, y1, w, h, llm_results])
                else:
                    results.append([x1, y1, w, h])
        return results

def infer_faces(img, model, llm_config: dict = None, preprocess: bool = False, full_output: bool = False):
    """
    API-compatible face inference function for external use.
    Args:
        img: np.ndarray (RGB, uint8) if preprocess=False, else raw image or path
        model: Detector instance
        model_config: ignored
        preprocess: whether to preprocess the image (default: False)
        llm_config: dict with LLM config (optional)
        full_output: if True, include all LLM results in output
    Returns:
        List of [x, y, w, h] (int) or [x, y, w, h, llm_results] if full_output
    """
    if hasattr(model, 'infer_faces'):
        return model.infer_faces(img, preprocess=preprocess, llm_config=llm_config, full_output=full_output)
    raise ValueError("Model must be an instance of Detector from mmllm_face_refinement.init()") 