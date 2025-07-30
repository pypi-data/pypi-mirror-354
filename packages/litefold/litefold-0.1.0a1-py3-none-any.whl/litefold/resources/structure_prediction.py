# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Mapping, Optional, cast

import httpx

from ..types import structure_prediction_submit_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["StructurePredictionResource", "AsyncStructurePredictionResource"]


class StructurePredictionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StructurePredictionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiteFold/LiteFoldSDK#accessing-raw-response-data-eg-headers
        """
        return StructurePredictionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StructurePredictionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiteFold/LiteFoldSDK#with_streaming_response
        """
        return StructurePredictionResourceWithStreamingResponse(self)

    def get_results(
        self,
        job_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Job Results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_name:
            raise ValueError(f"Expected a non-empty value for `job_name` but received {job_name!r}")
        return self._get(
            f"/structure-prediction/results/{job_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def get_status(
        self,
        job_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get status of a structure prediction job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_name:
            raise ValueError(f"Expected a non-empty value for `job_name` but received {job_name!r}")
        return self._get(
            f"/structure-prediction/status/{job_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def submit(
        self,
        *,
        job_name: str,
        model_name: str,
        existing_job_name: Optional[str] | NotGiven = NOT_GIVEN,
        files: Optional[List[FileTypes]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Submit Structure Prediction

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "job_name": job_name,
                "model_name": model_name,
                "existing_job_name": existing_job_name,
                "files": files,
            }
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/structure-prediction/submit",
            body=maybe_transform(body, structure_prediction_submit_params.StructurePredictionSubmitParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncStructurePredictionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStructurePredictionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiteFold/LiteFoldSDK#accessing-raw-response-data-eg-headers
        """
        return AsyncStructurePredictionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStructurePredictionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiteFold/LiteFoldSDK#with_streaming_response
        """
        return AsyncStructurePredictionResourceWithStreamingResponse(self)

    async def get_results(
        self,
        job_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Job Results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_name:
            raise ValueError(f"Expected a non-empty value for `job_name` but received {job_name!r}")
        return await self._get(
            f"/structure-prediction/results/{job_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def get_status(
        self,
        job_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get status of a structure prediction job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_name:
            raise ValueError(f"Expected a non-empty value for `job_name` but received {job_name!r}")
        return await self._get(
            f"/structure-prediction/status/{job_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def submit(
        self,
        *,
        job_name: str,
        model_name: str,
        existing_job_name: Optional[str] | NotGiven = NOT_GIVEN,
        files: Optional[List[FileTypes]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Submit Structure Prediction

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "job_name": job_name,
                "model_name": model_name,
                "existing_job_name": existing_job_name,
                "files": files,
            }
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/structure-prediction/submit",
            body=await async_maybe_transform(body, structure_prediction_submit_params.StructurePredictionSubmitParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class StructurePredictionResourceWithRawResponse:
    def __init__(self, structure_prediction: StructurePredictionResource) -> None:
        self._structure_prediction = structure_prediction

        self.get_results = to_raw_response_wrapper(
            structure_prediction.get_results,
        )
        self.get_status = to_raw_response_wrapper(
            structure_prediction.get_status,
        )
        self.submit = to_raw_response_wrapper(
            structure_prediction.submit,
        )


class AsyncStructurePredictionResourceWithRawResponse:
    def __init__(self, structure_prediction: AsyncStructurePredictionResource) -> None:
        self._structure_prediction = structure_prediction

        self.get_results = async_to_raw_response_wrapper(
            structure_prediction.get_results,
        )
        self.get_status = async_to_raw_response_wrapper(
            structure_prediction.get_status,
        )
        self.submit = async_to_raw_response_wrapper(
            structure_prediction.submit,
        )


class StructurePredictionResourceWithStreamingResponse:
    def __init__(self, structure_prediction: StructurePredictionResource) -> None:
        self._structure_prediction = structure_prediction

        self.get_results = to_streamed_response_wrapper(
            structure_prediction.get_results,
        )
        self.get_status = to_streamed_response_wrapper(
            structure_prediction.get_status,
        )
        self.submit = to_streamed_response_wrapper(
            structure_prediction.submit,
        )


class AsyncStructurePredictionResourceWithStreamingResponse:
    def __init__(self, structure_prediction: AsyncStructurePredictionResource) -> None:
        self._structure_prediction = structure_prediction

        self.get_results = async_to_streamed_response_wrapper(
            structure_prediction.get_results,
        )
        self.get_status = async_to_streamed_response_wrapper(
            structure_prediction.get_status,
        )
        self.submit = async_to_streamed_response_wrapper(
            structure_prediction.submit,
        )
