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

async def get_water_history(db:aiosqlite.Connection, user_id: int, limit: int = 7):
    async with db.execute(
        """
        SELECT DATE(timestamp) as log_date, SUM(amount_ml) as total_ml
        FROM water_logs
        WHERE user_id = ?
        GROUP BY log_date
        ORDER BY log_date ASC
        LIMIT ?
        """,
        (user_id, limit)
    ) as cursor:
        return await cursor.fetchall()