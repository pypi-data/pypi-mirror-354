# ByteDance Volcengine EMR, Copyright 2024.
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

from unittest.mock import Mock

import pytest
import requests
from tos.exceptions import TosClientError, TosServerError
from tos.http import Response
from urllib3 import HTTPConnectionPool
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from tosfs.retry import _get_sleep_time, is_retryable_exception

mock_resp = Mock(spec=requests.Response)

mock_resp.status_code = 429
mock_resp.headers = {"content-length": "123", "x-tos-request-id": "test-id"}
mock_resp.iter_content = Mock(return_value=[b"chunk1", b"chunk2", b"chunk3"])
mock_resp.json = Mock(return_value={"key": "value"})

response = Response(mock_resp)


@pytest.mark.parametrize(
    ("exception", "expected"),
    [
        (
            TosServerError(
                response,
                "Exceed account external rate limit. Too much throughput in a "
                "short period of time, please slow down.",
                "ExceedAccountExternalRateLimit",
                "KmsJSKDKhjasdlKmsduwRETYHB",
                "",
                "0004-00000001",
            ),
            True,
        ),
        (
            TosClientError(
                "http request timeout",
                ConnectionError(
                    ProtocolError(
                        "Connection aborted.",
                        ConnectionResetError(104, "Connection reset by peer"),
                    )
                ),
            ),
            True,
        ),
        (
            TosClientError(
                "{'message': 'http request timeout', "
                "'case': \"('Connection aborted.', "
                "ConnectionResetError(104, 'Connection reset by peer'))\", "
                "'request_url': "
                "'http://proton-ci.tos-cn-beijing.volces.com/"
                "nHnbR/yAlen'}",
                TosClientError(
                    "http request timeout",
                    ConnectionError(
                        ProtocolError(
                            "Connection aborted.",
                            ConnectionResetError(104, "Connection reset by peer"),
                        )
                    ),
                ),
            ),
            True,
        ),
        (
            requests.exceptions.ConnectionError(
                HTTPConnectionPool(host="proton-ci.tos-cn-beijing.volces.com", port=80)
            ),
            True,
        ),
        (
            ReadTimeoutError(None, message="", url=""),
            True,
        ),
    ],
)
def test_is_retry_exception(
    exception,
    expected,
):
    assert is_retryable_exception(exception) == expected


def test_get_sleep_time():
    mock_resp = Mock(spec=requests.Response)

    sleep_time = 1000

    mock_resp.status_code = 429
    mock_resp.headers = {
        "Content-Type": "application/json",
        "Date": "Thu, 07 Nov 2024 17:19:56 GMT",
        "Retry-After": str(sleep_time),
        "Server": "TosServer",
        "x-tos-ec": "0004-00000007",
        "x-tos-id-2": "0000-00000-0000",
        "x-tos-request-id": "0000-0000-0000",
        "x-tos-server-time": "1",
        "Content-Length": "277",
    }
    mock_resp.iter_content = Mock(return_value=[b"chunk1", b"chunk2", b"chunk3"])
    mock_resp.json = Mock(return_value={"key": "value"})

    response = Response(mock_resp)

    err = TosServerError(
        response,
        "Exceed account external rate limit. Too much throughput in a "
        "short period of time, please slow down.",
        "ExceedAccountExternalRateLimit",
        "KmsJSKDKhjasdlKmsduwRETYHB",
        "",
        "0004-00000001",
    )

    assert _get_sleep_time(err, 1) == sleep_time
