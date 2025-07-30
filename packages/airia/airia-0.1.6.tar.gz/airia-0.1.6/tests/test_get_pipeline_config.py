from unittest.mock import patch

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from airia import AiriaAPIError, AiriaAsyncClient, AiriaClient
from airia.types import GetPipelineConfigResponse

# Load environment variables for testing
load_dotenv()
PYTHON_PIPELINE = "0134da17-c5a5-4730-a576-92f8eaf0926f"


@pytest.fixture
def sync_client():
    return AiriaClient(log_requests=True)


@pytest_asyncio.fixture
async def async_client():
    return AiriaAsyncClient(log_requests=True)


# Mock response data for testing
MOCK_PIPELINE_CONFIG_RESPONSE = {
    "deploymentId": None,
    "deploymentName": None,
    "deploymentDescription": None,
    "userKeys": {},
    "groupKeys": {},
    "agentIcon": None,
    "external": False,
    "activeVersionId": "6e98f6ae-d666-4db0-9495-b5b40e45b482",
    "name": "Python Block Test",
    "executionName": "python_block_test",
    "description": "",
    "videoLink": None,
    "agentIconId": None,
    "versions": [
        {
            "pipelineId": "0134da17-c5a5-4730-a576-92f8eaf0926f",
            "majorVersion": 1,
            "minorVersion": 0,
            "versionNumber": "1.00",
            "isDraftVersion": False,
            "isLatest": False,
            "steps": None,
            "alignment": "Horizontal",
            "id": "1756d834-4c2a-4271-beff-b6a1b8b4737f",
            "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
            "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
            "createdAt": "2025-03-26T20:33:31.9410340Z",
            "updatedAt": "2025-03-26T22:37:25.8345390Z",
            "userId": "9f7e215f-5563-414e-9635-570efa078c35",
        },
        {
            "pipelineId": "0134da17-c5a5-4730-a576-92f8eaf0926f",
            "majorVersion": 2,
            "minorVersion": 0,
            "versionNumber": "2.00",
            "isDraftVersion": False,
            "isLatest": False,
            "steps": None,
            "alignment": "Horizontal",
            "id": "0ac78be5-182c-4350-b5a9-128fb8904ded",
            "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
            "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
            "createdAt": "2025-03-26T22:37:25.8318150Z",
            "updatedAt": "2025-03-26T22:40:49.4444470Z",
            "userId": "9f7e215f-5563-414e-9635-570efa078c35",
        },
        {
            "pipelineId": "0134da17-c5a5-4730-a576-92f8eaf0926f",
            "majorVersion": 3,
            "minorVersion": 0,
            "versionNumber": "3.00",
            "isDraftVersion": False,
            "isLatest": False,
            "steps": None,
            "alignment": "Horizontal",
            "id": "8b4cff91-22c9-4f49-8d56-c7679e97d896",
            "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
            "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
            "createdAt": "2025-03-26T22:40:49.4406740Z",
            "updatedAt": "2025-03-26T22:50:14.2888930Z",
            "userId": "9f7e215f-5563-414e-9635-570efa078c35",
        },
        {
            "pipelineId": "0134da17-c5a5-4730-a576-92f8eaf0926f",
            "majorVersion": 4,
            "minorVersion": 0,
            "versionNumber": "4.00",
            "isDraftVersion": False,
            "isLatest": False,
            "steps": None,
            "alignment": "Horizontal",
            "id": "a51ab51f-f680-46fe-bb92-9ccdf35d05ab",
            "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
            "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
            "createdAt": "2025-03-26T22:50:53.2168600Z",
            "updatedAt": "2025-03-26T23:52:29.1746240Z",
            "userId": "9f7e215f-5563-414e-9635-570efa078c35",
        },
        {
            "pipelineId": "0134da17-c5a5-4730-a576-92f8eaf0926f",
            "majorVersion": 5,
            "minorVersion": 0,
            "versionNumber": "5.00",
            "isDraftVersion": False,
            "isLatest": True,
            "steps": None,
            "alignment": "Horizontal",
            "id": "6e98f6ae-d666-4db0-9495-b5b40e45b482",
            "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
            "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
            "createdAt": "2025-03-26T23:52:29.1722390Z",
            "updatedAt": "2025-03-26T23:52:29.1746230Z",
            "userId": "9f7e215f-5563-414e-9635-570efa078c35",
        },
    ],
    "executionStats": {"successCount": 1039, "failureCount": 1},
    "industry": None,
    "subIndustries": [],
    "agentDetails": {},
    "agentDetailsTags": [],
    "activeVersion": {
        "pipelineId": "0134da17-c5a5-4730-a576-92f8eaf0926f",
        "majorVersion": 5,
        "minorVersion": 0,
        "versionNumber": "5.00",
        "isDraftVersion": False,
        "isLatest": True,
        "steps": [
            {
                "code": '"""\nThis Block processes input data and client context to produce an output.\n\nAvailable Variables:\n- input (str): Input from previous steps.\n- client_data (dict): Contains user context with the following keys:\n    - user_id (str): The user\'s unique identifier.\n    - conversation_id (str): The conversation\'s unique identifier.\n    - user_input (str): The user\'s input text.\n    - user_roles (List[str]): The user\'s roles.\n    - user_groups (List[str]): The user\'s groups.\n    - images (List[str]): An array of image URLs.\n    - additional_info (List[Any]): an array of objects containing additional information passed to the agent.\n    - step_inputs (List[Any]): The inputs for the current step.\n    - files (List[str]): The files associated with the request.    \n- execution_parameters (dict): Contains the following keys:\n    - execution_id (str): The unique identifier for the execution.\n    - step_results_by_type (dict): A dictionary containing the results of the previous steps, ordered by completion, with the following keys:\n       - model (List[Any]): The results of the model steps.\n       - data_source (List[Any]): The results of the data search steps.\n       - memory_load (List[Any]): The results of the memory load steps.\n       - memory_store (List[Any]): The results of the memory store steps.    \n       - python (List[Any]): The results of the python steps.\n       - router (List[Any]): The results of the router steps.\n       - tool_action (List[Any]): The results of the tool action steps.\n       - agent (List[Any]): The results of the agent steps.\n                     \nReturns:\n- output (str): The processed output, initially set to the input value.\n"""\n\n# Your code here\noutput = input  # Assign your output to this variable\n\nif len(client_data["images"]) > 0:\n    output = f\'{len(client_data["images"])} images\'\n\nif len(client_data["files"]) > 0:\n    output = f\'{len(client_data["files"])} files\'\n\nif len(client_data["additional_info"]) > 0:\n    output = str(client_data["additional_info"])\n',
                "stepType": "pythonStep",
                "position": None,
                "positionId": "a8c9cfa0-6313-4f1b-a28b-cdd2350b05d3",
                "handles": [
                    {
                        "pipelineStepId": "48c1e273-e1ba-47df-a713-35eee1c2d7d7",
                        "uuid": "198db5b2-75d6-4fe1-92d9-b347207449a4",
                        "type": "source",
                        "label": "",
                        "tooltip": "",
                        "x": 255.9375,
                        "y": 47.738647,
                        "id": "95f413c2-0e3f-47c5-af31-38549dd72bef",
                        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                        "projectId": "00000000-0000-0000-0000-000000000000",
                        "createdAt": "2025-03-26T23:52:29.1722350Z",
                        "updatedAt": "2025-03-26T23:52:29.1746230Z",
                        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
                    },
                    {
                        "pipelineStepId": "48c1e273-e1ba-47df-a713-35eee1c2d7d7",
                        "uuid": "ca16a5b9-f32e-454d-873d-1e9efa0ce167",
                        "type": "target",
                        "label": "",
                        "tooltip": "",
                        "x": -5.4454956,
                        "y": 47.738647,
                        "id": "fc0b1989-1e49-4e3c-8f22-094426513669",
                        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                        "projectId": "00000000-0000-0000-0000-000000000000",
                        "createdAt": "2025-03-26T23:52:29.1722360Z",
                        "updatedAt": "2025-03-26T23:52:29.1746230Z",
                        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
                    },
                ],
                "dependenciesObject": [
                    {
                        "pipelineStepId": "48c1e273-e1ba-47df-a713-35eee1c2d7d7",
                        "parentId": "ae8b9ff8-7f95-4b62-9fde-2c7127448a10",
                        "parentHandleId": "b81a7e4e-3e55-4797-889d-a4f6015cab9b",
                        "handleId": "ca16a5b9-f32e-454d-873d-1e9efa0ce167",
                        "id": "e59f33f2-33c8-4b04-a2cd-3df416979771",
                        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                        "projectId": "00000000-0000-0000-0000-000000000000",
                        "createdAt": "2025-03-26T23:52:29.1722330Z",
                        "updatedAt": "2025-03-26T23:52:29.1746230Z",
                        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
                    }
                ],
                "pipelineVersionId": "6e98f6ae-d666-4db0-9495-b5b40e45b482",
                "stepTitle": "Python Code",
                "id": "48c1e273-e1ba-47df-a713-35eee1c2d7d7",
                "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
                "createdAt": "2025-03-26T20:33:31.9370040Z",
                "updatedAt": "2025-03-26T23:52:29.1746230Z",
                "userId": "9f7e215f-5563-414e-9635-570efa078c35",
            },
            {
                "stepType": "outputStep",
                "position": None,
                "positionId": "fef7c865-1b6e-4896-b1c4-7d89fbfad260",
                "handles": [
                    {
                        "pipelineStepId": "a0f14314-602d-46d8-b6be-d350865231c9",
                        "uuid": "b5de5347-6897-4414-ae3c-0d4f513f6461",
                        "type": "target",
                        "label": "",
                        "tooltip": "",
                        "x": -5.4453125,
                        "y": 32.491364,
                        "id": "95be20fa-a8d0-40a8-9047-20cb7546c8e7",
                        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                        "projectId": "00000000-0000-0000-0000-000000000000",
                        "createdAt": "2025-03-26T23:52:29.1722320Z",
                        "updatedAt": "2025-03-26T23:52:29.1746230Z",
                        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
                    }
                ],
                "dependenciesObject": [
                    {
                        "pipelineStepId": "a0f14314-602d-46d8-b6be-d350865231c9",
                        "parentId": "48c1e273-e1ba-47df-a713-35eee1c2d7d7",
                        "parentHandleId": "198db5b2-75d6-4fe1-92d9-b347207449a4",
                        "handleId": "b5de5347-6897-4414-ae3c-0d4f513f6461",
                        "id": "c11e97cf-994d-479a-97da-195a60c3bef0",
                        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                        "projectId": "00000000-0000-0000-0000-000000000000",
                        "createdAt": "2025-03-26T23:52:29.1722290Z",
                        "updatedAt": "2025-03-26T23:52:29.1746230Z",
                        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
                    }
                ],
                "pipelineVersionId": "6e98f6ae-d666-4db0-9495-b5b40e45b482",
                "stepTitle": "Output",
                "id": "a0f14314-602d-46d8-b6be-d350865231c9",
                "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
                "createdAt": "2025-03-26T20:33:31.9369710Z",
                "updatedAt": "2025-03-26T23:52:29.1746230Z",
                "userId": "9f7e215f-5563-414e-9635-570efa078c35",
            },
            {
                "inputVariables": [],
                "inputTemplate": None,
                "stepType": "inputStep",
                "position": None,
                "positionId": "b7e17fb7-1ee4-42e3-803b-6d3053673f23",
                "handles": [
                    {
                        "pipelineStepId": "ae8b9ff8-7f95-4b62-9fde-2c7127448a10",
                        "uuid": "b81a7e4e-3e55-4797-889d-a4f6015cab9b",
                        "type": "source",
                        "label": "",
                        "tooltip": "",
                        "x": 255.93744,
                        "y": 32.491364,
                        "id": "b6be5af9-7534-450f-850b-14cb7ad654bf",
                        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                        "projectId": "00000000-0000-0000-0000-000000000000",
                        "createdAt": "2025-03-26T23:52:29.1722380Z",
                        "updatedAt": "2025-03-26T23:52:29.1746240Z",
                        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
                    }
                ],
                "dependenciesObject": [],
                "pipelineVersionId": "6e98f6ae-d666-4db0-9495-b5b40e45b482",
                "stepTitle": "Input",
                "id": "ae8b9ff8-7f95-4b62-9fde-2c7127448a10",
                "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
                "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
                "createdAt": "2025-03-26T20:33:31.9369340Z",
                "updatedAt": "2025-03-26T23:52:29.1746230Z",
                "userId": "9f7e215f-5563-414e-9635-570efa078c35",
            },
        ],
        "alignment": "Horizontal",
        "id": "6e98f6ae-d666-4db0-9495-b5b40e45b482",
        "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
        "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
        "createdAt": "2025-03-26T23:52:29.1722390Z",
        "updatedAt": "2025-03-26T23:52:29.1746230Z",
        "userId": "9f7e215f-5563-414e-9635-570efa078c35",
    },
    "backupPipelineId": None,
    "deployment": None,
    "libraryAgentId": None,
    "libraryImportedHash": None,
    "libraryImportedVersion": None,
    "isDeleted": None,
    "agentTrigger": None,
    "apiKeyId": None,
    "isSeeded": False,
    "behaviours": [],
    "id": "0134da17-c5a5-4730-a576-92f8eaf0926f",
    "tenantId": "2ce49ae0-c3ff-421a-91b7-830d0c73b348",
    "projectId": "01948f99-f78a-7415-a187-b250c6e04458",
    "createdAt": "2025-03-26T20:33:31.9410260Z",
    "updatedAt": "2025-03-26T23:52:31.1933780Z",
    "userId": "9f7e215f-5563-414e-9635-570efa078c35",
}


