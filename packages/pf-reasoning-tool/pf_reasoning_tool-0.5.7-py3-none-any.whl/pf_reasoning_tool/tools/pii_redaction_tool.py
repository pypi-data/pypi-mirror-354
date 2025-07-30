# -*- coding: utf-8 -*-
"""
Azure AI Language Service PII Detection and Redaction Tool
==========================================================
Takes a string input and returns a string with PII redacted,
using the Azure AI Language Service.
"""

from __future__ import annotations

import logging
import os
from typing import List, Optional, Tuple

# Attempt to import 'requests'.  PromptFlow may scan modules in an environment
# that does not yet have third-party packages installed, which would crash
# discovery if we imported unconditionally.
try:
    import requests  # noqa: E402  (keep import near the top for clarity)
except ImportError:  # pragma: no cover
    requests = None  # will be checked at runtime

# Core PromptFlow imports
from promptflow.core import tool
from promptflow.connections import CustomConnection

# ------------------------------------------------------------------ #
# 1.  Robust Logger Setup                                            #
# ------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
log_level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, log_level_name, logging.INFO))

if not logger.handlers:  # make logs visible when run locally
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(_handler)

# ------------------------------------------------------------------ #
# 2.  Global Constants                                               #
# ------------------------------------------------------------------ #
LANGUAGE_API_VERSION = '2023-04-01'  # GA version at time of writing

# ------------------------------------------------------------------ #
# 3.  Credential Extraction Helper                                   #
# ------------------------------------------------------------------ #
def _extract_language_service_credentials(conn: CustomConnection) -> Tuple[str, str]:
    """Return (endpoint, api_key) extracted from a CustomConnection."""
    # PromptFlow’s CustomConnection behaves like a dict
    c = dict(conn)

    endpoint = (
        c.get('endpoint')
        or c.get('api_base')
        or c.get('value1')
        or c.get('key1')
    )
    api_key = (
        c.get('api_key')
        or c.get('value2')
        or c.get('key2')
        or c.get('key')
    )

    if not endpoint:
        raise ValueError('Connection is missing an endpoint (endpoint/api_base).')
    if not api_key or api_key == '***':
        raise ValueError('Connection is missing a valid API key (key2/api_key).')

    # Strip path if somebody pasted the full REST URL
    if '/language/:analyze-text' in endpoint:
        endpoint = endpoint.split('/language/:analyze-text')[0]

    return endpoint.rstrip('/'), api_key

# ------------------------------------------------------------------ #
# 4.  Main PromptFlow Tool (SDK version)                             #
# ------------------------------------------------------------------ #

from azure.ai.textanalytics import TextAnalyticsClient, PiiEntityDomainType
from azure.core.credentials import AzureKeyCredential


@tool
def redact_pii_text(
    connection: CustomConnection,
    text_input: str,
    language: str = 'en',
    pii_categories: Optional[List[str]] = None,
) -> str:
    '''
    Detects and redacts PII from *text_input* using the Azure AI
    Text Analytics SDK.  Returns the redacted string.  If no PII is
    found, the original text is returned unchanged.
    '''
    if not text_input or not text_input.strip():
        logger.warning('Input text is empty or whitespace only.  Returning as-is.')
        return text_input

    # Pull endpoint and key out of the PromptFlow connection
    endpoint, api_key = _extract_language_service_credentials(connection)

    # Build the SDK client (no retry policy tweaks needed for a single call)
    ta_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
        api_version='v3.2'  # maps to REST 2023-04-01 under the hood
    )

    # The SDK works on batches; we pass a single-item list
    try:
        response = ta_client.recognize_pii_entities(
            documents=[text_input],
            language=language,
            categories_filter=pii_categories or None,
            model_version='latest',
            domain_filter=PiiEntityDomainType.NONE  # keep generic, not healthcare
        )
    except Exception as e:  # covers HTTP and client errors
        logger.error(f'Text Analytics SDK call failed: {e}', exc_info=True)
        raise RuntimeError(f'PII redaction failed: {e}') from e

    doc_result = response[0]

    if doc_result.is_error:  # SDK surfaces a rich error object
        err = doc_result.error
        raise RuntimeError(
            f'Language Service returned an error '
            f'({err.code} - {err.message})'
        )

    # If no PII entities are detected, redacted_text will be None
    redacted = getattr(doc_result, "redacted_text", None)
    return redacted if redacted is not None else text_input

