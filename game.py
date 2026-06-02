import random
from dataclasses import dataclass, field
from typing import Optional
import uuid

MOODS = [
    # originals
    {"name": "کنایی",           "emoji": "🙄", "color": "#6366f1"},
    {"name": "فلرت",            "emoji": "😏", "color": "#ec4899"},
    {"name": "عصبانی",          "emoji": "😡", "color": "#ef4444"},
    {"name": "غمگین",           "emoji": "😢", "color": "#3b82f6"},
    {"name": "هیجان‌زده",       "emoji": "🤩", "color": "#f59e0b"},
    {"name": "رسمی",            "emoji": "🧐", "color": "#475569"},
    {"name": "بچگانه",          "emoji": "🍼", "color": "#22c55e"},
    {"name": "شرور",            "emoji": "😈", "color": "#7c3aed"},
    # new
    {"name": "دیوا",            "emoji": "💅", "color": "#e879f9"},
    {"name": "مست",             "emoji": "🥴", "color": "#84cc16"},
    {"name": "ترسیده",          "emoji": "😱", "color": "#1e293b"},
    {"name": "اغراق‌آمیز",     "emoji": "🎭", "color": "#db2777"},
    {"name": "لهجه هندی",       "emoji": "🪷", "color": "#f97316"},
    {"name": "لهجه روسی",       "emoji": "🥶", "color": "#334155"},
    {"name": "لهجه عربی",       "emoji": "🫡", "color": "#15803d"},
    {"name": "لهجه اصفهانی",    "emoji": "🎶", "color": "#0891b2"},
    {"name": "لهجه شمالی",      "emoji": "🌊", "color": "#0d9488"},
    {"name": "لهجه سبزواری",    "emoji": "🌾", "color": "#b45309"},
]

SENTENCES = [
    # everyday
    "همه چیز خوبه",
    "اینترنت قطعه",
    "شام آماده‌ست",
    "ببخشید دیر کردم",
    "صبح بخیر همه",
    "فردا می‌بینمت",
    "خیلی خسته‌ام",
    "پیتزا تموم شد",
    "مامانم زنگ زد",
    "کسی میدونه پسورد وای‌فای چیه؟",
    "این لباس بهم میاد؟",
    "من رژیمم ولی فقط یه تیکه کوچیک",
    "پنجشنبه‌ست!",
    "یه چیزی توی آشپزخونه بو گرفت",
    "چرا همه انقدر بهم نگاه می‌کنن؟",
    "ماشینم خراب شد",
    "جیبم خالیه",
    # dramatic
    "یه چیزی دارم بهت بگم",
    "باید باهات حرف بزنم",
    "باورم نمیشه این کارو کردی",
    "این آخرین باره که اینو میگم",
    "باید یه راز بهت بگم",
    "چرا هیچکس منو درک نمیکنه؟",
    "دیگه نمیتونم ادامه بدم",
    "نمیفهمم چی شد",
    "داری بهم خیانت میکنی؟",
    "باور کن من آدم بدی نیستم",
    "می‌خوام باهات قهر کنم",
    "خواهش می‌کنم نرو",
    "این همون چیزیه که همیشه می‌خواستم",
    "نمیدونم چرا ولی داری گریم میاد",
    # work / achievement
    "امروز اخراجم کردن",
    "جلسه ۵ دقیقه دیگه شروع میشه",
    "تازه برنده لاتاری شدم",
    "میخوام استعفا بدم",
    "امتحانمو قبول شدم!",
    "اوه، یه جلسه دیگه",
    "این بهترین ایده‌ایه که تا حالا شنیدم",
    "باید زودتر میومدی",
    # feelings
    "خیلی دلم برات تنگ شده بود",
    "عاشقتم",
    "ازت متنفرم",
    "امروز خیلی خوشگلی",
    "فکر کنم گم شدم",
    "عصبانی نیستم، فقط ناامیدم",
    "یه لطف ازت می‌خوام",
    "فقط میخوام بخوابم",
    "می‌خوای بریم بیرون؟",
    "تولدمه!",
    "امروز بهترین روز زندگیمه",
    # random fun
    "فکر کنم فر رو روشن گذاشتم",
    "عاشق دوشنبه‌ام",
    "این غذا خوشمزه‌ترین چیزیه که تا حالا خوردم",
    "میشه یه کم ساکت باشی؟",
    "می‌تونی کمکم کنی؟",
]


@dataclass
class Player:
    id: str
    name: str
    score: int = 0


