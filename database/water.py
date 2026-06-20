import aiosqlite


async def add_water(db: aiosqlite.Connection, user_id: int, amount_ml: int) -> None:
    await db.execute(
        "INSERT INTO water_logs (user_id, amount_ml) VALUES (?, ?)",
        (user_id, amount_ml)
    )
    await db.commit()

async def get_today_water(db: aiosqlite.Connection, user_id: int) -> int:
    async with db.execute(
        """
        SELECT SUM(amount_ml) FROM water_logs
        WHERE user_id = ? AND date(timestamp) = date('now')
        """,
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row[0] if row and row[0] is not None else 0

async def delete_last_water(db: aiosqlite.Connection, user_id: int) -> bool:
    async with db.execute(
        """
        SELECT id FROM water_logs
        WHERE user_id = ? and date(timestamp) = date('now')
        ORDER BY id DESC LIMIT 1
        """,
            (user_id,)
    ) as cursor:
        row = await cursor.fetchone()

    if row:
        last_id = row[0]
        await db.execute("DELETE FROM water_logs WHERE id = ?", (last_id,))
        await db.commit()
        return True
    return False
