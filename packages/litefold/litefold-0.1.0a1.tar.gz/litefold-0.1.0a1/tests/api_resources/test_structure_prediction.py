# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from litefold import Litefold, AsyncLitefold
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStructurePrediction:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_results(self, client: Litefold) -> None:
        structure_prediction = client.structure_prediction.get_results(
            "job_name",
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_results(self, client: Litefold) -> None:
        response = client.structure_prediction.with_raw_response.get_results(
            "job_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_prediction = response.parse()
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_results(self, client: Litefold) -> None:
        with client.structure_prediction.with_streaming_response.get_results(
            "job_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_prediction = response.parse()
            assert_matches_type(object, structure_prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_results(self, client: Litefold) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_name` but received ''"):
            client.structure_prediction.with_raw_response.get_results(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_status(self, client: Litefold) -> None:
        structure_prediction = client.structure_prediction.get_status(
            "job_name",
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_status(self, client: Litefold) -> None:
        response = client.structure_prediction.with_raw_response.get_status(
            "job_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_prediction = response.parse()
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_status(self, client: Litefold) -> None:
        with client.structure_prediction.with_streaming_response.get_status(
            "job_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_prediction = response.parse()
            assert_matches_type(object, structure_prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_status(self, client: Litefold) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_name` but received ''"):
            client.structure_prediction.with_raw_response.get_status(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_submit(self, client: Litefold) -> None:
        structure_prediction = client.structure_prediction.submit(
            job_name="job_name",
            model_name="model_name",
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_submit_with_all_params(self, client: Litefold) -> None:
        structure_prediction = client.structure_prediction.submit(
            job_name="job_name",
            model_name="model_name",
            existing_job_name="existing_job_name",
            files=[b"raw file contents"],
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_submit(self, client: Litefold) -> None:
        response = client.structure_prediction.with_raw_response.submit(
            job_name="job_name",
            model_name="model_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_prediction = response.parse()
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_submit(self, client: Litefold) -> None:
        with client.structure_prediction.with_streaming_response.submit(
            job_name="job_name",
            model_name="model_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_prediction = response.parse()
            assert_matches_type(object, structure_prediction, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStructurePrediction:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_results(self, async_client: AsyncLitefold) -> None:
        structure_prediction = await async_client.structure_prediction.get_results(
            "job_name",
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_results(self, async_client: AsyncLitefold) -> None:
        response = await async_client.structure_prediction.with_raw_response.get_results(
            "job_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_prediction = await response.parse()
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_results(self, async_client: AsyncLitefold) -> None:
        async with async_client.structure_prediction.with_streaming_response.get_results(
            "job_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_prediction = await response.parse()
            assert_matches_type(object, structure_prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_results(self, async_client: AsyncLitefold) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_name` but received ''"):
            await async_client.structure_prediction.with_raw_response.get_results(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_status(self, async_client: AsyncLitefold) -> None:
        structure_prediction = await async_client.structure_prediction.get_status(
            "job_name",
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_status(self, async_client: AsyncLitefold) -> None:
        response = await async_client.structure_prediction.with_raw_response.get_status(
            "job_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_prediction = await response.parse()
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_status(self, async_client: AsyncLitefold) -> None:
        async with async_client.structure_prediction.with_streaming_response.get_status(
            "job_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_prediction = await response.parse()
            assert_matches_type(object, structure_prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_status(self, async_client: AsyncLitefold) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_name` but received ''"):
            await async_client.structure_prediction.with_raw_response.get_status(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_submit(self, async_client: AsyncLitefold) -> None:
        structure_prediction = await async_client.structure_prediction.submit(
            job_name="job_name",
            model_name="model_name",
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_submit_with_all_params(self, async_client: AsyncLitefold) -> None:
        structure_prediction = await async_client.structure_prediction.submit(
            job_name="job_name",
            model_name="model_name",
            existing_job_name="existing_job_name",
            files=[b"raw file contents"],
        )
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_submit(self, async_client: AsyncLitefold) -> None:
        response = await async_client.structure_prediction.with_raw_response.submit(
            job_name="job_name",
            model_name="model_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_prediction = await response.parse()
        assert_matches_type(object, structure_prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_submit(self, async_client: AsyncLitefold) -> None:
        async with async_client.structure_prediction.with_streaming_response.submit(
            job_name="job_name",
            model_name="model_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_prediction = await response.parse()
            assert_matches_type(object, structure_prediction, path=["response"])

        assert cast(Any, response.is_closed) is True
