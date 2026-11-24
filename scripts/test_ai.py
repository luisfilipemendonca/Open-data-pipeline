import asyncio

from open_data_pipeline.features.ai.service import process_message


async def main():
    message = "Abre os schemas"

    response = await process_message(message)

    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
