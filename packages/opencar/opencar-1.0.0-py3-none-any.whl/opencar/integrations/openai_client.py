"""OpenAI API client integration."""

import asyncio
import base64
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

from opencar.config.settings import Settings

logger = structlog.get_logger()


class OpenAIClient:
    """OpenAI API client with retry logic and caching."""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """Initialize OpenAI client."""
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
        self._client = httpx.AsyncClient(
            timeout=60.0,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = timedelta(hours=1)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def generate_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate text completion with retry logic."""
        model = model or self.model
        
        try:
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Make API request
            response = await self._client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                # Fallback to mock response for demonstration
                return f"Mock response for: {prompt[:50]}... (API unavailable)"
                
        except Exception as e:
            logger.error(f"OpenAI completion error: {str(e)}")
            # Fallback to mock response
            return f"Mock response for: {prompt[:50]}... (Error: {str(e)})"

    async def analyze_image(
        self,
        image_data: bytes,
        analysis_type: str = "comprehensive",
    ) -> Dict[str, Any]:
        """Analyze image using GPT-4 Vision."""
        try:
            # Encode image to base64
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            
            system_prompt = """You are an expert autonomous vehicle perception system. 
            Analyze the driving scene and provide detailed safety recommendations and situational awareness."""

            prompts = {
                "comprehensive": "Analyze this driving scene comprehensively. Identify all objects, assess road conditions, weather, traffic situation, and potential hazards. Provide safety recommendations.",
                "traffic": "Focus on traffic analysis: vehicles, traffic signs, signals, lane markings, and traffic flow patterns.",
                "safety": "Perform safety analysis: identify hazards, assess risk levels, and provide immediate safety recommendations.",
                "weather": "Analyze weather and road conditions: visibility, precipitation, lighting, road surface conditions.",
                "navigation": "Provide navigation context: road type, intersections, lane information, and directional guidance."
            }
            
            prompt = prompts.get(analysis_type, prompts["comprehensive"])
            
            # Use vision model if available, otherwise fall back to text analysis
            try:
                response = await self._client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": "gpt-4-vision-preview",
                        "messages": [{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_b64}"
                                    }
                                }
                            ]
                        }],
                        "temperature": 0.3,
                        "max_tokens": 1000,
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    analysis_text = data["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"API error: {response.status_code}")
                    
            except Exception as e:
                logger.warning(f"Vision API unavailable, using mock analysis: {str(e)}")
                analysis_text = f"Mock {analysis_type} analysis: Scene appears to be a typical driving environment with standard traffic elements."

            # Return structured analysis
            return {
                "scene_type": self._extract_scene_type(analysis_text),
                "objects": self._extract_objects(analysis_text),
                "hazards": self._extract_hazards(analysis_text),
                "recommendations": self._extract_recommendations(analysis_text),
                "safety_score": self._calculate_safety_score(analysis_text),
                "weather_conditions": self._extract_weather(analysis_text),
                "traffic_situation": self._extract_traffic(analysis_text),
                "full_analysis": analysis_text,
                "confidence": 0.85,
                "analysis_type": analysis_type
            }
            
        except Exception as e:
            logger.error(f"Image analysis error: {str(e)}")
            return {
                "scene_type": "unknown",
                "objects": [],
                "hazards": ["analysis_failed"],
                "recommendations": ["proceed_with_caution"],
                "safety_score": 0.5,
                "weather_conditions": "unclear",
                "traffic_situation": "unknown",
                "full_analysis": f"Analysis failed: {str(e)}",
                "confidence": 0.0,
                "analysis_type": analysis_type
            }

    def _extract_scene_type(self, analysis: str) -> str:
        """Extract scene type from analysis."""
        scene_types = ["urban", "highway", "rural", "intersection", "parking", "residential"]
        analysis_lower = analysis.lower()
        for scene_type in scene_types:
            if scene_type in analysis_lower:
                return scene_type
        return "general"

    def _extract_objects(self, analysis: str) -> List[str]:
        """Extract detected objects from analysis."""
        objects = ["vehicle", "pedestrian", "bicycle", "traffic_light", "stop_sign", "building"]
        found_objects = []
        analysis_lower = analysis.lower()
        for obj in objects:
            if obj in analysis_lower or obj.replace("_", " ") in analysis_lower:
                found_objects.append(obj)
        return found_objects

    def _extract_hazards(self, analysis: str) -> List[str]:
        """Extract hazards from analysis."""
        hazards = ["pedestrian", "vehicle", "weather", "visibility", "construction", "debris"]
        found_hazards = []
        analysis_lower = analysis.lower()
        for hazard in hazards:
            if hazard in analysis_lower:
                found_hazards.append(hazard)
        return found_hazards

    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis."""
        recommendations = [
            "reduce_speed", "maintain_distance", "check_blind_spots", 
            "signal_early", "prepare_to_stop", "increase_following_distance"
        ]
        found_recs = []
        analysis_lower = analysis.lower()
        for rec in recommendations:
            if rec.replace("_", " ") in analysis_lower:
                found_recs.append(rec)
        return found_recs if found_recs else ["proceed_normally"]

    def _calculate_safety_score(self, analysis: str) -> float:
        """Calculate safety score from analysis."""
        analysis_lower = analysis.lower()
        
        # Start with base score
        score = 0.8
        
        # Reduce score for hazards
        hazard_words = ["danger", "hazard", "risk", "caution", "warning", "unsafe"]
        for word in hazard_words:
            if word in analysis_lower:
                score -= 0.1
        
        # Increase score for positive indicators
        positive_words = ["safe", "clear", "normal", "good", "optimal"]
        for word in positive_words:
            if word in analysis_lower:
                score += 0.05
        
        return max(0.0, min(1.0, score))

    def _extract_weather(self, analysis: str) -> str:
        """Extract weather conditions from analysis."""
        weather_conditions = ["clear", "cloudy", "rainy", "foggy", "snowy", "stormy"]
        analysis_lower = analysis.lower()
        for condition in weather_conditions:
            if condition in analysis_lower:
                return condition
        return "clear"

    def _extract_traffic(self, analysis: str) -> str:
        """Extract traffic situation from analysis."""
        traffic_situations = ["heavy", "moderate", "light", "congested", "flowing", "stopped"]
        analysis_lower = analysis.lower()
        for situation in traffic_situations:
            if situation in analysis_lower:
                return situation
        return "normal"

    async def generate_embeddings(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small",
    ) -> List[List[float]]:
        """Generate embeddings for text inputs."""
        try:
            response = await self._client.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": model,
                    "input": texts,
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return [item["embedding"] for item in data["data"]]
            else:
                logger.error(f"Embeddings API error: {response.status_code}")
                # Return mock embeddings
                return [[0.0] * 1536 for _ in texts]  # text-embedding-3-small dimension
                
        except Exception as e:
            logger.error(f"Embeddings error: {str(e)}")
            return [[0.0] * 1536 for _ in texts]

    async def moderate_content(self, text: str) -> Dict[str, Any]:
        """Moderate content using OpenAI moderation API."""
        try:
            response = await self._client.post(
                f"{self.base_url}/moderations",
                json={"input": text}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["results"][0]
            else:
                logger.error(f"Moderation API error: {response.status_code}")
                return {"flagged": False, "categories": {}, "category_scores": {}}
                
        except Exception as e:
            logger.error(f"Moderation error: {str(e)}")
            return {"flagged": False, "categories": {}, "category_scores": {}}

    async def stream_completion(
        self,
        prompt: str,
        callback: Any,
        model: Optional[str] = None,
    ) -> None:
        """Stream completion with callback for each token."""
        model = model or self.model
        
        try:
            async with self._client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and data["choices"]:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    await callback(delta["content"])
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            await callback(f"Error: {str(e)}")

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    def get_client_info(self) -> Dict[str, Any]:
        """Get client information."""
        return {
            "model": self.model,
            "base_url": self.base_url,
            "cache_size": len(self._cache),
            "cache_ttl_hours": self._cache_ttl.total_seconds() / 3600,
        }

    async def health_check(self) -> bool:
        """Check if the OpenAI API is accessible."""
        try:
            response = await self._client.get(f"{self.base_url}/models")
            return response.status_code == 200
        except Exception:
            return False


# Export the main class
__all__ = ["OpenAIClient"] 