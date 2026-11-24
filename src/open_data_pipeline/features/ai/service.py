from open_data_pipeline.features.ai.client import generate_response
from open_data_pipeline.features.ai.prompts import SYSTEM_PROMPT
from open_data_pipeline.features.ai.schemas import AssistantResponse


async def process_message(message: str) -> AssistantResponse:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]

    response_schema = AssistantResponse.model_json_schema()

    response = await generate_response(
        messages=messages, response_schema=response_schema
    )

    return AssistantResponse.model_validate_json(response)
