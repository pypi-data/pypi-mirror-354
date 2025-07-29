# Copyright 2021 - 2025 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
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

"""This module provides all API calls related to downloading files."""

from typing import Union

import httpx
from tenacity import RetryError

from ghga_connector.constants import CACHE_MIN_FRESH, TIMEOUT_LONG
from ghga_connector.core import RetryHandler, WorkPackageAccessor, exceptions

from .structs import (
    RetryResponse,
    UrlAndHeaders,
    URLResponse,
)


async def _get_authorization(
    file_id: str, work_package_accessor: WorkPackageAccessor, bust_cache: bool = False
) -> httpx.Headers:
    """
    Fetch work order token using accessor and prepare DCS endpoint URL and headers for a
    given endpoint identified by the `url` passed.

    The calls will use the cache if possible while the cached responses are still fresh
    for at least another `CACHE_MIN_FRESH` seconds.
    """
    # fetch a work order token
    decrypted_token = await work_package_accessor.get_work_order_token(
        file_id=file_id, bust_cache=bust_cache
    )
    # build headers
    headers = httpx.Headers(
        {
            "Accept": "application/json",
            "Authorization": f"Bearer {decrypted_token}",
            "Content-Type": "application/json",
            "Cache-Control": f"min-fresh={CACHE_MIN_FRESH}",
        }
    )

    return headers


async def get_envelope_authorization(
    file_id: str, work_package_accessor: WorkPackageAccessor
) -> UrlAndHeaders:
    """
    Fetch work order token using accessor and prepare DCS endpoint URL and headers to get
    a Crypt4GH envelope for file identified by `file_id`
    """
    # build url
    url = f"{work_package_accessor.dcs_api_url}/objects/{file_id}/envelopes"
    headers = await _get_authorization(
        file_id=file_id, work_package_accessor=work_package_accessor
    )
    return UrlAndHeaders(url, headers)


async def get_file_authorization(
    file_id: str, work_package_accessor: WorkPackageAccessor, bust_cache: bool = False
) -> UrlAndHeaders:
    """
    Fetch work order token using accessor and prepare DCS endpoint URL and headers to get
    object storage URL for file download
    """
    # build URL
    url = f"{work_package_accessor.dcs_api_url}/objects/{file_id}"
    headers = await _get_authorization(
        file_id=file_id,
        work_package_accessor=work_package_accessor,
        bust_cache=bust_cache,
    )
    return UrlAndHeaders(url, headers)


async def get_download_url(  # noqa: C901, PLR0912
    *,
    client: httpx.AsyncClient,
    url_and_headers: UrlAndHeaders,
    bust_cache: bool = False,
) -> Union[RetryResponse, URLResponse]:
    """
    Perform a RESTful API call to retrieve a presigned download URL.
    Returns:
        If the download url is not available yet, a RetryResponse is returned,
        containing the time in seconds after which the download url should become
        available.
        Otherwise, a URLResponse containing the download url and file size in bytes
        is returned.
    """
    url = url_and_headers.endpoint_url
    headers = url_and_headers.headers

    if bust_cache:
        # update cache-control headers to get fresh response from source
        cache_control_headers = headers.get("Cache-Control")
        if not cache_control_headers:
            cache_control_headers = ["max-age=0"]
        else:
            cache_control_headers = [cache_control_headers, "max-age=0"]
        headers["Cache-Control"] = ",".join(cache_control_headers)

    try:
        retry_handler = RetryHandler.basic()
        response: httpx.Response = await retry_handler(
            fn=client.get,
            url=url,
            headers=headers,
            timeout=TIMEOUT_LONG,
        )

    except RetryError as retry_error:
        wrapped_exception = retry_error.last_attempt.exception()

        if isinstance(wrapped_exception, httpx.RequestError):
            exceptions.raise_if_connection_failed(
                request_error=wrapped_exception, url=url
            )
            raise exceptions.RequestFailedError(url=url) from retry_error
        elif wrapped_exception:
            raise wrapped_exception from retry_error
        elif result := retry_error.last_attempt.result():
            response = result
        else:
            raise

    status_code = response.status_code
    if status_code != 200:
        if status_code == 403:
            content = response.json()
            # handle both normal and httpyexpect 403 response
            try:
                cause = content["description"]
            except KeyError:
                cause = content["detail"]
            raise exceptions.UnauthorizedAPICallError(url=url, cause=cause)
        if status_code != 202:
            raise exceptions.BadResponseCodeError(url=url, response_code=status_code)

        headers = response.headers
        if "retry-after" not in headers:
            raise exceptions.RetryTimeExpectedError(url=url)

        return RetryResponse(retry_after=int(headers["retry-after"]))

    # look for an access method of type s3 in the response:
    response_body = response.json()
    download_url = None
    access_methods = response_body["access_methods"]
    for access_method in access_methods:
        if access_method["type"] == "s3":
            download_url = access_method["access_url"]["url"]
            file_size = response_body["size"]
            break
    else:
        raise exceptions.NoS3AccessMethodError(url=url)

    return URLResponse(
        download_url=download_url,
        file_size=file_size,
    )
