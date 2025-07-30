# -*- coding: utf-8 -*-
"""
Azure AI Language Service – PII Detection and Redaction Tool
===========================================================

Accepts a text string and returns the same string with any detected
Personally Identifiable Information (PII) redacted by the Azure AI Language Service.
"""

from __future__ import annotations

import logging
import os
from typing import List, Optional, Tuple

# ------------------------------------------------------------------ #
# 1   Safe import of 'requests'                                       #
# ------------------------------------------------------------------ #
# PromptFlow scans tool modules in an environment that may not have third-
# party packages installed yet.  We import 'requests' defensively so the
# module still loads (which keeps the *other* tools visible in the UI).
try:
    import requests  # noqa: E402 – keep near the top for readability
except ImportError:  # pragma: no cover
    requests = None  # will be checked at runtime

# PromptFlow core
from promptflow.core import tool
from promptflow.connections import CustomConnection

# ------------------------------------------------------------------ #
# 2   Logging setup                                                  #
# ------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper(), logging.INFO))

if not logger.handlers:  # ensure console output when run locally
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(_h)

# ------------------------------------------------------------------ #
# 3   Constants                                                      #
# ------------------------------------------------------------------ #
LANGUAGE_API_VERSION = '2023-04-01'  # current GA REST version

# ------------------------------------------------------------------ #
# 4   Credential helper                                              #
# ------------------------------------------------------------------ #
def _extract_language_service_credentials(conn: CustomConnection) -> Tuple[str, str]:
    """
    Return (endpoint, api_key) from a CustomConnection.

    Accepts either key1/key2 or the newer attribute names.
    Raises a ValueError with a clear message if anything is missing.
    """
    c = dict(conn)  # CustomConnection is dict-like

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
        raise ValueError('Azure Language Service connection is missing the endpoint (key1).')
    if not api_key or api_key == '***':
        raise ValueError('Azure Language Service connection is missing a valid API key (key2).')

    # Trim if someone pasted the full REST path
    if '/language/:analyze-text' in endpoint:
        endpoint = endpoint.split('/language/:analyze-text')[0]

    return endpoint.rstrip('/'), api_key

# ------------------------------------------------------------------ #
# 5   Main PromptFlow tool                                           #
# ------------------------------------------------------------------ #
@tool
def redact_pii_text(
    connection: CustomConnection,
    text_input: str,
    language: str = 'en',
    pii_categories: Optional[List[str]] = None,
) -> str:
    """
    Detects and redacts PII from *text_input*.

    • If `pii_categories` is provided, the service only looks for those categories.  
    • If no PII is found the original text is returned unchanged.
    """
    # Quick sanity check
    if not text_input or not text_input.strip():
        logger.warning('Input text is empty or whitespace only.  Returning as-is.')
        return text_input

    # Ensure 'requests' is available in the runtime (it may be missing in discovery)
    if requests is None:  # pragma: no cover
        raise RuntimeError(
            'The "requests" package is not installed in this runtime.  '
            'Add "requests>=2.31.0" to your environment or custom container.'
        )

    # Credentials
    endpoint, api_key = _extract_language_service_credentials(connection)

    api_url = f'{endpoint}/language/:analyze-text?api-version={LANGUAGE_API_VERSION}'
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/json',
    }

    # Build the REST payload
    parameters = {'modelVersion': 'latest'}
    if pii_categories:
        parameters['piiCategories'] = pii_categories
        logger.info(f'Filtering PII categories: {pii_categories}')

    payload = {
        'kind': 'PiiEntityRecognition',
        'parameters': parameters,
        'analysisInput': {
            'documents': [{'id': '1', 'language': language, 'text': text_input}]
        },
    }

    logger.debug(f'Sending PII request to {api_url}')
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        body = resp.json()
    except requests.exceptions.HTTPError as http_err:  # pragma: no cover
        raise RuntimeError(
            f'Language Service request failed with HTTP {http_err.response.status_code}: '
            f'{http_err.response.text}'
        ) from http_err
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f'PII redaction failed: {e}') from e

    # Parse response
    results = body.get('results', {})
    if results.get('errors'):
        err_msg = '; '.join(
            e.get('error', {}).get('message', 'Unknown error') for e in results['errors']
        )
        raise RuntimeError(f'Language Service returned errors: {err_msg}')

    docs = results.get('documents')
    if docs and 'redactedText' in docs[0]:
        logger.info('PII redaction successful.')
        return docs[0]['redactedText']

    # No PII detected or unexpected shape
    logger.warning("No 'redactedText' in response; returning original text.")
    return text_input
