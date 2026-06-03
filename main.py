from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from game import create_room, join_room, rooms
import os

app = FastAPI()

HTML_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")

# room_id -> { player_id -> WebSocket }
connections: dict[str, dict[str, WebSocket]] = {}


async def broadcast(room_id: str):
    room = rooms.get(room_id)
    if not room or room_id not in connections:
        return
    for pid, ws in list(connections[room_id].items()):
        try:
            await ws.send_json(room.to_dict(for_player_id=pid))
        except Exception:
            pass


class NameBody(BaseModel):
    name: str = "بازیکن"


@app.get("/")
async def index():
    with open(HTML_PATH, encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/api/create")
async def api_create(body: NameBody):
    room, player = create_room(body.name.strip() or "Player")
    return {"room_id": room.id, "player_id": player.id}


@app.post("/api/join/{room_id}")
async def api_join(room_id: str, body: NameBody):
    room, player, err = join_room(room_id, body.name.strip() or "Player")
    if err:
        return JSONResponse({"error": err}, status_code=400)
    await broadcast(room.id)
    return {"room_id": room.id, "player_id": player.id}


@app.websocket("/ws/{room_id}/{player_id}")
async def ws_endpoint(ws: WebSocket, room_id: str, player_id: str):
    await ws.accept()
    room = rooms.get(room_id)
    if not room:
        await ws.send_json({"error": "room_not_found"})
        await ws.close()
        return

    connections.setdefault(room_id, {})[player_id] = ws
    await ws.send_json(room.to_dict(for_player_id=player_id))

    try:
        while True:
            data = await ws.receive_json()
            action = data.get("action")

            if action == "set_mode":
                if room.state == "lobby" and player_id == room.host_id():
                    room.game_mode = data.get("mode", "faztoumim")
                    await broadcast(room_id)

            elif action == "start":
                if room.state == "lobby" and len(room.players) >= 2 and player_id == room.host_id():
                    if room.game_mode == "who":
                        room.start_who(int(data.get("rounds", 10)))
                    elif room.game_mode == "wl":
                        room.start_wl(int(data.get("rounds", 8)))
                    else:
                        room.game_mode = "faztoumim"
                        rpp = int(data.get("rounds_per_player", 1))
                        room.begin_game(rpp)
                    await broadcast(room_id)

            elif action == "actor_done":
                actor = room.current_actor()
                if room.state == "acting" and actor and actor.id == player_id:
                    room.actor_done()
                    await broadcast(room_id)

            elif action == "guess":
                if room.state == "guessing":
                    all_in = room.submit_guess(player_id, data.get("mood", ""))
                    if all_in:
                        room.do_reveal()
                    await broadcast(room_id)

            elif action == "next_round":
                if room.state == "reveal" and player_id == room.host_id():
                    room.next_round()
                    await broadcast(room_id)

            elif action == "play_again":
                if room.state == "ended" and player_id == room.host_id():
                    rpp = int(data.get("rounds_per_player", 1))
                    room.play_again(rpp)
                    await broadcast(room_id)

            # ── کدوم‌تون بیشتر actions ────────────────
            elif action == "who_launch":
                if room.state == "who_preparing" and player_id == room.host_id():
                    room.who_launch(data.get("custom_q", ""))
                    await broadcast(room_id)

            elif action == "who_vote":
                if room.state == "who_voting":
                    all_in = room.who_vote(player_id, data.get("target_id", ""))
                    if all_in:
                        room.who_reveal()
                    await broadcast(room_id)

            elif action == "who_tiebreak_vote":
                if room.state == "who_tiebreak":
                    all_in = room.who_tiebreak_vote(player_id, data.get("target_id", ""))
                    if all_in:
                        room.who_tiebreak_reveal()
                    await broadcast(room_id)

            elif action == "who_next":
                if room.state == "who_reveal" and player_id == room.host_id():
                    room.who_next()
                    await broadcast(room_id)

            elif action == "who_play_again":
                if room.state == "who_ended" and player_id == room.host_id():
                    room.who_play_again(int(data.get("rounds", 10)))
                    await broadcast(room_id)

            # ── خط کیه؟ actions ──────────────────────────
            elif action == "wl_submit_answer":
                if room.state == "wl_writing":
                    all_in = room.wl_submit(player_id, data.get("answer", ""))
                    if all_in:
                        room.wl_move_to_vote()
                    await broadcast(room_id)

            elif action == "wl_move_to_vote":
                if room.state == "wl_writing" and player_id == room.host_id():
                    if room.wl_answers:
                        room.wl_move_to_vote()
                    else:
                        room.wl_next()
                    await broadcast(room_id)

            elif action == "wl_vote":
                if room.state == "wl_voting":
                    all_in = room.wl_vote(player_id, data.get("target_id", ""))
                    if all_in:
                        room.wl_do_reveal()
                    await broadcast(room_id)

            elif action == "wl_tiebreak_vote":
                if room.state == "wl_tiebreak":
                    all_in = room.wl_tiebreak_vote(player_id, data.get("target_id", ""))
                    if all_in:
                        room.wl_tiebreak_reveal()
                    await broadcast(room_id)

            elif action == "wl_next":
                if room.state == "wl_reveal" and player_id == room.host_id():
                    room.wl_next()
                    await broadcast(room_id)

            elif action == "wl_play_again":
                if room.state == "wl_ended" and player_id == room.host_id():
                    room.wl_play_again(int(data.get("rounds", 8)))
                    await broadcast(room_id)

            elif action == "exit":
                # Explicit leave — remove player from room
                connections.get(room_id, {}).pop(player_id, None)
                room.players = [p for p in room.players if p.id != player_id]
                if not room.players:
                    connections.pop(room_id, None)
                    rooms.pop(room_id, None)
                else:
                    await broadcast(room_id)
                return

    except WebSocketDisconnect:
        # Keep the player in the room so they can reconnect after a refresh.
        # Only remove their websocket from the active connections.
        connections.get(room_id, {}).pop(player_id, None)
        if not connections.get(room_id):
            connections.pop(room_id, None)
