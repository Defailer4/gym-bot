import aiosqlite

async def get_active_month(db: aiosqlite.Connection, user_id: int):
    async with db.execute(
        """
        SELECT DISTINCT strftime('%Y-%m', start_time) as ym
        FROM workouts
        WHERE user_id = ? AND end_time IS NOT NULL
        ORDER BY ym DESC
        """,
            (user_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def get_workout_by_month(db: aiosqlite.Connection, user_id: int, year_month):
    async with db.execute(
        """
        SELECT id, start_time,
        FROM workouts
        WHERE user_id = ? AND end_time IS NOT NULL
        AND strftime('%Y-%m', start_time) = ?
        ORDER BY start_time DESC
        """,
            (user_id, year_month)
    ) as cursor:
        return await cursor.fetchall()