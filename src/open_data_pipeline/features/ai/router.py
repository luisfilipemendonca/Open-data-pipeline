from fastapi import APIRouter

from open_data_pipeline.features.ai.schemas import AssistantPayload, AssistantResponse
from open_data_pipeline.features.ai.service import process_message

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/")
async def process_message_endpoint(payload: AssistantPayload) -> AssistantResponse:
    return await process_message(message=payload.message)
