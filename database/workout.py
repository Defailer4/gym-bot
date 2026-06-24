import aiosqlite


async def get_active_workout(db: aiosqlite.Connection, user_id: int) -> int | None:
    async with db.execute("""
        SELECT id FROM workouts 
        WHERE user_id = ? 
        AND end_time IS NULL LIMIT 1
        """,
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None

async def create_workout(db : aiosqlite.Connection, user_id: int) -> int:
    async with db.execute(
        "INSERT INTO workouts (user_id) VALUES (?)",
        (user_id,)
    ) as cursor:
        await db.commit()
        return cursor.lastrowid

async def get_exercises_by_category(db: aiosqlite.Connection, category: str , user_id: int) -> list:
    async with db.execute(
        """
        SELECT id, name FROM exercises 
        WHERE category = ? AND (user_ID IS NULL OR user_id = ?)
        """,
        (category, user_id)
    ) as cursor:
        return await cursor.fetchall()

async def cancel_workout(db: aiosqlite.Connection, workout_id: int):
    async with db.execute("DELETE FROM workouts WHERE id = ?", (workout_id,)):
        await db.commit()

async def add_workout_set(db: aiosqlite.Connection, workout_id: int, exercise_id: int, weight: float, reps: int):
    async with db.execute(
        "SELECT COUNT(*) FROM workout_sets WHERE workout_id = ? AND exercise_id = ?",
        (workout_id, exercise_id)
    ) as cursor:
        result = await cursor.fetchone()
        next_set = result[0] + 1

    await db.execute(
        "INSERT INTO workout_sets (workout_id, exercise_id, set_number, weight, reps) VALUES (?, ?, ?, ?, ?)",
        (workout_id, exercise_id, next_set, weight, reps)
    )
    await db.commit()

async def get_workout_sets(db: aiosqlite.Connection, workout_id: int, exercise_id: int) -> list:
    async with db.execute(
        "SELECT set_number, weight, reps FROM workout_sets WHERE workout_id = ? AND exercise_id = ? ORDER BY set_number",
            (workout_id, exercise_id)
    ) as cursor:
        return await cursor.fetchall()

async def undo_last_set(db:aiosqlite.Connection, workout_id: int, exercise_id: int):
    async with db.execute(
        "SELECT id FROM workout_sets WHERE workout_id = ? AND exercise_id = ? ORDER BY set_number DESC LIMIT 1",
        (workout_id, exercise_id)
    ) as cursor:
        last_set = await cursor.fetchone()

    if last_set:
        await db.execute("DELETE FROM workout_sets WHERE id = ?", (last_set[0],))
        await db.commit()

async def get_user_records(db: aiosqlite.Connection, user_id: int) -> dict:
    async with db.execute(
        """
        SELECT e.name, MAX(ws.weight) 
        FROM workout_sets ws
        JOIN workouts w ON ws.workout_id = w.id
        JOIN exercises e ON ws.exercise_id = e.id
        WHERE w.user_id = ?
        GROUP BY e.name
        """,
        (user_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        return {row[0]: row[1] for row in rows}

async def complete_workout(db: aiosqlite.Connection, workout_id: int):
    await db.execute(
        """
        UPDATE workouts 
        SET end_time = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (workout_id,)
    )
    await db.commit()

async def add_custom_exercise(db: aiosqlite.Connection, name: str, category: str, user_id: int) -> bool:
    async with db.execute("SELECT id FROM exercises WHERE LOWER(name) = ?", (name.lower(),)) as cursor:
        if await cursor.fetchone():
            return False

    await db.execute(
        "INSERT INTO exercises (name, category, user_id) VALUES (?, ?, ?)",
        (name, category, user_id),
    )
    await db.commit()
    return True