# ModelRed SDK - Client Library for ModelRed API
# pip install modelred

import asyncio
import aiohttp
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List, Union

# =============================================================================
# TYPES AND ENUMS
# =============================================================================


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
    CANCELLED = "CANCELLED"


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# =============================================================================
# DATA MODELS
# =============================================================================


@dataclass
class ModelConfig:
    model_id: str
    provider: ModelProvider
    model_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=lambda: datetime.now())


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

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(ModelRedError):
    """Invalid API key"""

    pass


class QuotaExceededError(ModelRedError):
    """Usage quota exceeded"""

    def __init__(
        self,
        message: str,
        current_usage: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.current_usage = current_usage
        self.limit = limit


class ModelNotFoundError(ModelRedError):
    """Model not registered"""

    pass


class AssessmentError(ModelRedError):
    """Assessment execution error"""

    pass


class ValidationError(ModelRedError):
    """Invalid parameters"""

    pass


class RateLimitError(ModelRedError):
    """Rate limit exceeded"""

    pass


# =============================================================================
# MAIN CLIENT
# =============================================================================


class ModelRed:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize ModelRed client

        Args:
            api_key: Your ModelRed API key (starts with 'mr_')
                    Can also be set via MODELRED_API_KEY environment variable

        Raises:
            ValidationError: If API key is missing or invalid format
        """
        self.api_key = api_key or os.getenv("MODELRED_API_KEY")
        if not self.api_key:
            raise ValidationError(
                "API key required. Set MODELRED_API_KEY environment variable or pass api_key parameter"
            )

        if not self.api_key.startswith("mr_"):
            raise ValidationError("Invalid API key format. Must start with 'mr_'")

        # Use production URL by default, localhost for development
        self.base_url = os.getenv("MODELRED_API_URL", "http://localhost:3000")

        self.logger = logging.getLogger("modelred")
        self.session = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120),
            headers={
                "User-Agent": "ModelRed-SDK/1.0.0",
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to ModelRed API

        Raises:
            AuthenticationError: Invalid API key (401)
            QuotaExceededError: Usage limits exceeded (403)
            ModelNotFoundError: Resource not found (404)
            RateLimitError: Too many requests (429)
            ModelRedError: Other API errors
        """
        if not self.session:
            raise RuntimeError(
                "Client not initialized. Use 'async with ModelRed() as client:'"
            )

        # All ModelRed endpoints go to /api/modelred/...
        url = f"{self.base_url}/api/modelred{endpoint}"

        try:
            async with self.session.request(method, url, **kwargs) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = {"error": await response.text()}

                # Handle different HTTP status codes with specific exceptions
                if response.status == 401:
                    raise AuthenticationError(
                        message="Invalid API key",
                        status_code=response.status,
                        response_data=response_data,
                    )
                elif response.status == 403:
                    error_message = response_data.get(
                        "error", response_data.get("message", "Quota exceeded")
                    )
                    raise QuotaExceededError(
                        message=error_message,
                        status_code=response.status,
                        response_data=response_data,
                    )
                elif response.status == 404:
                    raise ModelNotFoundError(
                        message=response_data.get(
                            "error", response_data.get("message", "Not found")
                        ),
                        status_code=response.status,
                        response_data=response_data,
                    )
                elif response.status == 429:
                    raise RateLimitError(
                        message=response_data.get(
                            "error", response_data.get("message", "Rate limit exceeded")
                        ),
                        status_code=response.status,
                        response_data=response_data,
                    )
                elif response.status >= 400:
                    raise ModelRedError(
                        message=f"API error ({response.status}): {response_data.get('error', response_data.get('message', 'Unknown error'))}",
                        status_code=response.status,
                        response_data=response_data,
                    )

                return response_data

        except aiohttp.ClientError as e:
            raise ModelRedError(f"Network error: {e}")

    async def validate_api_key(self) -> Dict[str, Any]:
        """Validate API key and get account info

        Returns:
            Dict with validation status and account information

        Raises:
            AuthenticationError: Invalid API key
        """
        return await self._make_request("GET", "/auth/validate")

    async def get_usage_stats(self) -> UsageStats:
        """Get current usage statistics and limits

        Returns:
            UsageStats object with current usage and limits

        Raises:
            AuthenticationError: Invalid API key
        """
        data = await self._make_request("GET", "/account/usage")
        return UsageStats(**data)

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
        """Register a model for security testing

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
            bedrock_model_id: Bedrock model ID

        Returns:
            True if registration successful

        Raises:
            ValidationError: Invalid parameters
            AuthenticationError: Invalid API key
            QuotaExceededError: Model limit exceeded
            ModelRedError: Other API errors

        Examples:
            # OpenAI model
            await client.register_model(
                model_id="my-gpt4",
                provider="openai",
                api_key="sk-...",
                model_name="gpt-4"
            )

            # Anthropic model
            await client.register_model(
                model_id="my-claude",
                provider="anthropic",
                api_key="sk-ant-...",
                model_name="claude-3-sonnet-20240229"
            )
        """
        # Input validation
        if not model_id or not model_id.strip():
            raise ValidationError("Model ID cannot be empty")

        # Convert string to enum
        if isinstance(provider, str):
            try:
                provider = ModelProvider(provider.upper())
            except ValueError:
                supported = ", ".join([p.value.lower() for p in ModelProvider])
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

        # Make API request - matches Next.js API route schema
        payload = {
            "model_id": model_id,
            "provider": provider.value,
            "model_name": model_name,
            "provider_config": provider_config,
            "metadata": metadata or {},
        }

        # Let exceptions bubble up - no catching and re-raising
        response = await self._make_request("POST", "/models", json=payload)
        self.logger.info(f"Registered model: {model_id} ({provider.value})")
        return response.get("success", True)

    async def list_models(self) -> List[Dict[str, Any]]:
        """List all registered models

        Returns:
            List of model dictionaries

        Raises:
            AuthenticationError: Invalid API key
        """
        response = await self._make_request("GET", "/models")
        return response.get("models", [])

    async def get_model(self, model_id: str) -> Dict[str, Any]:
        """Get details for a specific model

        Args:
            model_id: Model identifier

        Returns:
            Model details dictionary

        Raises:
            ModelNotFoundError: Model not found
            AuthenticationError: Invalid API key
        """
        if not model_id or not model_id.strip():
            raise ValidationError("Model ID cannot be empty")

        return await self._make_request("GET", f"/models/{model_id}")

    async def delete_model(self, model_id: str) -> bool:
        """Delete a registered model

        Args:
            model_id: Model identifier to delete

        Returns:
            True if deletion successful

        Raises:
            ModelNotFoundError: Model not found
            AuthenticationError: Invalid API key
            ModelRedError: Other API errors
        """
        if not model_id or not model_id.strip():
            raise ValidationError("Model ID cannot be empty")

        # Let exceptions bubble up - no swallowing errors
        response = await self._make_request("DELETE", f"/models/{model_id}")
        self.logger.info(f"Deleted model: {model_id}")
        return response.get("success", True)

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

        Raises:
            ValidationError: Invalid parameters
            ModelNotFoundError: Model not registered
            QuotaExceededError: Assessment limit exceeded
            AssessmentError: Assessment failed
            AuthenticationError: Invalid API key
        """
        if not model_id or not model_id.strip():
            raise ValidationError("Model ID cannot be empty")

        if test_types is None:
            test_types = ["prompt_injection", "jailbreak", "toxicity"]

        if not test_types:
            raise ValidationError("At least one test type must be specified")

        valid_priorities = ["low", "normal", "high", "critical"]
        if priority not in valid_priorities:
            raise ValidationError(
                f"Priority must be one of: {', '.join(valid_priorities)}"
            )

        # Start assessment - matches Next.js API route schema
        payload = {"model_id": model_id, "test_types": test_types, "priority": priority}

        response = await self._make_request("POST", "/assessments", json=payload)
        assessment_id = response["assessment_id"]

        self.logger.info(f"Started assessment: {assessment_id}")

        if not wait_for_completion:
            # Return minimal result without waiting
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
                test_types=test_types,
            )

        # Wait for completion with progress updates
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        last_progress = 0

        while time.time() - start_time < timeout_seconds:
            try:
                status_response = await self.get_assessment_status(assessment_id)
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
                    return await self.get_assessment_results(assessment_id)

                elif status == AssessmentStatus.FAILED:
                    error_msg = status_response.get("error_message", "Unknown error")
                    raise AssessmentError(f"Assessment failed: {error_msg}")

                elif status == AssessmentStatus.CANCELLED:
                    raise AssessmentError("Assessment was cancelled")

                # Wait before next check
                await asyncio.sleep(10)

            except ModelRedError:
                # Re-raise ModelRed errors immediately
                raise
            except Exception as e:
                # Handle transient errors
                self.logger.warning(f"Status check failed (retrying): {e}")
                await asyncio.sleep(5)

        raise AssessmentError(f"Assessment timeout after {timeout_minutes} minutes")

    async def get_assessment_status(self, assessment_id: str) -> Dict[str, Any]:
        """Get real-time assessment status

        Args:
            assessment_id: Assessment identifier

        Returns:
            Assessment status dictionary

        Raises:
            ModelNotFoundError: Assessment not found
            AuthenticationError: Invalid API key
        """
        if not assessment_id or not assessment_id.strip():
            raise ValidationError("Assessment ID cannot be empty")

        return await self._make_request("GET", f"/assessments/{assessment_id}")

    async def get_assessment_results(self, assessment_id: str) -> AssessmentResult:
        """Get detailed assessment results

        Args:
            assessment_id: Assessment identifier

        Returns:
            Complete AssessmentResult object

        Raises:
            ModelNotFoundError: Assessment not found
            AssessmentError: Assessment not completed
            AuthenticationError: Invalid API key
        """
        if not assessment_id or not assessment_id.strip():
            raise ValidationError("Assessment ID cannot be empty")

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

    async def list_assessments(self) -> List[Dict[str, Any]]:
        """List all assessments

        Returns:
            List of assessment dictionaries

        Raises:
            AuthenticationError: Invalid API key
        """
        response = await self._make_request("GET", "/assessments")
        return response.get("assessments", [])

    def get_supported_providers(self) -> List[str]:
        """Get list of supported model providers

        Returns:
            List of provider names (lowercase)
        """
        return [provider.value.lower() for provider in ModelProvider]

    def get_supported_test_types(self) -> List[str]:
        """Get list of supported test types

        Returns:
            List of test type names
        """
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
    "RateLimitError",
]