class TestSyncGetPipelineConfig:
    """Test cases for synchronous get_pipeline_config method."""

    def test_get_pipeline_config_success(self, sync_client: AiriaClient):
        """Test successful pipeline configuration retrieval."""
        response = sync_client.get_pipeline_config(pipeline_id=PYTHON_PIPELINE)
        # Verify the response is properly typed
        assert isinstance(response, GetPipelineConfigResponse)

    def test_get_pipeline_config_with_custom_api_version(
        self, sync_client: AiriaClient
    ):
        """Test pipeline configuration retrieval with custom API version."""
        with patch.object(sync_client, "_make_request") as mock_request:
            mock_request.return_value = MOCK_PIPELINE_CONFIG_RESPONSE

            response = sync_client.get_pipeline_config(
                pipeline_id="test-pipeline-123", api_version="v1"
            )

            assert isinstance(response, GetPipelineConfigResponse)

    def test_get_pipeline_config_with_correlation_id(self, sync_client: AiriaClient):
        """Test pipeline configuration retrieval with custom correlation ID."""
        with patch.object(sync_client, "_make_request") as mock_request:
            mock_request.return_value = MOCK_PIPELINE_CONFIG_RESPONSE

            custom_correlation_id = "test-correlation-123"
            response = sync_client.get_pipeline_config(
                pipeline_id="test-pipeline-123", correlation_id=custom_correlation_id
            )

            assert isinstance(response, GetPipelineConfigResponse)

    def test_get_pipeline_config_invalid_api_version(self, sync_client: AiriaClient):
        """Test that invalid API version raises ValueError."""
        with pytest.raises(ValueError, match="Invalid API version"):
            sync_client.get_pipeline_config(
                pipeline_id="test-pipeline-123", api_version="invalid_version"
            )

    def test_get_pipeline_config_api_error(self, sync_client: AiriaClient):
        """Test handling of API errors."""
        with patch.object(sync_client, "_make_request") as mock_request:
            mock_request.side_effect = AiriaAPIError(
                status_code=404, message="Pipeline not found"
            )

            with pytest.raises(AiriaAPIError) as exc_info:
                sync_client.get_pipeline_config(pipeline_id="nonexistent-pipeline")

            assert exc_info.value.status_code == 404
            assert "Pipeline not found" in str(exc_info.value)


