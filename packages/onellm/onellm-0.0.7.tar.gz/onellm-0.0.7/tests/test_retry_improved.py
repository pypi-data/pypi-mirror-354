import asyncio
"""
Improved tests for the retry utility.

These tests focus on achieving 100% code coverage for the retry utilities,
with special attention to edge cases and error handling.
"""

import random
import pytest
from unittest import mock

from onellm.utils.retry import retry_async, RetryConfig, _calculate_backoff
from onellm.errors import RateLimitError, ServiceUnavailableError


class TestRetryConfigClass:
    """Tests for the RetryConfig class."""

    def test_default_initialization(self):
        """Test default initialization of RetryConfig."""
        config = RetryConfig()

        # Check default values
        assert config.max_retries == 3
        assert config.initial_backoff == 0.5
        assert config.max_backoff == 60.0
        assert config.backoff_multiplier == 2.0
        assert config.jitter is True

        # Check default retryable errors
        assert len(config.retryable_errors) == 6
        error_types = [type(err()) for err in config.retryable_errors if not isinstance(err, type)]
        error_types.extend([err for err in config.retryable_errors if isinstance(err, type)])
        assert RateLimitError in error_types or RateLimitError in config.retryable_errors
        assert (ServiceUnavailableError in error_types or
                ServiceUnavailableError in config.retryable_errors)
        assert ConnectionError in error_types or ConnectionError in config.retryable_errors

    def test_custom_initialization(self):
        """Test custom initialization of RetryConfig."""
        config = RetryConfig(
            max_retries=5,
            initial_backoff=1.0,
            max_backoff=30.0,
            backoff_multiplier=3.0,
            jitter=False,
            retryable_errors=[ValueError, TypeError]
        )

        # Check custom values
        assert config.max_retries == 5
        assert config.initial_backoff == 1.0
        assert config.max_backoff == 30.0
        assert config.backoff_multiplier == 3.0
        assert config.jitter is False
        assert config.retryable_errors == [ValueError, TypeError]


class TestRetryAsyncEdgeCases:
    """Tests for edge cases in the retry_async function."""

    @pytest.mark.asyncio
    async def test_always_failing_function(self):
        """Test with a function that always fails with retryable errors."""
        # Create a counter for verifying calls
        call_counter = 0

        async def failing_func():
            nonlocal call_counter
            call_counter += 1
            raise RateLimitError(f"Rate limited (attempt {call_counter})")

        config = RetryConfig(max_retries=4, initial_backoff=0.01, jitter=False)

        # Mock sleep to avoid actual waiting
        with mock.patch("asyncio.sleep") as mock_sleep:
            with pytest.raises(RateLimitError) as excinfo:
                await retry_async(failing_func, config=config)

            # Should make exactly 5 attempts (original + 4 retries)
            assert call_counter == 5
            assert "attempt 5" in str(excinfo.value)

            # Sleep should be called 4 times (after each failure except the last)
            assert mock_sleep.call_count == 4

            # Check backoff times (0.01, 0.02, 0.04, 0.08)
            expected_backoffs = [0.01, 0.02, 0.04, 0.08]
            actual_backoffs = [call[0][0] for call in mock_sleep.call_args_list]
            assert actual_backoffs == expected_backoffs

    @pytest.mark.asyncio
    async def test_random_jitter_deterministic(self):
        """Test that jitter is deterministic when random.random is fixed."""
        config = RetryConfig(initial_backoff=1.0, jitter=True)

        # Mock random.random to return fixed values
        with mock.patch("random.random", return_value=0.75):  # 0.5 + 0.75 = 1.25 multiplier
            backoff = _calculate_backoff(1, config)
            assert backoff == 1.25  # 1.0 * 1.25

            # Verify calculate_backoff was using our mocked random.random
            random_mock = random.random
            assert random_mock() == 0.75

    @pytest.mark.asyncio
    async def test_last_error_reraise(self):
        """Test that retry_async properly re-raises the last error after retries."""
        # Create a test error with a distinct message for verification
        test_error = RateLimitError("Specific last error test")

        @pytest.mark.asyncio
        # Create a test function that raises our specific error
        async def test_function(*args, **kwargs):
            raise test_error

        # Force the retry mechanism to re-raise by setting max_retries=0
        # and patching _should_retry to return False
        with mock.patch("onellm.utils.retry._should_retry", return_value=False):
            # Call with a config that has max_retries=0
            config = RetryConfig(max_retries=0)

            # Call retry_async and verify it raises our test error
            with pytest.raises(RateLimitError) as excinfo:
                await retry_async(test_function, config=config)

            # Verify it's our specific error
            assert "Specific last error test" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_retry_with_multiple_error_instances(self):
        """Test retry with multiple instances of allowed error types."""
        class CustomRetryableError(Exception):
            pass

        # Function fails with different instances of the same error type
        errors = [
            CustomRetryableError("Error 1"),
            CustomRetryableError("Error 2"),
            CustomRetryableError("Error 3")
        ]
        mock_func = mock.AsyncMock(side_effect=errors)

        # Custom config that retries CustomRetryableError
        config = RetryConfig(
            max_retries=2,
            retryable_errors=[CustomRetryableError],
            initial_backoff=0.01,
            jitter=False
        )

        # Mock sleep to avoid actual waiting
        with mock.patch("asyncio.sleep") as mock_sleep:
            with pytest.raises(CustomRetryableError) as excinfo:
                await retry_async(mock_func, config=config)

            # Should have the third error message
            assert "Error 3" in str(excinfo.value)

            # Should be called 3 times
            assert mock_func.call_count == 3

            # Sleep should be called twice
            assert mock_sleep.call_count == 2
