import aiosqlite

async def get_weight_history(db: aiosqlite.Connection, user_id: int):
    async with db.execute(
        """
        SELECT timestamp, weight
        FROM user_weight_logs
        WHERE user_id = ?
        ORDER BY timestamp ASC
        """,
        (user_id,)
    ) as cursor:
        return await cursor.fetchall()