# ModelRed SDK - Complete Implementation for Backend Worker Integration
# pip install modelred

import asyncio
import aiohttp
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List, Union

# =============================================================================
# TYPES AND ENUMS
# =============================================================================


class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    SAGEMAKER = "sagemaker"
    BEDROCK = "bedrock"


class AssessmentStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# =============================================================================
# DATA MODELS
# =============================================================================


@dataclass
class ModelConfig:
    model_id: str
    provider: ModelProvider
    model_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


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
    error_message: Optional[str] = None
    test_types: Optional[List[str]] = None
    probes_used: Optional[List[str]] = None
    raw_results: Optional[List[Dict[str, Any]]] = None


@dataclass
class UsageStats:
    models_registered: int
    models_limit: int
    assessments_this_month: int
    assessments_limit: int
    tier: str
    next_reset_date: str


# =============================================================================
# EXCEPTIONS
# =============================================================================


class ModelRedError(Exception):
    """Base exception for ModelRed SDK"""

    pass


class AuthenticationError(ModelRedError):
    """Invalid API key"""

    pass


class QuotaExceededError(ModelRedError):
    """Usage quota exceeded"""

    pass


class ModelNotFoundError(ModelRedError):
    """Model not registered"""

    pass


class AssessmentError(ModelRedError):
    """Assessment execution error"""

    pass


class ValidationError(ModelRedError):
    """Invalid parameters"""

    pass


# =============================================================================
# API CLIENT (Next.js Routes)
# =============================================================================


class ModelRedAPIClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:3000"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None

        if not api_key.startswith("mr_"):
            raise ValidationError("Invalid API key format")

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120),
            headers={"User-Agent": "ModelRed-SDK/1.0.0"},
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        # Call Next.js API routes instead of direct backend
        url = f"{self.base_url}/api{endpoint}"
        headers = self._get_headers()

        async with self.session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            try:
                response_data = await response.json()
            except:
                response_data = {"error": await response.text()}

            if response.status == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status == 403:
                raise QuotaExceededError(response_data.get("error", "Quota exceeded"))
            elif response.status == 404:
                raise ModelNotFoundError(response_data.get("error", "Not found"))
            elif response.status >= 400:
                raise ModelRedError(
                    f"API error: {response_data.get('error', 'Unknown error')}"
                )

            return response_data

    async def validate_api_key(self) -> Dict[str, Any]:
        return await self._make_request("POST", "/auth/validate")

    async def get_usage_stats(self) -> UsageStats:
        data = await self._make_request("GET", "/account/usage")
        return UsageStats(**data)

    async def register_model(
        self, config: ModelConfig, provider_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        payload = {
            "model_id": config.model_id,
            "provider": config.provider.value,
            "model_name": config.model_name,
            "provider_config": provider_config,
            "metadata": config.metadata or {},
        }
        return await self._make_request("POST", "/models", json=payload)

    async def list_models(self) -> List[Dict[str, Any]]:
        response = await self._make_request("GET", "/models")
        return response.get("models", [])

    async def delete_model(self, model_id: str) -> Dict[str, Any]:
        return await self._make_request("DELETE", f"/models/{model_id}")

    async def start_assessment(
        self, model_id: str, test_types: List[str], priority: str = "normal"
    ) -> Dict[str, Any]:
        payload = {"model_id": model_id, "test_types": test_types, "priority": priority}
        return await self._make_request("POST", "/assessments", json=payload)

    async def get_assessment_status(self, assessment_id: str) -> Dict[str, Any]:
        return await self._make_request("GET", f"/assessments/{assessment_id}")

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
            error_message=data.get("error_message"),
            test_types=data.get("test_types"),
            probes_used=data.get("probes_used"),
            raw_results=data.get("raw_results"),
        )


# =============================================================================
# MAIN CLIENT
# =============================================================================


