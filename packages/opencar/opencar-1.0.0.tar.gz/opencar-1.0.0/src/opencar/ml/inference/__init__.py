"""ML inference module for OpenCar."""

import asyncio
import time
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
import numpy as np
import torch
import structlog

logger = structlog.get_logger()


class InferenceEngine:
    """High-performance inference engine for ML models."""

    def __init__(
        self,
        model_path: Optional[Path] = None,
        device: str = "cpu",
        batch_size: int = 1,
        use_tensorrt: bool = False,
        use_onnx: bool = False,
    ):
        """Initialize inference engine."""
        self.model_path = model_path
        self.device = device
        self.batch_size = batch_size
        self.use_tensorrt = use_tensorrt
        self.use_onnx = use_onnx
        
        self.model = None
        self.is_loaded = False
        self.input_shape = None
        self.output_shape = None
        
        # Performance tracking
        self.inference_times = []
        self.total_inferences = 0

    async def load_model(self) -> None:
        """Load model for inference."""
        if self.is_loaded:
            return
            
        try:
            logger.info(f"Loading model from {self.model_path}")
            
            # Simulate model loading
            await asyncio.sleep(0.1)
            
            # Mock model for demonstration
            self.model = {
                "type": "mock_model",
                "device": self.device,
                "batch_size": self.batch_size,
                "loaded_at": time.time()
            }
            
            self.input_shape = (3, 640, 640)  # CHW format
            self.output_shape = (85, 8400)    # YOLO output format
            self.is_loaded = True
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    async def predict(
        self,
        inputs: Union[np.ndarray, torch.Tensor, List[np.ndarray]],
        return_raw: bool = False,
    ) -> Dict[str, Any]:
        """Run inference on inputs."""
        if not self.is_loaded:
            await self.load_model()
            
        start_time = time.time()
        
        try:
            # Preprocess inputs
            processed_inputs = self._preprocess(inputs)
            
            # Run inference (mock implementation)
            outputs = await self._run_inference(processed_inputs)
            
            # Postprocess outputs
            if return_raw:
                results = {"raw_outputs": outputs}
            else:
                results = self._postprocess(outputs)
            
            # Track performance
            inference_time = (time.time() - start_time) * 1000
            self.inference_times.append(inference_time)
            self.total_inferences += 1
            
            # Keep only last 1000 times
            if len(self.inference_times) > 1000:
                self.inference_times = self.inference_times[-1000:]
            
            results["inference_time_ms"] = inference_time
            
            return results
            
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            raise

    def _preprocess(self, inputs: Union[np.ndarray, torch.Tensor, List[np.ndarray]]) -> np.ndarray:
        """Preprocess inputs for inference."""
        if isinstance(inputs, list):
            # Batch processing
            batch = np.stack([self._normalize_input(inp) for inp in inputs])
        else:
            batch = np.expand_dims(self._normalize_input(inputs), axis=0)
            
        return batch

    def _normalize_input(self, input_data: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """Normalize single input."""
        if isinstance(input_data, torch.Tensor):
            input_data = input_data.numpy()
            
        # Ensure correct shape and type
        if input_data.dtype != np.float32:
            input_data = input_data.astype(np.float32)
            
        # Normalize to [0, 1] if needed
        if input_data.max() > 1.0:
            input_data = input_data / 255.0
            
        return input_data

    async def _run_inference(self, inputs: np.ndarray) -> np.ndarray:
        """Run actual inference (mock implementation)."""
        # Simulate inference time
        await asyncio.sleep(0.01)
        
        batch_size = inputs.shape[0]
        
        # Mock YOLO-style output
        # Shape: (batch_size, 85, 8400) where 85 = 4 (bbox) + 1 (conf) + 80 (classes)
        mock_output = np.random.rand(batch_size, 85, 8400).astype(np.float32)
        
        # Make some detections more confident
        mock_output[:, 4, :100] = np.random.uniform(0.7, 0.95, (batch_size, 100))  # High confidence
        mock_output[:, 4, 100:] = np.random.uniform(0.0, 0.3, (batch_size, 8300))  # Low confidence
        
        return mock_output

    def _postprocess(self, outputs: np.ndarray) -> Dict[str, Any]:
        """Postprocess inference outputs."""
        batch_size = outputs.shape[0]
        all_detections = []
        
        for i in range(batch_size):
            detections = self._extract_detections(outputs[i])
            all_detections.append(detections)
        
        return {
            "detections": all_detections,
            "batch_size": batch_size,
            "num_detections": [len(dets) for dets in all_detections]
        }

    def _extract_detections(self, output: np.ndarray, conf_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Extract detections from model output."""
        # output shape: (85, 8400)
        confidences = output[4, :]  # Objectness scores
        
        # Filter by confidence
        valid_indices = confidences > conf_threshold
        
        if not np.any(valid_indices):
            return []
        
        # Extract valid detections
        valid_boxes = output[:4, valid_indices].T  # (N, 4)
        valid_confs = confidences[valid_indices]
        valid_classes = output[5:, valid_indices].T  # (N, 80)
        
        detections = []
        for i in range(len(valid_confs)):
            # Get class with highest probability
            class_probs = valid_classes[i]
            class_id = np.argmax(class_probs)
            class_conf = class_probs[class_id]
            
            # Combined confidence
            final_conf = valid_confs[i] * class_conf
            
            if final_conf > conf_threshold:
                # Convert from center format to corner format
                x_center, y_center, width, height = valid_boxes[i]
                x1 = x_center - width / 2
                y1 = y_center - height / 2
                x2 = x_center + width / 2
                y2 = y_center + height / 2
                
                detections.append({
                    "class_name": self._get_class_name(class_id),
                    "confidence": float(final_conf),
                    "bbox": {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2)
                    },
                    "attributes": {}
                })
        
        return detections

    def _get_class_name(self, class_id: int) -> str:
        """Get class name from ID."""
        # COCO class names
        coco_classes = [
            "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
            "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
            "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
            "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
            "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
            "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
            "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop",
            "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
            "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
        ]
        
        if class_id < len(coco_classes):
            return coco_classes[class_id]
        return f"class_{class_id}"

    async def batch_predict(
        self,
        inputs_list: List[Union[np.ndarray, torch.Tensor]],
        batch_size: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Run batch inference on multiple inputs."""
        if not self.is_loaded:
            await self.load_model()
            
        batch_size = batch_size or self.batch_size
        results = []
        
        # Process in batches
        for i in range(0, len(inputs_list), batch_size):
            batch = inputs_list[i:i + batch_size]
            batch_results = await self.predict(batch)
            
            # Split batch results back to individual results
            for j, detections in enumerate(batch_results["detections"]):
                results.append({
                    "detections": detections,
                    "inference_time_ms": batch_results["inference_time_ms"] / len(batch),
                    "batch_index": i + j
                })
        
        return results

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self.inference_times:
            return {"error": "No inference data available"}
        
        times = self.inference_times
        return {
            "total_inferences": self.total_inferences,
            "average_time_ms": np.mean(times),
            "median_time_ms": np.median(times),
            "min_time_ms": np.min(times),
            "max_time_ms": np.max(times),
            "std_time_ms": np.std(times),
            "p95_time_ms": np.percentile(times, 95),
            "p99_time_ms": np.percentile(times, 99),
            "throughput_fps": 1000.0 / np.mean(times) if np.mean(times) > 0 else 0,
        }

    async def warmup(self, num_iterations: int = 10) -> None:
        """Warm up the model with dummy inputs."""
        if not self.is_loaded:
            await self.load_model()
            
        logger.info(f"Warming up model with {num_iterations} iterations...")
        
        # Create dummy input
        dummy_input = np.random.rand(*self.input_shape).astype(np.float32)
        
        for i in range(num_iterations):
            await self.predict(dummy_input)
            
        logger.info("Model warmup completed")

    async def unload_model(self) -> None:
        """Unload model from memory."""
        if self.is_loaded:
            self.model = None
            self.is_loaded = False
            logger.info("Model unloaded from memory")

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            "model_path": str(self.model_path) if self.model_path else None,
            "device": self.device,
            "batch_size": self.batch_size,
            "is_loaded": self.is_loaded,
            "input_shape": self.input_shape,
            "output_shape": self.output_shape,
            "use_tensorrt": self.use_tensorrt,
            "use_onnx": self.use_onnx,
            "total_inferences": self.total_inferences,
        }


# Export the main class
__all__ = ["InferenceEngine"]
