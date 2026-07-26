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


async def get_user_exercises_with_stats(db: aiosqlite.Connection, user_id: int):
    async with db.execute(
        """
        SELECT e.id, e.name
        FROM workout_sets ws
        JOIN workouts w ON ws.workout_id = w.id
        JOIN exercises e ON ws.exercise_id = e.id
        WHERE w.user_id = ?
        GROUP BY e.id, e.name
        HAVING COUNT(DISTINCT DATE(w.start_time)) >= 2
        """,
        (user_id,)
    ) as cursor:
        return await cursor.fetchall()

async def get_exercise_history_by_id(db: aiosqlite.Connection, user_id: int, exercise_id: int):
    async with db.execute("SELECT name FROM exercises WHERE id = ?", (exercise_id,)) as cursor:
        row = await cursor.fetchone()
        exercise_name = row[0] if row else "Упражнение"

    async with db.execute(
        """
        SELECT DATE(w.start_time) as workout_date, MAX(ws.weight) as max_weight
        FROM workout_sets ws
        JOIN workouts w ON ws.workout_id = w.id
        WHERE w.user_id = ? AND ws.exercise_id = ?
        GROUP BY workout_date
        ORDER BY workout_date ASC
        """,
        (user_id, exercise_id)
    ) as cursor:
        history = await cursor.fetchall()
        return exercise_name, history