# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gitpod import Gitpod, AsyncGitpod
from tests.utils import assert_matches_type
from gitpod.pagination import SyncPoliciesPage, AsyncPoliciesPage
from gitpod.types.projects import (
    ProjectPolicy,
    PolicyCreateResponse,
    PolicyUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPolicies:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Gitpod) -> None:
        policy = client.projects.policies.create()
        assert_matches_type(PolicyCreateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Gitpod) -> None:
        policy = client.projects.policies.create(
            group_id="f53d2330-3795-4c5d-a1f3-453121af9c60",
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
            role="PROJECT_ROLE_ADMIN",
        )
        assert_matches_type(PolicyCreateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Gitpod) -> None:
        response = client.projects.policies.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(PolicyCreateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Gitpod) -> None:
        with client.projects.policies.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(PolicyCreateResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Gitpod) -> None:
        policy = client.projects.policies.update()
        assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Gitpod) -> None:
        policy = client.projects.policies.update(
            group_id="f53d2330-3795-4c5d-a1f3-453121af9c60",
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
            role="PROJECT_ROLE_EDITOR",
        )
        assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Gitpod) -> None:
        response = client.projects.policies.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Gitpod) -> None:
        with client.projects.policies.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Gitpod) -> None:
        policy = client.projects.policies.list()
        assert_matches_type(SyncPoliciesPage[ProjectPolicy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Gitpod) -> None:
        policy = client.projects.policies.list(
            token="token",
            page_size=0,
            pagination={
                "token": "token",
                "page_size": 20,
            },
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
        )
        assert_matches_type(SyncPoliciesPage[ProjectPolicy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Gitpod) -> None:
        response = client.projects.policies.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(SyncPoliciesPage[ProjectPolicy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Gitpod) -> None:
        with client.projects.policies.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(SyncPoliciesPage[ProjectPolicy], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Gitpod) -> None:
        policy = client.projects.policies.delete()
        assert_matches_type(object, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_with_all_params(self, client: Gitpod) -> None:
        policy = client.projects.policies.delete(
            group_id="f53d2330-3795-4c5d-a1f3-453121af9c60",
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
        )
        assert_matches_type(object, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Gitpod) -> None:
        response = client.projects.policies.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(object, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Gitpod) -> None:
        with client.projects.policies.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(object, policy, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPolicies:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.create()
        assert_matches_type(PolicyCreateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.create(
            group_id="f53d2330-3795-4c5d-a1f3-453121af9c60",
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
            role="PROJECT_ROLE_ADMIN",
        )
        assert_matches_type(PolicyCreateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGitpod) -> None:
        response = await async_client.projects.policies.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(PolicyCreateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGitpod) -> None:
        async with async_client.projects.policies.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(PolicyCreateResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.update()
        assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.update(
            group_id="f53d2330-3795-4c5d-a1f3-453121af9c60",
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
            role="PROJECT_ROLE_EDITOR",
        )
        assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncGitpod) -> None:
        response = await async_client.projects.policies.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncGitpod) -> None:
        async with async_client.projects.policies.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(PolicyUpdateResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.list()
        assert_matches_type(AsyncPoliciesPage[ProjectPolicy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.list(
            token="token",
            page_size=0,
            pagination={
                "token": "token",
                "page_size": 20,
            },
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
        )
        assert_matches_type(AsyncPoliciesPage[ProjectPolicy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGitpod) -> None:
        response = await async_client.projects.policies.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(AsyncPoliciesPage[ProjectPolicy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGitpod) -> None:
        async with async_client.projects.policies.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(AsyncPoliciesPage[ProjectPolicy], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.delete()
        assert_matches_type(object, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncGitpod) -> None:
        policy = await async_client.projects.policies.delete(
            group_id="f53d2330-3795-4c5d-a1f3-453121af9c60",
            project_id="b0e12f6c-4c67-429d-a4a6-d9838b5da047",
        )
        assert_matches_type(object, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncGitpod) -> None:
        response = await async_client.projects.policies.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(object, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncGitpod) -> None:
        async with async_client.projects.policies.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(object, policy, path=["response"])

        assert cast(Any, response.is_closed) is True