@dataclass
class Room:
    id: str
    players: list = field(default_factory=list)
    state: str = "lobby"
    actor_index: int = 0
    sentence: str = ""
    mood: dict = field(default_factory=dict)
    guesses: dict = field(default_factory=dict)
    rounds_played: int = 0
    max_rounds: int = 0
    _sentence_queue: list = field(default_factory=list)

    def host_id(self) -> Optional[str]:
        return self.players[0].id if self.players else None

    def current_actor(self) -> Optional[Player]:
        if self.players:
            return self.players[self.actor_index % len(self.players)]
        return None

    def _next_sentence(self) -> str:
        if not self._sentence_queue:
            self._sentence_queue = random.sample(SENTENCES, len(SENTENCES))
        return self._sentence_queue.pop()

    def start_round(self):
        self.sentence = self._next_sentence()
        self.mood = random.choice(MOODS)
        self.guesses = {}
        self.state = "acting"

    def begin_game(self, rounds_per_player: int = 1):
        rpp = max(1, min(rounds_per_player, 10))
        self.max_rounds = rpp * len(self.players)
        self._sentence_queue = random.sample(SENTENCES, len(SENTENCES))
        self.start_round()

    def actor_done(self):
        self.state = "guessing"

    def submit_guess(self, player_id: str, mood_name: str) -> bool:
        actor = self.current_actor()
        if not actor or player_id == actor.id:
            return False
        self.guesses[player_id] = mood_name
        non_actors = [p for p in self.players if p.id != actor.id]
        return len(self.guesses) >= len(non_actors)

    def do_reveal(self):
        self.state = "reveal"
        actor = self.current_actor()
        correct_mood = self.mood["name"]
        correct_count = sum(1 for g in self.guesses.values() if g == correct_mood)
        if actor:
            actor.score += correct_count  # actor earns 1 pt per correct guesser
        for player in self.players:
            if player.id in self.guesses and self.guesses[player.id] == correct_mood:
                player.score += 1        # correct guesser also earns 1 pt

    def next_round(self):
        self.rounds_played += 1
        self.actor_index = (self.actor_index + 1) % len(self.players)
        if self.rounds_played >= self.max_rounds:
            self.state = "ended"
        else:
            self.start_round()

    def play_again(self, rounds_per_player: int = 1):
        for p in self.players:
            p.score = 0
        self.rounds_played = 0
        self.actor_index = 0
        self.begin_game(rounds_per_player)

    def to_dict(self, for_player_id: str = None) -> dict:
        actor = self.current_actor()
        non_actors = [p for p in self.players if actor and p.id != actor.id]
        data = {
            "state":           self.state,
            "room_id":         self.id,
            "host_id":         self.host_id(),
            "players":         [{"id": p.id, "name": p.name, "score": p.score} for p in self.players],
            "actor_id":        actor.id if actor else None,
            "actor_name":      actor.name if actor else None,
            "sentence":        self.sentence,
            "mood_options":    MOODS,
            "guesses_count":   len(self.guesses),
            "non_actor_count": len(non_actors),
            "rounds_played":   self.rounds_played,
            "max_rounds":      self.max_rounds,
        }
        if for_player_id and actor and for_player_id == actor.id and self.state == "acting":
            data["secret_mood"] = self.mood
        if self.state == "guessing":
            data["guessed_ids"] = list(self.guesses.keys())
        if self.state in ("reveal", "ended"):
            data["revealed_mood"] = self.mood
            data["correct_count"] = sum(1 for g in self.guesses.values() if g == self.mood["name"])
        return data


rooms: dict[str, Room] = {}


def make_room_code() -> str:
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        code = "".join(random.choices(chars, k=4))
        if code not in rooms:
            return code


def create_room(host_name: str) -> tuple[Room, Player]:
    code = make_room_code()
    room = Room(id=code)
    player = Player(id=str(uuid.uuid4())[:8], name=host_name)
    room.players.append(player)
    rooms[code] = room
    return room, player


def join_room(room_id: str, name: str) -> tuple[Optional[Room], Optional[Player], Optional[str]]:
    room = rooms.get(room_id.upper())
    if not room:
        return None, None, "اتاق پیدا نشد"
    name = name.strip()
    # Allow rejoining by matching name — works even mid-game
    for player in room.players:
        if player.name.strip() == name:
            return room, player, None
    # New player — only allowed in lobby
    if room.state != "lobby":
        return None, None, "بازی شروع شده — با اسم قبلیت دوباره وارد شو"
    if len(room.players) >= 12:
        return None, None, "اتاق پر شده"
    player = Player(id=str(uuid.uuid4())[:8], name=name)
    room.players.append(player)
    return room, player, None
