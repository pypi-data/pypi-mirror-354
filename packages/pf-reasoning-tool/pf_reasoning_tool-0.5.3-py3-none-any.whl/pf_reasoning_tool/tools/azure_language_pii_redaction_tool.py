# -*- coding: utf-8 -*-
"""
Azure AI Language Service PII Detection and Redaction Tool
=========================================================
Takes a string input and returns a string with PII redacted,
using the Azure AI Language Service.
"""

from __future__ import annotations

import logging
import os
import requests  # Required for REST API calls
from typing import List, Optional, Tuple

# Core PromptFlow imports
from promptflow.core import tool
from promptflow.connections import CustomConnection

# ------------------------------------------------------------------ #
# 1.  Robust Logger Setup (Prevents Import-Time Crashes)            #
# ------------------------------------------------------------------ #
# This setup is hardened to prevent crashes if the LOG_LEVEL env var is missing or invalid.
logger = logging.getLogger(__name__)
log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_name, logging.INFO)
logger.setLevel(log_level)

# Ensure logs are visible during local testing by adding a handler if none exist
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ------------------------------------------------------------------ #
# 2.  Global Constants                                               #
# ------------------------------------------------------------------ #
# Using a GA version is recommended.
# Refer to: https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/model-lifecycle
LANGUAGE_API_VERSION = "2023-04-01"

# ------------------------------------------------------------------ #
# 3.  Credential Extraction Helper                                   #
# ------------------------------------------------------------------ #
def _extract_language_service_credentials(conn: CustomConnection) -> Tuple[str, str]:
    # Secret bag
    secrets = getattr(conn, 'secrets', {}) or {}

    # Non-secret configs – access as attributes, not as a dict
    endpoint = getattr(conn, 'endpoint', None) or getattr(conn, 'api_base', None)
    api_key  = secrets.get('api_key') or secrets.get('key')

    if not endpoint:
        raise ValueError('Connection is missing an "endpoint" (or "api_base") value.')
    if not api_key:
        raise ValueError('Connection is missing the API key secret ("api_key" or "key").')

    # Strip any trailing /language/:analyze-text that might have been pasted in
    if '/language/:analyze-text' in endpoint:
        endpoint = endpoint.split('/language/:analyze-text')[0]

    logger.debug(f'Using Language Service endpoint: {endpoint.rstrip("/")}')
    return endpoint, api_key

# ------------------------------------------------------------------ #
# 4.  Main PromptFlow Tool Function                                  #
# ------------------------------------------------------------------ #
@tool
def redact_pii_text(
    connection: CustomConnection,
    text_input: str,
    language: str = "en",
    pii_categories: Optional[List[str]] = None,
) -> str:
    """
    Detects and redacts Personally Identifiable Information (PII) from input text
    using the Azure AI Language Service.
    """
    if not text_input or not text_input.strip():
        logger.warning("Input text is empty or whitespace only. Returning as is.")
        return text_input

    try:
        endpoint, api_key = _extract_language_service_credentials(connection)
    except Exception as e:
        logger.error(f"Failed to extract Language Service credentials: {e}", exc_info=True)
        # Re-raise with a user-friendly message for the PF UI
        raise ValueError(f"Invalid Language Service connection provided. Details: {e}") from e

    api_url = f"{endpoint.rstrip('/')}/language/:analyze-text?api-version={LANGUAGE_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload_parameters = {"modelVersion": "latest"}
    if pii_categories and isinstance(pii_categories, list) and len(pii_categories) > 0:
        payload_parameters["piiCategories"] = pii_categories
        logger.info(f"Using custom PII categories for redaction: {pii_categories}")

    payload = {
        "kind": "PiiEntityRecognition",
        "parameters": payload_parameters,
        "analysisInput": {
            "documents": [{"id": "1", "language": language, "text": text_input}]
        },
    }

    logger.debug(f"Sending PII redaction request to: {api_url}")
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        response_json = response.json()
        logger.debug(f"Received API response: {response_json}")

        results = response_json.get("results", {})
        if results.get("errors"):
            errors = results["errors"]
            error_message = "; ".join([e.get("error", {}).get("message", "Unknown error") for e in errors])
            logger.error(f"Language Service API returned errors: {error_message}")
            raise RuntimeError(f"Language Service API returned errors: {error_message}")

        if results.get("documents"):
            doc_result = results["documents"][0]
            if "redactedText" in doc_result:
                logger.info("PII redaction successful.")
                return doc_result["redactedText"]
            else:
                # This can happen if no PII is found; the original text is returned.
                logger.warning("API response did not contain 'redactedText'. Returning original text.")
                return text_input
        else:
            logger.error(f"Unexpected API response format: {response_json}")
            raise RuntimeError("Unexpected response format from Language Service API.")

    except requests.exceptions.HTTPError as http_err:
        error_body = http_err.response.text
        logger.error(f"HTTP error occurred: {http_err} - Response: {error_body}", exc_info=True)
        raise RuntimeError(f"Language Service API request failed with HTTP {http_err.response.status_code}. Details: {error_body}") from http_err
    except Exception as e:
        logger.error(f"An unexpected error occurred during PII redaction: {e}", exc_info=True)
        raise RuntimeError(f"An unexpected error occurred: {e}") from e