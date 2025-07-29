#
# Copyright 2025 ABSA Group Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This module contains decorators for adding debug logging to method calls
and for creating rate-limited safe call functions.
"""

import logging

from typing import Callable, Optional, Any
from functools import wraps
from github import GithubException
from requests import Timeout, RequestException

from living_doc_utilities.github.rate_limiter import GithubRateLimiter

logger = logging.getLogger(__name__)


def debug_log_decorator(method: Callable) -> Callable:
    """
    Decorator to add debug logging for a method call.

    @param method: The method to decorate.
    @return: The decorated method.
    """

    @wraps(method)
    def wrapped(*args, **kwargs) -> Optional[Any]:
        logger.debug("Calling method %s with args: %s and kwargs: %s.", method.__name__, args, kwargs)
        result = method(*args, **kwargs)
        logger.debug("Method %s returned %s.", method.__name__, result)
        return result

    return wrapped


def safe_call_decorator(rate_limiter: GithubRateLimiter) -> Callable:
    """
    Decorator factory to create a rate-limited safe call function.

    @param rate_limiter: The rate limiter to use.
    @return: The decorator.
    """

    def decorator(method: Callable) -> Callable:
        # Note: Keep the log decorator first to log the correct method name.
        @debug_log_decorator
        @wraps(method)
        @rate_limiter
        def wrapped(*args, **kwargs) -> Optional[Any]:
            try:
                return method(*args, **kwargs)
            except (ConnectionError, Timeout) as e:
                logger.error("Network error calling %s: %s.", method.__name__, e, exc_info=True)
                return None
            except GithubException as e:
                logger.error("GitHub API error calling %s: %s.", method.__name__, e, exc_info=True)
                return None
            except RequestException as e:
                logger.error("HTTP error calling %s: %s.", method.__name__, e, exc_info=True)
                return None
            # pylint: disable=broad-exception-caught
            except Exception as e:
                logger.error(
                    "Unexpected error of type %s occurred in %s: %s.",
                    type(e).__name__,
                    method.__name__,
                    e,
                    exc_info=True,
                )
                return None

        return wrapped

    return decorator
