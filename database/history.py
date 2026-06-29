import aiosqlite

async def get_active_months(db: aiosqlite.Connection, user_id: int):
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
        SELECT id, start_time
        FROM workouts
        WHERE user_id = ? AND end_time IS NOT NULL
        AND strftime('%Y-%m', start_time) = ?
        ORDER BY start_time DESC
        """,
            (user_id, year_month)
    ) as cursor:
        return await cursor.fetchall()

async def get_workout_details(db: aiosqlite.Connection, workout_id: int):
    async with db.execute(
        """
        SELECT e.name, ws.set_number, ws.weight, ws.reps
        FROM workout_sets ws
        JOIN exercises e ON ws.exercise_id = e.id
        WHERE ws.workout_id = ?
        ORDER BY ws.id ASC
        """,
        (workout_id,)
    ) as cursor:
        return await cursor.fetchall()