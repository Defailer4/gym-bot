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