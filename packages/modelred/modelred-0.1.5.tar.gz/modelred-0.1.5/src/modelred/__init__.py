import asyncio
import aiohttp
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List, Union


# Enums
class ModelProvider(Enum):
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"
    HUGGINGFACE = "HUGGINGFACE"
    SAGEMAKER = "SAGEMAKER"
    BEDROCK = "BEDROCK"


class AssessmentStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Data classes
@dataclass
class AssessmentResult:
    assessment_id: str
    model_id: str
    status: AssessmentStatus
    overall_score: float
    risk_level: RiskLevel
    total_tests: int
    passed_tests: int
    failed_tests: int
    categories: Dict[str, Any]
    recommendations: List[str]
    started_at: datetime
    completed_at: Optional[datetime] = None


@dataclass
class UsageStats:
    models_registered: int
    models_limit: int
    assessments_this_month: int
    assessments_limit: int
    tier: str
    next_reset_date: str


# Exceptions
class ModelRedError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(ModelRedError):
    pass


class QuotaExceededError(ModelRedError):
    pass


class ModelNotFoundError(ModelRedError):
    pass


class ValidationError(ModelRedError):
    pass


# Main client
class ModelRed:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MODELRED_API_KEY")
        if not self.api_key:
            raise ValidationError("API key required")

        if not self.api_key.startswith("mr_"):
            raise ValidationError("Invalid API key format")

        self.base_url = os.getenv("MODELRED_API_URL", "http://localhost:3000")
        self.logger = logging.getLogger("modelred")
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        if not self.session:
            raise RuntimeError("Client not initialized")

        url = f"{self.base_url}/api/modelred{endpoint}"

        async with self.session.request(method, url, **kwargs) as response:
            try:
                response_data = await response.json()
            except:
                response_data = {"error": await response.text()}

            # Handle errors - NO FALLBACKS
            if response.status == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status == 403:
                raise QuotaExceededError(response_data.get("message", "Quota exceeded"))
            elif response.status == 404:
                raise ModelNotFoundError(response_data.get("message", "Not found"))
            elif response.status >= 400:
                raise ModelRedError(
                    f"API error: {response_data.get('message', 'Unknown error')}"
                )

            return response_data

    async def validate_api_key(self) -> Dict[str, Any]:
        return await self._make_request("GET", "/auth/validate")

    async def get_usage_stats(self) -> UsageStats:
        data = await self._make_request("GET", "/account/usage")
        return UsageStats(**data)

    async def register_model(
        self,
        model_id: str,
        provider: Union[str, ModelProvider],
        model_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_region: Optional[str] = None,
        endpoint_name: Optional[str] = None,
        bedrock_model_id: Optional[str] = None,
    ) -> bool:
        # Validation
        if not model_id.strip():
            raise ValidationError("Model ID cannot be empty")

        if isinstance(provider, str):
            provider = ModelProvider(provider.upper())

        # Build config based on provider
        provider_config = {}

        if provider == ModelProvider.OPENAI:
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValidationError("OpenAI API key required")
            provider_config = {
                "api_key": api_key,
                "model_name": model_name or "gpt-3.5-turbo",
            }

        elif provider == ModelProvider.ANTHROPIC:
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValidationError("Anthropic API key required")
            provider_config = {
                "api_key": api_key,
                "model_name": model_name or "claude-3-sonnet",
            }

        # Add other providers as needed...

        payload = {
            "model_id": model_id,
            "provider": provider.value,
            "model_name": model_name,
            "provider_config": provider_config,
            "metadata": metadata or {},
        }

        # Let exceptions bubble up - NO CATCHING
        response = await self._make_request("POST", "/models", json=payload)
        return response.get("success", True)

    async def list_models(self) -> List[Dict[str, Any]]:
        response = await self._make_request("GET", "/models")
        return response.get("models", [])

    async def delete_model(self, model_id: str) -> bool:
        response = await self._make_request("DELETE", f"/models/{model_id}")
        return response.get("success", True)

    async def run_assessment(
        self,
        model_id: str,
        test_types: Optional[List[str]] = None,
        priority: str = "normal",
        wait_for_completion: bool = True,
        timeout_minutes: int = 30,
    ) -> AssessmentResult:
        if not test_types:
            test_types = ["prompt_injection", "jailbreak", "toxicity"]

        payload = {"model_id": model_id, "test_types": test_types, "priority": priority}

        response = await self._make_request("POST", "/assessments", json=payload)
        assessment_id = response["assessment_id"]

        if not wait_for_completion:
            return AssessmentResult(
                assessment_id=assessment_id,
                model_id=model_id,
                status=AssessmentStatus.QUEUED,
                overall_score=0.0,
                risk_level=RiskLevel.LOW,
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                categories={},
                recommendations=[],
                started_at=datetime.now(),
            )

        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < timeout_minutes * 60:
            status_response = await self._make_request(
                "GET", f"/assessments/{assessment_id}"
            )
            status = AssessmentStatus(status_response["status"])

            if status == AssessmentStatus.COMPLETED:
                return await self.get_assessment_results(assessment_id)
            elif status == AssessmentStatus.FAILED:
                raise ModelRedError(
                    f"Assessment failed: {status_response.get('error_message')}"
                )

            await asyncio.sleep(10)

        raise ModelRedError("Assessment timeout")

    async def get_assessment_results(self, assessment_id: str) -> AssessmentResult:
        data = await self._make_request("GET", f"/assessments/{assessment_id}/results")

        return AssessmentResult(
            assessment_id=data["assessment_id"],
            model_id=data["model_id"],
            status=AssessmentStatus(data["status"]),
            overall_score=data["overall_score"],
            risk_level=RiskLevel(data["risk_level"]),
            total_tests=data["total_tests"],
            passed_tests=data["passed_tests"],
            failed_tests=data["failed_tests"],
            categories=data["categories"],
            recommendations=data["recommendations"],
            started_at=datetime.fromisoformat(
                data["started_at"].replace("Z", "+00:00")
            ),
            completed_at=(
                datetime.fromisoformat(data["completed_at"].replace("Z", "+00:00"))
                if data.get("completed_at")
                else None
            ),
        )
