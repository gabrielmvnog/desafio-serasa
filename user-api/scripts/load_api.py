import asyncio

import httpx

from app.users.schemas import UserIn

URL = "http://localhost:8000/users"
USERS = [
    UserIn(
        name="José",
        cpf="41964287030",
        email="jose@gmail.com",
        phone_number="+12029182132",
    )
]


async def main():
    async with httpx.AsyncClient() as client:
        for i, user in enumerate(USERS * 100):
            response = await client.put(URL + f"/{i}", json=user.dict())
            print(response.status_code)

    return


asyncio.run(main())
