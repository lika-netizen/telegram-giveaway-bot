from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

@app.get("/confirm")
async def confirm(request: Request, tg_id: str):
    ip = request.client.host
    conn = sqlite3.connect("ip_log.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS access (ip TEXT, tg_id TEXT)")
    cursor.execute("INSERT INTO access (ip, tg_id) VALUES (?, ?)", (ip, tg_id))
    conn.commit()
    cursor.execute("SELECT COUNT(DISTINCT tg_id) FROM access WHERE ip=?", (ip,))
    count = cursor.fetchone()[0]
    if count > 2:
        return {"status": "error", "message": "С одного IP уже зарегистрировано 2 участника"}
    return {"status": "success", "message": "Участие подтверждено"}