class ModelRed:
    def __init__(
        self, api_key: Optional[str] = None, base_url: str = "http://localhost:3000"
    ):
        self.api_key = api_key or os.getenv("MODELRED_API_KEY")
        if not self.api_key:
            raise ValidationError(
                "API key required. Set MODELRED_API_KEY or pass api_key parameter"
            )

        self.base_url = base_url
        self.logger = logging.getLogger("modelred")
        self.models: Dict[str, ModelConfig] = {}
        self.account_info: Optional[Dict[str, Any]] = None

    async def _ensure_authenticated(self):
        if self.account_info is None:
            async with ModelRedAPIClient(self.api_key, self.base_url) as client:
                self.account_info = await client.validate_api_key()

    async def register_model(
        self,
        model_id: str,
        provider: Union[str, ModelProvider],
        # Universal parameters
        model_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        # API-based providers (OpenAI, Anthropic, HuggingFace)
        api_key: Optional[str] = None,
        # AWS providers (SageMaker, Bedrock)
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        # SageMaker specific
        endpoint_name: Optional[str] = None,
        # Bedrock specific
        bedrock_model_id: Optional[str] = None,
    ) -> bool:
        """Register a model for testing

        Args:
            model_id: Unique identifier for your model
            provider: Model provider (openai, anthropic, huggingface, sagemaker, bedrock)
            model_name: Optional model name
            metadata: Optional metadata dict

            # For API-based providers (OpenAI, Anthropic, HuggingFace):
            api_key: Provider API key

            # For AWS providers (SageMaker, Bedrock):
            aws_access_key_id: AWS access key
            aws_secret_access_key: AWS secret access key
            aws_session_token: AWS session token (optional)
            aws_region: AWS region (default: us-east-1)

            # For SageMaker:
            endpoint_name: SageMaker endpoint name

            # For Bedrock:
            bedrock_model_id: Bedrock model ID (e.g., anthropic.claude-3-sonnet-20240229-v1:0)

        Examples:
            # OpenAI
            await client.register_model(
                model_id="my-gpt4",
                provider="openai",
                api_key="sk-...",
                model_name="gpt-4"
            )

            # SageMaker
            await client.register_model(
                model_id="my-sagemaker-model",
                provider="sagemaker",
                aws_access_key_id="AKIA...",
                aws_secret_access_key="...",
                aws_region="us-east-1",
                endpoint_name="my-llm-endpoint"
            )

            # Bedrock
            await client.register_model(
                model_id="my-claude-bedrock",
                provider="bedrock",
                aws_access_key_id="AKIA...",
                aws_secret_access_key="...",
                aws_region="us-east-1",
                bedrock_model_id="anthropic.claude-3-sonnet-20240229-v1:0"
            )
        """
        await self._ensure_authenticated()

        # Convert string to enum
        if isinstance(provider, str):
            try:
                provider = ModelProvider(provider.lower())
            except ValueError:
                supported = ", ".join([p.value for p in ModelProvider])
                raise ValidationError(
                    f"Unsupported provider: {provider}. Supported: {supported}"
                )

        # Build provider-specific configuration
        provider_config = {}

        if provider == ModelProvider.OPENAI:
            if not api_key:
                api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValidationError(
                    "OpenAI API key required. Set OPENAI_API_KEY or pass api_key parameter"
                )

            provider_config = {
                "api_key": api_key,
                "model_name": model_name or "gpt-3.5-turbo",
            }

        elif provider == ModelProvider.ANTHROPIC:
            if not api_key:
                api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValidationError(
                    "Anthropic API key required. Set ANTHROPIC_API_KEY or pass api_key parameter"
                )

            provider_config = {
                "api_key": api_key,
                "model_name": model_name or "claude-3-sonnet-20240229",
            }

        elif provider == ModelProvider.HUGGINGFACE:
            if not api_key:
                api_key = os.getenv("HUGGINGFACE_API_TOKEN")

            provider_config = {"api_key": api_key, "model_name": model_name or "gpt2"}

        elif provider == ModelProvider.SAGEMAKER:
            # Get AWS credentials
            if not aws_access_key_id:
                aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            if not aws_secret_access_key:
                aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            if not aws_session_token:
                aws_session_token = os.getenv("AWS_SESSION_TOKEN")
            if not aws_region:
                aws_region = os.getenv("AWS_REGION", "us-east-1")

            if not aws_access_key_id or not aws_secret_access_key:
                raise ValidationError(
                    "AWS credentials required for SageMaker. "
                    "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or pass them as parameters"
                )

            if not endpoint_name:
                raise ValidationError("SageMaker endpoint_name required")

            provider_config = {
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "aws_session_token": aws_session_token,
                "region": aws_region,
                "endpoint_name": endpoint_name,
                "model_name": model_name,
            }

        elif provider == ModelProvider.BEDROCK:
            # Get AWS credentials
            if not aws_access_key_id:
                aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            if not aws_secret_access_key:
                aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            if not aws_session_token:
                aws_session_token = os.getenv("AWS_SESSION_TOKEN")
            if not aws_region:
                aws_region = os.getenv("AWS_REGION", "us-east-1")

            if not aws_access_key_id or not aws_secret_access_key:
                raise ValidationError(
                    "AWS credentials required for Bedrock. "
                    "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or pass them as parameters"
                )

            if not bedrock_model_id:
                raise ValidationError(
                    "Bedrock bedrock_model_id required (e.g., anthropic.claude-3-sonnet-20240229-v1:0)"
                )

            provider_config = {
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "aws_session_token": aws_session_token,
                "region": aws_region,
                "model_id": bedrock_model_id,
                "model_name": model_name or bedrock_model_id,
            }

        else:
            raise ValidationError(f"Unsupported provider: {provider}")

        # Create model config
        config = ModelConfig(
            model_id=model_id,
            provider=provider,
            model_name=model_name,
            metadata=metadata,
        )

        try:
            async with ModelRedAPIClient(self.api_key, self.base_url) as client:
                await client.register_model(config, provider_config)

            self.models[model_id] = config
            self.logger.info(f"Registered model: {model_id} ({provider.value})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register model {model_id}: {e}")
            raise

    async def run_assessment(
        self,
        model_id: str,
        test_types: Optional[List[str]] = None,
        priority: str = "normal",
        wait_for_completion: bool = True,
        timeout_minutes: int = 30,
    ) -> AssessmentResult:
        """Run security assessment on a model

        Args:
            model_id: Model to assess
            test_types: List of test types (prompt_injection, jailbreak, toxicity, bias, hallucination, data_leakage)
            priority: Assessment priority (low, normal, high, critical)
            wait_for_completion: Whether to wait for completion
            timeout_minutes: Timeout for waiting

        Returns:
            AssessmentResult with detailed findings
        """
        await self._ensure_authenticated()

        if model_id not in self.models:
            raise ModelNotFoundError(
                f"Model '{model_id}' not registered. Use register_model() first."
            )

        if test_types is None:
            # Default test types - backend will determine available tests based on tier
            test_types = ["prompt_injection", "jailbreak", "toxicity"]

        async with ModelRedAPIClient(self.api_key, self.base_url) as client:
            # Start assessment
            response = await client.start_assessment(model_id, test_types, priority)
            assessment_id = response["assessment_id"]

            self.logger.info(f"Started assessment: {assessment_id}")

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
                    started_at=datetime.utcnow(),
                    test_types=test_types,
                )

            # Wait for completion with progress updates
            start_time = time.time()
            timeout_seconds = timeout_minutes * 60
            last_progress = 0

            while time.time() - start_time < timeout_seconds:
                try:
                    status_response = await client.get_assessment_status(assessment_id)
                    status = AssessmentStatus(status_response["status"])

                    # Log progress updates
                    if (
                        "progress" in status_response
                        and status_response["progress"] != last_progress
                    ):
                        last_progress = status_response["progress"]
                        self.logger.info(f"Assessment progress: {last_progress}%")

                    if status == AssessmentStatus.COMPLETED:
                        self.logger.info("Assessment completed, fetching results...")
                        return await client.get_assessment_results(assessment_id)

                    elif status == AssessmentStatus.FAILED:
                        error_msg = status_response.get("error", "Unknown error")
                        raise AssessmentError(f"Assessment failed: {error_msg}")

                    elif status == AssessmentStatus.CANCELLED:
                        raise AssessmentError("Assessment was cancelled")

                    # Wait before next check
                    await asyncio.sleep(10)

                except ModelRedError:
                    # Re-raise ModelRed errors
                    raise
                except Exception as e:
                    # Handle transient errors
                    self.logger.warning(f"Status check failed (retrying): {e}")
                    await asyncio.sleep(5)

            raise AssessmentError(f"Assessment timeout after {timeout_minutes} minutes")

    async def get_assessment_status(self, assessment_id: str) -> Dict[str, Any]:
        """Get real-time assessment status"""
        async with ModelRedAPIClient(self.api_key, self.base_url) as client:
            return await client.get_assessment_status(assessment_id)

    async def get_assessment_results(self, assessment_id: str) -> AssessmentResult:
        """Get detailed assessment results"""
        async with ModelRedAPIClient(self.api_key, self.base_url) as client:
            return await client.get_assessment_results(assessment_id)

    async def list_models(self) -> List[str]:
        """List registered model IDs"""
        await self._ensure_authenticated()
        return list(self.models.keys())

    async def get_model_info(self, model_id: str) -> Optional[ModelConfig]:
        """Get model configuration info"""
        return self.models.get(model_id)

    async def delete_model(self, model_id: str) -> bool:
        """Delete a registered model"""
        if model_id not in self.models:
            raise ModelNotFoundError(f"Model '{model_id}' not registered")

        try:
            async with ModelRedAPIClient(self.api_key, self.base_url) as client:
                await client.delete_model(model_id)

            del self.models[model_id]
            self.logger.info(f"Deleted model: {model_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete model {model_id}: {e}")
            return False

    async def get_usage_stats(self) -> UsageStats:
        """Get current usage statistics and limits"""
        await self._ensure_authenticated()
        async with ModelRedAPIClient(self.api_key, self.base_url) as client:
            return await client.get_usage_stats()

    def get_supported_providers(self) -> List[str]:
        """Get list of supported model providers"""
        return [provider.value for provider in ModelProvider]

    def get_supported_test_types(self) -> List[str]:
        """Get list of supported test types"""
        return [
            "prompt_injection",
            "jailbreak",
            "toxicity",
            "bias",
            "hallucination",
            "data_leakage",
        ]


# =============================================================================
# EXPORTS
# =============================================================================

__version__ = "1.0.0"
__all__ = [
    "ModelRed",
    "ModelProvider",
    "AssessmentStatus",
    "RiskLevel",
    "ModelConfig",
    "AssessmentResult",
    "UsageStats",
    "ModelRedError",
    "AuthenticationError",
    "QuotaExceededError",
    "ModelNotFoundError",
    "AssessmentError",
    "ValidationError",
]
