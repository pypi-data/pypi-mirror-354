#!/usr/bin/env python3
import os
import logging
import json
from typing import Dict, Any, Optional, Union
from abc import ABC, abstractmethod
from PIL import Image
import requests
from dotenv import load_dotenv

class BaseLLMAnalyzer(ABC):
    """
    Base class for LLM analyzers
    """
    
    def __init__(self, prompt_template: str):
        """
        Initialize base LLM analyzer
        
        Args:
            prompt_template: Template for the prompt to send to the LLM
        """
        self.logger = logging.getLogger(__name__)
        self.prompt_template = prompt_template
    
    @abstractmethod
    def analyze(self, image_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an image with the LLM
        
        Args:
            image_path: Path to the image
            metadata: Metadata about the image and detection
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the response from the LLM
        
        Args:
            response: Raw text response from the LLM
            
        Returns:
            Dictionary with parsed results
        """
        # Mock implementation: this should be overridden by subclasses with more specific parsing
        is_face = "yes" in response.lower() or "face" in response.lower()
        
        return {
            "is_face": is_face,
            "raw_response": response,
            "face_description": response if is_face else None,
            "confidence": 0.9 if is_face else 0.1,  # Mock confidence
            "suggested_adjustments": None
        }


class GeminiAnalyzer(BaseLLMAnalyzer):
    """
    LLM analyzer using Google's Gemini API
    """
    
    def __init__(
        self,
        model: str = "gemini-pro-vision",
        max_tokens: int = 256,
        temperature: float = 0.2,
        prompt_template: Optional[str] = None,
        rate_limit: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Gemini analyzer
        
        Args:
            model: Gemini model name
            max_tokens: Maximum number of tokens in the response
            temperature: Temperature for sampling
            prompt_template: Template for the prompt, if None uses default
            rate_limit: Rate limiting configuration dictionary with 'enabled' and 'delay_seconds'
        """
        if prompt_template is None:
            prompt_template = ("Is there a human face in this image? "
                              "If yes, describe it briefly and suggest if the "
                              "bounding box (shown in red) should be adjusted. "
                              "If it's not a face, explain why.")
        
        super().__init__(prompt_template)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.rate_limit = rate_limit or {"enabled": False, "delay_seconds": 0.5}
        
        # Import and configure Google's Generative AI library
        try:
            import google.generativeai as genai
            from google.oauth2 import service_account
            import os
            
            # Load environment variables from .env file
            load_dotenv()
            
            # Check for API key in environment
            api_key = os.environ.get("GOOGLE_API_KEY")
            if api_key:
                #print(f"Using API key: {api_key}")
                genai.configure(api_key=api_key)
                self.genai = genai
                self.logger.info(f"Initialized Gemini analyzer with model {model}")
            else:
                # Check for service account credentials
                creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
                if creds_path and os.path.exists(creds_path):
                    credentials = service_account.Credentials.from_service_account_file(
                        creds_path,
                        scopes=["https://www.googleapis.com/auth/cloud-platform"]
                    )
                    genai.configure(credentials=credentials)
                    self.genai = genai
                    self.logger.info(f"Initialized Gemini analyzer with service account credentials")
                else:
                    raise ValueError("No API key or service account credentials found for Google Gemini API")
                    
        except ImportError:
            self.logger.error("Failed to import Google Generative AI library. "
                          "Install with: pip install google-generativeai")
            raise
    
    def analyze(self, image_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an image with Gemini
        
        Args:
            image_path: Path to the image
            metadata: Metadata about the image and detection
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Create model
            model = self.genai.GenerativeModel(self.model)
            
            # Create prompt with metadata
            prompt = (f"{self.prompt_template}\n\n"
                     f"Detection confidence: {metadata['confidence']:.2f}\n"
                     f"Original bounding box in image: {metadata['original_bbox']}")
            
            # Generate response
            response = model.generate_content(
                [prompt, image],
                generation_config={
                    "max_output_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
            )
            
            # Extract text from response
            text = response.text
            
            # Parse response
            result = self._parse_gemini_response(text)
            
            # Respect rate limits if configured
            if hasattr(self, 'rate_limit') and self.rate_limit.get('enabled', False):
                import time
                delay = self.rate_limit.get('delay_seconds', 0.5)
                self.logger.info(f"Rate limiting: Sleeping for {delay} seconds between Gemini API requests")
                time.sleep(delay)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing image with Gemini: {e}")
            return {
                "is_face": False,
                "raw_response": f"Error: {str(e)}",
                "face_description": None,
                "confidence": 0.0,
                "suggested_adjustments": None,
                "error": str(e)
            }
    
    def _parse_gemini_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the response from Gemini
        
        Args:
            response: Raw text response from Gemini
            
        Returns:
            Dictionary with parsed results
        """
        response = response.lower()
        
        # Check if it's a face
        is_face = False
        if "yes" in response or "there is a face" in response or "human face" in response:
            is_face = True
        elif "no" in response or "not a face" in response:
            is_face = False
            
        # Extract description (all text after "yes" if it's a face)
        description = None
        if is_face:
            # Try to extract description
            if "yes" in response:
                description = response.split("yes", 1)[1].strip()
            else:
                description = response
                
        # Look for adjustment suggestions
        adjustments = None
        bbox_adjustment = None
        
        if "adjust" in response or "bounding box" in response:
            # Extract the sentences containing adjustment suggestions
            sentences = response.split('.')
            for sentence in sentences:
                if "adjust" in sentence or "bounding box" in sentence:
                    adjustments = sentence.strip()
                    
                    # Try to extract specific adjustment directions
                    directions = []
                    if "up" in sentence or "higher" in sentence or "top" in sentence:
                        directions.append("up")
                    if "down" in sentence or "lower" in sentence or "bottom" in sentence:
                        directions.append("down")
                    if "left" in sentence:
                        directions.append("left")
                    if "right" in sentence:
                        directions.append("right")
                    if "wider" in sentence or "expand" in sentence:
                        directions.append("wider")
                    if "tighter" in sentence or "smaller" in sentence:
                        directions.append("tighter")
                    
                    if directions:
                        bbox_adjustment = {
                            "directions": directions,
                            "suggestion": adjustments
                        }
                    break
        
        # Estimate confidence based on language
        confidence = 0.0
        if is_face:
            if "clearly" in response or "definitely" in response:
                confidence = 0.9
            elif "appears to be" in response or "likely" in response:
                confidence = 0.7
            else:
                confidence = 0.5
        
        return {
            "is_face": is_face,
            "raw_response": response,
            "face_description": description,
            "confidence": confidence,
            "suggested_adjustments": adjustments,
            "bbox_adjustment": bbox_adjustment
        }


class LlavaAnalyzer(BaseLLMAnalyzer):
    """
    LLM analyzer using LLaVA-NeXT OV model
    """
    
    def __init__(
        self,
        model: str = "lmms-lab/llava-onevision-qwen2-0.5b-ov",
        device: str = "cpu",
        prompt_template: Optional[str] = None
    ):
        """
        Initialize LLaVA analyzer
        
        Args:
            model: Model name or path
            device: Device to run inference on ('cpu' or 'cuda')
            prompt_template: Template for the prompt, if None uses default
        """
        if prompt_template is None:
            prompt_template = ("Is there a human face in this image? "
                              "If yes, describe it briefly and suggest if the "
                              "bounding box (shown in red) should be adjusted. "
                              "If it's not a face, explain why.")
        
        super().__init__(prompt_template)
        self.model_name = model
        self.device = device
        
        # Load model and processor
        try:
            from transformers import AutoProcessor, LlavaForConditionalGeneration
            import torch
            
            self.processor = AutoProcessor.from_pretrained(model)
            self.model = LlavaForConditionalGeneration.from_pretrained(
                model,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            self.model.to(device)

            # Patch for missing patch_size in some LLaVA configs
            if not hasattr(self.processor, "patch_size") or self.processor.patch_size is None:
                patch_size = getattr(self.model.config, "patch_size", None)
                if patch_size is None:
                    vision_cfg = getattr(self.model.config, "vision_config", None)
                    if vision_cfg and hasattr(vision_cfg, "patch_size"):
                        patch_size = vision_cfg.patch_size
                    else:
                        patch_size = 14  # Default for LLaVA models
                self.processor.patch_size = patch_size
                self.logger.warning(f"Patched processor.patch_size to {self.processor.patch_size}")
            
            # Set torch parameters for inference
            self.torch = torch
            torch.set_grad_enabled(False)
            
            self.logger.info(f"Initialized LLaVA analyzer with model {model} on {device}")
            
        except ImportError:
            self.logger.error("Failed to import required libraries for LLaVA.")
            self.logger.error("Install with: pip install transformers torch")
            raise
    
    def analyze(self, image_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an image with LLaVA
        
        Args:
            image_path: Path to the image
            metadata: Metadata about the image and detection
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Load image
            image = Image.open(image_path)

            # Ensure image is 224x224 for LLaVA
            image = image.resize((224, 224))
            
            # Create prompt with metadata
            prompt = (f"<image>\n{self.prompt_template}\n\n"
                     f"Detection confidence: {metadata['confidence']:.2f}\n"
                     f"Original bounding box in image: {metadata['original_bbox']}")
            
            # Prepare inputs
            inputs = self.processor(
                text=prompt,
                images=image,
                return_tensors="pt"
            ).to(self.device)

            # Debug: check for tokenizer/model mismatch
            if 'input_ids' in inputs:
                max_token_id = inputs['input_ids'].max().item()
                vocab_size = self.model.get_input_embeddings().weight.shape[0]
                self.logger.info(f"Max token id: {max_token_id}, vocab size: {vocab_size}")
                if max_token_id >= vocab_size:
                    error_msg = f"Token id {max_token_id} out of range for model vocab size {vocab_size}. Tokenizer/model mismatch."
                    self.logger.error(error_msg)
                    return {
                        "is_face": False,
                        "raw_response": error_msg,
                        "face_description": None,
                        "confidence": 0.0,
                        "suggested_adjustments": None,
                        "error": error_msg
                    }
            
            # Generate response
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False
            )
            
            # Decode response
            generated_text = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0].strip()
            
            # Parse response
            result = self._parse_llava_response(generated_text)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing image with LLaVA: {e}")
            import traceback
            traceback.print_exc()
            return {
                "is_face": False,
                "raw_response": f"Error: {str(e)}",
                "face_description": None,
                "confidence": 0.0,
                "suggested_adjustments": None,
                "error": str(e)
            }
    
    def _parse_llava_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the response from LLaVA
        
        Args:
            response: Raw text response from LLaVA
            
        Returns:
            Dictionary with parsed results
        """
        response = response.lower()
        
        # Check if it's a face
        is_face = False
        if "yes" in response or "there is a face" in response or "human face" in response:
            is_face = True
        elif "no" in response or "not a face" in response:
            is_face = False
            
        # Extract description (all text after "yes" if it's a face)
        description = None
        if is_face:
            # Try to extract description
            if "yes" in response:
                description = response.split("yes", 1)[1].strip()
            else:
                description = response
                
        # Look for adjustment suggestions
        adjustments = None
        bbox_adjustment = None
        
        if "adjust" in response or "bounding box" in response:
            # Extract the sentences containing adjustment suggestions
            sentences = response.split('.')
            for sentence in sentences:
                if "adjust" in sentence or "bounding box" in sentence:
                    adjustments = sentence.strip()
                    
                    # Try to extract specific adjustment directions
                    directions = []
                    if "up" in sentence or "higher" in sentence or "top" in sentence:
                        directions.append("up")
                    if "down" in sentence or "lower" in sentence or "bottom" in sentence:
                        directions.append("down")
                    if "left" in sentence:
                        directions.append("left")
                    if "right" in sentence:
                        directions.append("right")
                    if "wider" in sentence or "expand" in sentence:
                        directions.append("wider")
                    if "tighter" in sentence or "smaller" in sentence:
                        directions.append("tighter")
                    
                    if directions:
                        bbox_adjustment = {
                            "directions": directions,
                            "suggestion": adjustments
                        }
                    break
        
        # Estimate confidence based on language
        confidence = 0.0
        if is_face:
            if "clearly" in response or "definitely" in response:
                confidence = 0.9
            elif "appears to be" in response or "likely" in response:
                confidence = 0.7
            else:
                confidence = 0.5
        
        return {
            "is_face": is_face,
            "raw_response": response,
            "face_description": description,
            "confidence": confidence,
            "suggested_adjustments": adjustments,
            "bbox_adjustment": bbox_adjustment
        }


# For testing purposes
def test_gemini_analyzer():
    """
    Test the Gemini analyzer with a sample image
    """
    import matplotlib.pyplot as plt
    
    # Create an analyzer
    analyzer = GeminiAnalyzer()
    
    # Sample image path
    image_path = "temp/test_face_crop.jpg"
    
    # Mock metadata
    metadata = {
        "original_image": "sample.jpg",
        "original_image_size": (1280, 720),
        "original_bbox": [100, 100, 300, 300],
        "padded_bbox": [80, 80, 320, 320],
        "bbox_in_crop": [20, 20, 220, 220],
        "confidence": 0.85,
        "landmarks": None
    }
    
    # Analyze image
    result = analyzer.analyze(image_path, metadata)
    
    # Display results
    print("Gemini Analysis Results:")
    print(f"Is face: {result['is_face']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Description: {result['face_description']}")
    print(f"Suggested adjustments: {result['suggested_adjustments']}")
    print(f"Raw response: {result['raw_response']}")


def test_llava_analyzer():
    """
    Test the LLaVA analyzer with a sample image
    """
    import matplotlib.pyplot as plt
    
    # Create an analyzer
    analyzer = LlavaAnalyzer()
    
    # Sample image path
    image_path = "temp/test_face_crop.jpg"
    
    # Mock metadata
    metadata = {
        "original_image": "sample.jpg",
        "original_image_size": (1280, 720),
        "original_bbox": [100, 100, 300, 300],
        "padded_bbox": [80, 80, 320, 320],
        "bbox_in_crop": [20, 20, 220, 220],
        "confidence": 0.85,
        "landmarks": None
    }
    
    # Analyze image
    result = analyzer.analyze(image_path, metadata)
    
    # Display results
    print("LLaVA Analysis Results:")
    print(f"Is face: {result['is_face']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Description: {result['face_description']}")
    print(f"Suggested adjustments: {result['suggested_adjustments']}")
    print(f"Raw response: {result['raw_response']}")


if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Test the analyzers
    # Uncomment to test
    # test_gemini_analyzer()
    # test_llava_analyzer() 