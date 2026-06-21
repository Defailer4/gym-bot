import aiosqlite

async def add_weight(db: aiosqlite.Connection, user_id: int, weight: float) -> None:
    await db.execute(
        "INSERT INTO user_weight_logs (user_id, weight) VALUES (?, ?)",
        (user_id, weight)
    )
    await db.commit()

async def get_last_weight(db: aiosqlite.Connection, user_id: int) -> float | None:
    async with db.execute(
        "SELECT weight FROM user_weight_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1",
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_weight_history(db: aiosqlite.Connection, user_id: int, days: int ) -> list[tuple] | None:
    time_mod = f"-{days} days"
    async with db.execute(
        """
        SELECT date(timestamp), weight
        FROM user_weight_logs
        WHERE user_id = ? AND date(timestamp) >= date('now',?)
        ORDER BY timestamp ASC
        """,
        (user_id, time_mod)
    ) as cursor:
        rows = await cursor.fetchall()
        if not rows:
            return None

        return rows

async def delete_last_weight(db: aiosqlite.Connection, user_id: int) -> bool:
    async with db.execute(
        "SELECT id FROM user_weight_logs WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        if not row:
            return False
        last_id = row[0]

        await db.execute("DELETE FROM user_weight_logs WHERE id = ?", (last_id,))
        await db.commit()
        return True