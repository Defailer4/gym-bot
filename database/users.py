from asyncio.windows_events import NULL
from typing import Optional
import aiosqlite


async def get_user(db: aiosqlite.Connection, user_id: int) -> Optional[tuple]:
    async with db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)) as cursor:
        return await cursor.fetchone()


async def add_user(db: aiosqlite.Connection, user_id: int) -> None:
    await db.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )
    await db.commit()



async def update_water_goal(db: aiosqlite.Connection, user_id: int, new_goal: int) -> None:
    await db.execute(
        "UPDATE users SET water_goal = ? WHERE user_id = ?",
        (new_goal, user_id,)
    )
    await db.commit()

async def update_weight_goal(db: aiosqlite.Connection, user_id: int, new_goal: float) -> None:
    await db.execute(
        "UPDATE users SET weight_goal = ? WHERE user_id = ?",
        (new_goal, user_id,)
    )
    await db.commit()

async def get_user_goals(db: aiosqlite.Connection, user_id: int) -> tuple[int, float] | None:
    async with db.execute(
        "SELECT water_goal, weight_goal FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row if row else (2500, None)