class TestAsyncGetPipelineConfig:
    """Test cases for asynchronous get_pipeline_config method."""

    @pytest.mark.asyncio
    async def test_get_pipeline_config_success(self, async_client: AiriaAsyncClient):
        """Test successful asynchronous pipeline configuration retrieval."""
        response = await async_client.get_pipeline_config(pipeline_id=PYTHON_PIPELINE)

        # Verify the response is properly typed
        assert isinstance(response, GetPipelineConfigResponse)

    @pytest.mark.asyncio
    async def test_get_pipeline_config_with_custom_params(
        self, async_client: AiriaAsyncClient
    ):
        """Test asynchronous pipeline configuration retrieval with custom parameters."""
        with patch.object(async_client, "_make_request") as mock_request:
            mock_request.return_value = MOCK_PIPELINE_CONFIG_RESPONSE

            response = await async_client.get_pipeline_config(
                pipeline_id="test-pipeline-123",
                api_version="v1",
                correlation_id="async-test-correlation",
            )

            assert isinstance(response, GetPipelineConfigResponse)

    @pytest.mark.asyncio
    async def test_get_pipeline_config_api_error(self, async_client: AiriaAsyncClient):
        """Test handling of API errors in async context."""
        with patch.object(async_client, "_make_request") as mock_request:
            mock_request.side_effect = AiriaAPIError(
                status_code=403, message="Access forbidden"
            )

            with pytest.raises(AiriaAPIError) as exc_info:
                await async_client.get_pipeline_config(pipeline_id="forbidden-pipeline")

            assert exc_info.value.status_code == 403
            assert "Access forbidden" in str(exc_info.value)
