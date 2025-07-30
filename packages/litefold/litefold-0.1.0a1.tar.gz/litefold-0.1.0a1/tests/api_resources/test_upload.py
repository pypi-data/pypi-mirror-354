# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from litefold import Litefold, AsyncLitefold
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUpload:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_fasta(self, client: Litefold) -> None:
        upload = client.upload.create_fasta(
            files=[b"raw file contents"],
            job_name="job_name",
        )
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_fasta(self, client: Litefold) -> None:
        response = client.upload.with_raw_response.create_fasta(
            files=[b"raw file contents"],
            job_name="job_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_fasta(self, client: Litefold) -> None:
        with client.upload.with_streaming_response.create_fasta(
            files=[b"raw file contents"],
            job_name="job_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(object, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_stats(self, client: Litefold) -> None:
        upload = client.upload.get_stats()
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_stats(self, client: Litefold) -> None:
        response = client.upload.with_raw_response.get_stats()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_stats(self, client: Litefold) -> None:
        with client.upload.with_streaming_response.get_stats() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(object, upload, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUpload:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_fasta(self, async_client: AsyncLitefold) -> None:
        upload = await async_client.upload.create_fasta(
            files=[b"raw file contents"],
            job_name="job_name",
        )
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_fasta(self, async_client: AsyncLitefold) -> None:
        response = await async_client.upload.with_raw_response.create_fasta(
            files=[b"raw file contents"],
            job_name="job_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_fasta(self, async_client: AsyncLitefold) -> None:
        async with async_client.upload.with_streaming_response.create_fasta(
            files=[b"raw file contents"],
            job_name="job_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(object, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_stats(self, async_client: AsyncLitefold) -> None:
        upload = await async_client.upload.get_stats()
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_stats(self, async_client: AsyncLitefold) -> None:
        response = await async_client.upload.with_raw_response.get_stats()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(object, upload, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_stats(self, async_client: AsyncLitefold) -> None:
        async with async_client.upload.with_streaming_response.get_stats() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(object, upload, path=["response"])

        assert cast(Any, response.is_closed) is True
