import asyncio
from g4f.client import AsyncClient


async def main():
    client = AsyncClient()

    response = await client.images.generate(
        prompt="a white Mercedes",
        model="flux",
        response_format="url"
        # Add any other necessary parameters
    )

    image_url = response.data[0].url
    print(f"Generated image URL: {image_url}")


asyncio.run(main())