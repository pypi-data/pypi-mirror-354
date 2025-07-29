import cv2
import yaml
from pathlib import Path
from typing import Any, Dict, Union, Tuple, List
from PIL import Image
import numpy as np
import os
from mmllm_face_refinement.face_detector import YoloFaceDetector
from mmllm_face_refinement.llm_analyzer import GeminiAnalyzer, LlavaAnalyzer

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

    def infer_faces(self, img, preprocess: bool = False, llm_config: dict = None) -> List[Dict[str, Any]]:
        """
        Detect faces and run LLM analysis on each face.
        Args:
            img: np.ndarray (RGB, uint8) if preprocess=False, else raw image or path
            preprocess: whether to preprocess the image (default: False)
            llm_config: dict with LLM config (optional, falls back to self.config)
        Returns:
            List of dicts: [{bbox, confidence, landmarks, llm_results: {llava, gemini, ...}}, ...]
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
        # For each detection, run LLMs
        for det in detections:
            face_result = det.copy()
            face_result['llm_results'] = {}
            # Crop face for LLMs if needed
            # (Assume input is a file path for cropping, else skip cropping)
            image_path = img if isinstance(img, str) else None
            if image_path:
                # Use YOLO crop util
                crop, meta = self.detector.crop_face(image_path, det, padding=0.2, annotate=False)
                crop_path = None
                # Save crop to temp file for LLMs if needed
                temp_dir = '/tmp'
                crop_path = os.path.join(temp_dir, 'llm_face_crop.jpg')
                crop.save(crop_path)
            else:
                crop_path = None
                crop = None
            for llm_name, analyzer in self.llm_analyzers.items():
                try:
                    if crop_path:
                        llm_result = analyzer.analyze(crop_path, meta if image_path else None)
                    else:
                        llm_result = {'error': 'No crop available for LLM'}
                    face_result['llm_results'][llm_name] = llm_result
                except Exception as e:
                    face_result['llm_results'][llm_name] = {'error': str(e)}
            results.append(face_result)
        return results

def infer_faces(img, model, llm_config: dict = None, preprocess: bool = False):
    """
    API-compatible face inference function for external use.
    Args:
        img: np.ndarray (RGB, uint8) if preprocess=False, else raw image or path
        model: Detector instance
        model_config: ignored
        preprocess: whether to preprocess the image (default: False)
        llm_config: dict with LLM config (optional)
    Returns:
        List of dicts: [{bbox, confidence, landmarks, llm_results: {llava, gemini, ...}}, ...]
    """
    if hasattr(model, 'infer_faces'):
        return model.infer_faces(img, preprocess=preprocess, llm_config=llm_config)
    raise ValueError("Model must be an instance of Detector from mmllm_face_refinement.init()") 