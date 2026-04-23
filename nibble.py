import time
import random
import sys

# ═══════════════════════════════════════════════════════════
#  ANSI Color Palette
# ═══════════════════════════════════════════════════════════
PINK     = '\033[38;5;213m'
PEACH    = '\033[38;5;217m'
CYAN     = '\033[38;5;159m'
MINT     = '\033[38;5;194m'
YELLOW   = '\033[38;5;229m'
GOLD     = '\033[38;5;220m'
GREEN    = '\033[38;5;150m'
RED      = '\033[38;5;210m'
PURPLE   = '\033[38;5;183m'
LAVENDER = '\033[38;5;189m'
BOLD     = '\033[1m'
DIM      = '\033[2m'
ITALIC   = '\033[3m'
RESET    = '\033[0m'


def c(text, color):
    return f"{color}{text}{RESET}"


class Nibble:
    def __init__(self, name="Nibble"):
        self.name = name
        self.hunger = 20
        self.affection = 50
        self.pride = 50
        self.joy = 50
        self.xp = 0
        self.stamina = 3
        self.max_stamina = 3
        self.consecutive_pets = 0
        self.phase = 0
        self.current_mood = "neutral"
        self.dialogue = "..."
        self.day = 1
        self.sick = False
        self.sick_ticks = 0
        self.inventory = {"treat": 1, "toy": 0, "medicine": 0}
        self.total_pets = 0
        self.total_feeds = 0
        self.total_plays = 0
        self.total_grooms = 0
        self.achievements = set()
        self.event_message = ""
        self.event_timer = 0

        self.phase_names = {0: "SEED", 1: "SPROUT", 2: "TEEN", 3: "GUARDIAN"}

        # ═══════════════════════════════════════════════════════
        #  FLUFFY ART — 9 lines per frame, 4 phases × 6 moods
        # ═══════════════════════════════════════════════════════
        self.assets = {
            0: {  # SEED — tiny round fluffball
                "neutral": [
                    "       ·~~~~~~~·       ",
                    "      / · · · · \\      ",
                    "     | · °   ° · |     ",
                    "     |    >.<    |     ",
                    "     | · ~~~~~ · |     ",
                    "      \\ · · · · /      ",
                    "       ·~~~~~~~·       ",
                    "        ~~~~~~         ",
                    "         ~~            ",
                ],
                "happy": [
                    "       ·~~~~~~~·       ",
                    "      / · · · · \\      ",
                    "     | · °   ° · |     ",
                    "     |    >w<    |     ",
                    "     | · ~~~~~ · |     ",
                    "      \\ · · · · /      ",
                    "       ·~~~~~~~·       ",
                    "        ~~~~~~         ",
                    "       ~~~~~~~~        ",
                ],
                "eating": [
                    "       ·~~~~~~~·       ",
                    "      / · · · · \\      ",
                    "     | · °   ° · |     ",
                    "     |    >O<    |     ",
                    "     | · ~~~~~ · |     ",
                    "      \\ · · · · /      ",
                    "       ·~~~~~~~·       ",
                    "        ~~~~~~         ",
                    "         ~~            ",
                ],
                "overwhelmed": [
                    "       ·~~~~~~~·       ",
                    "      / · · · · \\      ",
                    "     | · ×   × · |     ",
                    "     |    -_-    |     ",
                    "     | · ~~~~~ · |     ",
                    "      \\ · · · · /      ",
                    "       ·~~~~~~~·       ",
                    "        ~~~~~~         ",
                    "         ~~            ",
                ],
                "sick": [
                    "       ·~~~~~~~·       ",
                    "      / · · · · \\      ",
                    "     | · °   ° · |     ",
                    "     |    >~<    |     ",
                    "     | · ~~~~~ · |     ",
                    "      \\ · · · · /      ",
                    "       ·~~~~~~~·       ",
                    "        ~~~~~~         ",
                    "         ~~            ",
                ],
                "sleeping": [
                    "       ·~~~~~~~·       ",
                    "      / · · · · \\      ",
                    "     | · -   - · |     ",
                    "     |   z Z z   |     ",
                    "     | · ~~~~~ · |     ",
                    "      \\ · · · · /      ",
                    "       ·~~~~~~~·       ",
                    "        ~~~~~~         ",
                    "         ~~            ",
                ],
            },
            1: {  # SPROUT — ears and tail appear
                "neutral": [
                    "         /\\  /\\         ",
                    "        / ·° °· \\       ",
                    "       |   >.<   |      ",
                    "       |  ~~~~~~ |      ",
                    "        \\ ·° °· /       ",
                    "         ·~~~~·         ",
                    "         || ||  ~       ",
                    "         ^^ ^^          ",
                    "          ~~            ",
                ],
                "happy": [
                    "         /\\  /\\         ",
                    "        / ·° °· \\       ",
                    "       |   >w<   |      ",
                    "       |  ~~~~~~ |      ",
                    "        \\ ·° °· /       ",
                    "         ·~~~~·         ",
                    "         || || ~~~      ",
                    "         ^^ ^^          ",
                    "         ~~~~           ",
                ],
                "eating": [
                    "         /\\  /\\         ",
                    "        / ·° °· \\       ",
                    "       |   >O<   |      ",
                    "       |  ~~~~~~ |      ",
                    "        \\ ·° °· /       ",
                    "         ·~~~~·         ",
                    "         || ||  ~       ",
                    "         ^^ ^^          ",
                    "          ~~            ",
                ],
                "overwhelmed": [
                    "         /\\  /\\         ",
                    "        / ·× ×· \\       ",
                    "       |   -_-   |      ",
                    "       |  ~~~~~~ |      ",
                    "        \\ ·× ×· /       ",
                    "         ·~~~~·         ",
                    "         || ||          ",
                    "         ^^ ^^          ",
                    "          ~~            ",
                ],
                "sick": [
                    "         /\\  /\\         ",
                    "        / ·° °· \\       ",
                    "       |   >~<   |      ",
                    "       |  ~~~~~~ |      ",
                    "        \\ ·° °· /       ",
                    "         ·~~~~·         ",
                    "         || ||          ",
                    "         ^^ ^^          ",
                    "          ~~            ",
                ],
                "sleeping": [
                    "         /\\  /\\         ",
                    "        / ·- -· \\       ",
                    "       |  z Z z  |      ",
                    "       |  ~~~~~~ |      ",
                    "        \\ ·- -· /       ",
                    "         ·~~~~·         ",
                    "         || ||  ~       ",
                    "         ^^ ^^          ",
                    "          ~~            ",
                ],
            },
            2: {  # TEEN — bigger, fluffier, sparkles
                "neutral": [
                    "          /\\    /\\          ",
                    "         / · °  ° · \\       ",
                    "        | *  >  <  * |      ",
                    "        |  ~~~~~~~~  |      ",
                    "        | ~~~~~~~~~~ |      ",
                    "         \\ ~~~~~~~~ /       ",
                    "          ·~~~~~~~·         ",
                    "         ||    ||  ~^~      ",
                    "         ^^    ^^           ",
                ],
                "happy": [
                    "          /\\    /\\          ",
                    "         / · °  ° · \\       ",
                    "        | *  >w<   * |      ",
                    "        |  ~~~~~~~~  |      ",
                    "        | ~~~~~~~~~~ |      ",
                    "         \\ ~~~~~~~~ /       ",
                    "          ·~~~~~~~·         ",
                    "         ||    || ~~~^~     ",
                    "         ^^    ^^           ",
                ],
                "eating": [
                    "          /\\    /\\          ",
                    "         / · °  ° · \\       ",
                    "        | *  >O<   * |      ",
                    "        |  ~~~~~~~~  |      ",
                    "        | ~~~~~~~~~~ |      ",
                    "         \\ ~~~~~~~~ /       ",
                    "          ·~~~~~~~·         ",
                    "         ||    ||  ~^~      ",
                    "         ^^    ^^           ",
                ],
                "overwhelmed": [
                    "          /\\    /\\          ",
                    "         / · ×  × · \\       ",
                    "        | *  -_-   * |      ",
                    "        |  ~~~~~~~~  |      ",
                    "        | ~~~~~~~~~~ |      ",
                    "         \\ ~~~~~~~~ /       ",
                    "          ·~~~~~~~·         ",
                    "         ||    ||           ",
                    "         ^^    ^^           ",
                ],
                "sick": [
                    "          /\\    /\\          ",
                    "         / · °  ° · \\       ",
                    "        | *  >~<   * |      ",
                    "        |  ~~~~~~~~  |      ",
                    "        | ~~~~~~~~~~ |      ",
                    "         \\ ~~~~~~~~ /       ",
                    "          ·~~~~~~~·         ",
                    "         ||    ||           ",
                    "         ^^    ^^           ",
                ],
                "sleeping": [
                    "          /\\    /\\          ",
                    "         / · -  - · \\       ",
                    "        | * z Z z  * |      ",
                    "        |  ~~~~~~~~  |      ",
                    "        | ~~~~~~~~~~ |      ",
                    "         \\ ~~~~~~~~ /       ",
                    "          ·~~~~~~~·         ",
                    "         ||    ||  ~        ",
                    "         ^^    ^^           ",
                ],
            },
            3: {  # GUARDIAN — majestic mane, full tail
                "neutral": [
                    "           /\\      /\\           ",
                    "       ~~ / · °  ° · \\ ~~       ",
                    "      |* *   >  <   * *|        ",
                    "      |  ~~~~~~~~~~~~  |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "       \\ ~~~~~~~~~~~~ /         ",
                    "        ·~~~~~~~~~~~~·          ",
                    "       ||      ||   ~^^^~       ",
                ],
                "happy": [
                    "           /\\      /\\           ",
                    "       ~~ / · °  ° · \\ ~~       ",
                    "      |* *   >w<    * *|        ",
                    "      |  ~~~~~~~~~~~~  |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "       \\ ~~~~~~~~~~~~ /         ",
                    "        ·~~~~~~~~~~~~·          ",
                    "       ||      || ~~~~~^^^~     ",
                ],
                "eating": [
                    "           /\\      /\\           ",
                    "       ~~ / · °  ° · \\ ~~       ",
                    "      |* *   >O<    * *|        ",
                    "      |  ~~~~~~~~~~~~  |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "       \\ ~~~~~~~~~~~~ /         ",
                    "        ·~~~~~~~~~~~~·          ",
                    "       ||      ||   ~^^^~       ",
                ],
                "overwhelmed": [
                    "           /\\      /\\           ",
                    "       ~~ / · ×  × · \\ ~~       ",
                    "      |* *   -_-    * *|        ",
                    "      |  ~~~~~~~~~~~~  |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "       \\ ~~~~~~~~~~~~ /         ",
                    "        ·~~~~~~~~~~~~·          ",
                    "       ||      ||               ",
                ],
                "sick": [
                    "           /\\      /\\           ",
                    "       ~~ / · °  ° · \\ ~~       ",
                    "      |* *   >~<    * *|        ",
                    "      |  ~~~~~~~~~~~~  |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "       \\ ~~~~~~~~~~~~ /         ",
                    "        ·~~~~~~~~~~~~·          ",
                    "       ||      ||               ",
                ],
                "sleeping": [
                    "           /\\      /\\           ",
                    "       ~~ / · -  - · \\ ~~       ",
                    "      |* *  z Z z   * *|        ",
                    "      |  ~~~~~~~~~~~~  |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "      | ~~~~~~~~~~~~~~ |        ",
                    "       \\ ~~~~~~~~~~~~ /         ",
                    "        ·~~~~~~~~~~~~·          ",
                    "       ||      ||   ~           ",
                ],
            },
        }

        # ═══════════════════════════════════════════════════════
        #  DIALOGUE POOLS
        # ═══════════════════════════════════════════════════════
        self.dialogues = {
            "hungry_proud": [
                "My internal sensors indicate a void. Fix it.",
                "I require sustenance of a higher caliber. Now.",
                "Do you enjoy watching me slowly dissipate?",
                "My elegance cannot be sustained on empty.",
                "Hunger is beneath one of my stature.",
            ],
            "hungry_needy": [
                "I... I think I'm hungry. Please don't forget me.",
                "Food? If it's not too much trouble...",
                "My stomach is making noises. Embarrassing.",
                "Is there maybe a snack somewhere...?",
                "I feel so light... and not in a good way.",
            ],
            "happy_proud": [
                "I suppose this environment is adequate. For now.",
                "You may continue existing in my presence.",
                "Don't let this go to your head, human.",
                "My fluff has never been more magnificent.",
                "I grace you with my satisfaction.",
            ],
            "happy_needy": [
                "You're okay for a human. Don't tell anyone.",
                "Thanks for paying attention to me... please stay.",
                "I'm smiling! Is this what joy feels like?",
                "This is nice... can we stay like this?",
                "My tail won't stop wagging. How undignified.",
            ],
            "overwhelmed": [
                "Unhand me. I am not a stress ball.",
                "Too much touching. Activating defense mode.",
                "My personal space is a sovereign territory.",
                "I'm all ruffled! Look what you've done!",
                "Cease! My fluff cannot take more!",
            ],
            "neutral": [
                "Hmph.",
                "...",
                "Entertain me.",
                "I am processing existential data.",
                "*fluffs self importantly*",
                "The void stares back.",
            ],
            "sick": [
                "I don't feel so fluffy...",
                "Everything is spinning... and not in a fun way.",
                "Can you... help? *coughs pathetically*",
                "My ears are drooping and I hate it.",
                "Need... medicine...",
            ],
            "sleeping": [
                "z Z z ...",
                "*snore* ... fluffy dreams ...",
                "mrrr... five more minutes...",
                "*twitches ear in sleep*",
            ],
            "groomed": [
                "Oh... OH that's the spot!",
                "My fluff! It's becoming MAGNIFICENT!",
                "I shall allow this. Continue immediately.",
                "*purring intensifies* Did I say that out loud?",
            ],
            "played_won": [
                "I caught it! Did you see?! ...Act casual.",
                "My reflexes are superior! Admit it!",
                "That was... acceptable entertainment.",
                "Again! Again! ...I mean, if you insist.",
            ],
            "played_lost": [
                "I meant to miss. It was a strategic choice.",
                "Next time I'll catch it for sure!",
                "Hmph. The wind was against me.",
                "That doesn't count. Rematch!",
            ],
        }

        self.idle_thoughts = [
            "I wonder what clouds taste like...",
            "My left ear is softer than my right. Fact.",
            "If I were bigger, I'd conquer the living room.",
            "I dreamt about a giant treat. It was glorious.",
            "Do you think other Nibbles are as fluffy as me?",
            "I've been practicing my tail swish. Very dignified.",
            "The carpet smells interesting today.",
            "I'm not napping. I'm meditating. There's a difference.",
            "What if we're all just characters in someone's terminal?",
            "I demand more chin scratches. It's in the contract.",
            "My fluff holds secrets. I'll never tell.",
            "Is the red dot real? I need to know.",
            "I memorized the sound of the treat bag. All of them.",
        ]

    # ═══════════════════════════════════════════════════════
    #  Core Logic
    # ═══════════════════════════════════════════════════════
    def update_mood_and_dialogue(self):
        if self.sick:
            self.current_mood = "sick"
            self.dialogue = random.choice(self.dialogues["sick"])
        elif self.consecutive_pets > 3:
            self.current_mood = "overwhelmed"
            self.dialogue = random.choice(self.dialogues["overwhelmed"])
        elif self.hunger > 70:
            self.current_mood = "neutral"
            self.dialogue = random.choice(
                self.dialogues["hungry_proud"]
                if self.pride > 50
                else self.dialogues["hungry_needy"]
            )
        elif self.affection > 60 and self.joy > 50:
            self.current_mood = "happy"
            self.dialogue = random.choice(
                self.dialogues["happy_proud"]
                if self.pride > 50
                else self.dialogues["happy_needy"]
            )
        else:
            self.current_mood = "neutral"
            self.dialogue = random.choice(self.dialogues["neutral"])

    def check_evolution(self):
        old = self.phase
        if self.xp >= 70:
            self.phase = 3
        elif self.xp >= 30:
            self.phase = 2
        elif self.xp >= 10:
            self.phase = 1
        else:
            self.phase = 0
        if self.phase != old:
            self.event_message = f"{self.name} evolved into {self.phase_names[self.phase]}!"
            self.event_timer = 3
            self.check_achievements()

    def check_achievements(self):
        checks = [
            ("beloved",   self.total_pets >= 20,   "Beloved - Pet 20 times"),
            ("well_fed",  self.total_feeds >= 15,  "Well Fed - Feed 15 times"),
            ("playful",   self.total_plays >= 10,  "Playful - Play 10 times"),
            ("guardian",  self.phase >= 3,          "Guardian - Reach final form"),
            ("survivor",  self.day >= 7,            "Survivor - Survive 7 days"),
            ("flawless",  self.total_grooms >= 10,  "Flawless - Groom 10 times"),
            ("collector", sum(self.inventory.values()) >= 5, "Collector - Hoard 5 items"),
        ]
        for key, cond, label in checks:
            if cond and key not in self.achievements:
                self.achievements.add(key)
                self.event_message = f"Achievement: {label}"
                self.event_timer = 3

    # ═══════════════════════════════════════════════════════
    #  Actions
    # ═══════════════════════════════════════════════════════
    def feed(self):
        if self.stamina <= 0:
            return "exhausted"
        self.hunger = max(0, self.hunger - 25)
        self.pride = min(100, self.pride + 5)
        self.joy = min(100, self.joy + 5)
        self.xp += 1
        self.stamina -= 1
        self.consecutive_pets = 0
        self.total_feeds += 1
        self.current_mood = "eating"
        self.dialogue = "*munch munch*"
        if self.sick and random.random() < 0.3:
            self.sick = False
            self.sick_ticks = 0
            self.dialogue = "*munch* I feel a bit better..."
        self.check_evolution()
        self.check_achievements()
        return "success"

    def pet(self):
        if self.stamina <= 0:
            return "exhausted"
        self.affection = min(100, self.affection + 10)
        self.consecutive_pets += 1
        self.xp += 1
        self.stamina -= 1
        self.total_pets += 1
        if self.consecutive_pets > 3:
            self.pride = max(0, self.pride - 15)
        else:
            self.pride = min(100, self.pride + 3)
        self.joy = min(100, self.joy + 3)
        self.check_evolution()
        self.update_mood_and_dialogue()
        self.check_achievements()
        return "success"

    def talk(self):
        if self.stamina <= 0:
            return "exhausted"
        self.stamina -= 1
        self.affection = min(100, self.affection + 3)
        self.update_mood_and_dialogue()
        self.check_achievements()
        return "success"

    def groom(self):
        if self.stamina <= 0:
            return "exhausted"
        self.stamina -= 1
        self.affection = min(100, self.affection + 8)
        self.joy = min(100, self.joy + 12)
        self.pride = max(0, self.pride - 5)
        self.xp += 1
        self.total_grooms += 1
        self.current_mood = "happy"
        self.dialogue = random.choice(self.dialogues["groomed"])
        self.consecutive_pets = 0
        self.check_evolution()
        self.check_achievements()
        return "success"

    def play(self):
        if self.stamina <= 0:
            return "exhausted"
        self.stamina -= 1
        self.joy = min(100, self.joy + 10)
        self.affection = min(100, self.affection + 3)
        self.hunger = min(100, self.hunger + 5)
        self.xp += 1
        self.total_plays += 1
        self.consecutive_pets = 0
        self.check_evolution()
        self.check_achievements()
        return "play"

    def nap(self):
        self.stamina = self.max_stamina
        self.hunger = min(100, self.hunger + 5)
        self.joy = min(100, self.joy + 5)
        self.current_mood = "sleeping"
        self.dialogue = random.choice(self.dialogues["sleeping"])
        self.consecutive_pets = 0
        return "success"

    def use_item(self, item):
        if self.inventory.get(item, 0) <= 0:
            return "no_item"
        self.inventory[item] -= 1
        if item == "treat":
            self.hunger = max(0, self.hunger - 35)
            self.joy = min(100, self.joy + 10)
            self.current_mood = "eating"
            self.dialogue = "*MUNCH* Special treat! Yum!!"
        elif item == "medicine":
            self.sick = False
            self.sick_ticks = 0
            self.current_mood = "happy"
            self.dialogue = "I feel the fluff returning... Thank you."
        elif item == "toy":
            self.joy = min(100, self.joy + 20)
            self.affection = min(100, self.affection + 5)
            self.current_mood = "happy"
            self.dialogue = "*plays enthusiastically* This is AMAZING!"
        self.check_achievements()
        return "success"

    def tick(self):
        self.hunger = min(100, self.hunger + 8)
        self.affection = max(0, self.affection - 3)
        self.joy = max(0, self.joy - 5)
        self.stamina = self.max_stamina
        self.consecutive_pets = 0
        self.day += 1

        if self.hunger > 80:
            self.sick_ticks += 1
            if self.sick_ticks >= 2 and not self.sick:
                self.sick = True
                self.event_message = f"{self.name} got sick from hunger!"
                self.event_timer = 3
        else:
            self.sick_ticks = max(0, self.sick_ticks - 1)

        if self.sick:
            self.joy = max(0, self.joy - 10)
            self.affection = max(0, self.affection - 5)

        # Random events
        roll = random.random()
        if roll < 0.12:
            found = random.choice(["treat", "toy", "medicine"])
            self.inventory[found] += 1
            names = {"treat": "a tasty treat", "toy": "a fun toy", "medicine": "some medicine"}
            self.event_message = f"{self.name} found {names[found]}!"
            self.event_timer = 3
        elif roll < 0.20:
            self.joy = min(100, self.joy + 10)
            self.event_message = f"{self.name} chased a butterfly! +Joy"
            self.event_timer = 3
        elif roll < 0.27:
            self.affection = min(100, self.affection + 5)
            self.event_message = f"{self.name} curled up near you. +Love"
            self.event_timer = 3
        elif roll < 0.33:
            self.hunger = min(100, self.hunger + 5)
            self.event_message = f"{self.name} sniffed something weird... +Hunger"
            self.event_timer = 3

        self.update_mood_and_dialogue()
        self.check_achievements()
        return "left" if self.hunger >= 100 else "alive"


# ═══════════════════════════════════════════════════════════
#  UI Helpers
# ═══════════════════════════════════════════════════════════
UI_HEIGHT = 22


def draw_bar(label, value, max_val=100, width=8):
    filled = int((value / max_val) * width)
    if value > 60:
        color = GREEN
    elif value > 30:
        color = YELLOW
    else:
        color = RED
    bar_str = f"{color}{'■' * filled}{DIM}{'□' * (width - filled)}{RESET}"
    return f"[ {label}: {bar_str}{RESET} ]"


def render(nibble):
    print("\033[H", end="")

    status = "SASSY" if nibble.pride > 50 else "NEEDY"
    if nibble.sick:
        status = "SICK"
    if nibble.consecutive_pets > 3:
        status = "FLUSTERED"

    status_color = GREEN
    if status == "SICK":
        status_color = RED
    elif status == "FLUSTERED":
        status_color = PINK
    elif status == "NEEDY":
        status_color = PURPLE

    art = nibble.assets[nibble.phase][nibble.current_mood]

    line_border = c("═" * 58, DIM)
    name_display = c(nibble.name, BOLD + CYAN)
    phase_display = c(nibble.phase_names[nibble.phase], GOLD)
    status_display = c(status, status_color)

    ui = [
        line_border,
        f"  {name_display}  ·  Phase: [{phase_display}]   "
        f"Day: {nibble.day}   ♥ {status_display}",
        line_border,
        "",
    ]

    # Art lines
    for i, line in enumerate(art):
        padded = line.ljust(32)
        if i == 2:
            ui.append(f"    {padded}  {c('\"' + nibble.dialogue[:40] + '\"', ITALIC + PEACH)}")
        else:
            ui.append(f"    {padded}")

    ui.append("")
    ui.append(
        f"  {draw_bar('Hunger', nibble.hunger)}  "
        f"{draw_bar('Love', nibble.affection)}  "
        f"{draw_bar('Joy', nibble.joy)}"
    )

    stamina_str = (
        f"{c('♥', RED)}" * nibble.stamina
        + f"{c('♡', DIM)}" * (nibble.max_stamina - nibble.stamina)
    )
    sick_str = c("YES", RED + BOLD) if nibble.sick else c("No", GREEN)
    inv_str = (
        f"Treats:{nibble.inventory['treat']}  "
        f"Toys:{nibble.inventory['toy']}  "
        f"Meds:{nibble.inventory['medicine']}"
    )
    ui.append(f"   {stamina_str}  |  Sick: {sick_str}  |  {inv_str}")

    if nibble.event_timer > 0:
        ui.append(f"   {c('✦ ' + nibble.event_message + ' ✦', GOLD + BOLD)}")
        nibble.event_timer -= 1
    else:
        ui.append("")

    ui.append(line_border)
    ui.append(
        f"  {c('(F)', CYAN)}eed {c('(P)', CYAN)}et "
        f"{c('(T)', CYAN)}alk {c('(G)', CYAN)}room "
        f"p{c('(L)', CYAN)}ay {c('(N)', CYAN)}ap "
        f"{c('(U)', CYAN)}se {c('(W)', CYAN)}ait "
        f"{c('(Q)', CYAN)}uit"
    )
    ui.append(line_border)

    # Pad to consistent height
    while len(ui) < UI_HEIGHT:
        ui.append("")
    ui = ui[:UI_HEIGHT]

    for line in ui:
        # Pad each line to 80 chars to overwrite old content
        print(line.ljust(80))


def play_fetch(nibble):
    """Mini-game: Fetch! Guess which direction the ball goes."""
    print("\033[H\033[J", end="")
    print(c("═" * 50, DIM))
    print(c("  🎾  FETCH!  🎾", BOLD + CYAN))
    print(c("═" * 50, DIM))
    print()
    print(f"  {nibble.name} wags their tail excitedly!")
    print(f"  Which direction did the ball go?")
    print()
    print(f"    {c('(1)', CYAN)} Left     {c('(2)', CYAN)} Center     {c('(3)', CYAN)} Right")
    print()
    print(f"  >> ", end="", flush=True)

    try:
        choice = input().strip()
    except (EOFError, KeyboardInterrupt):
        choice = "0"

    correct = random.randint(1, 3)
    try:
        guess = int(choice)
    except ValueError:
        guess = 0

    print("\033[H\033[J", end="")

    if guess == correct:
        nibble.joy = min(100, nibble.joy + 15)
        nibble.affection = min(100, nibble.affection + 5)
        nibble.xp += 2
        nibble.current_mood = "happy"
        nibble.dialogue = random.choice(nibble.dialogues["played_won"])
        print(c("═" * 50, DIM))
        print(c("  🎉 CAUGHT IT!", BOLD + GREEN))
        print(c("═" * 50, DIM))
        print()
        print(f"  {nibble.name} caught the ball! +Joy +Love +XP")
    else:
        nibble.joy = min(100, nibble.joy + 5)
        nibble.xp += 1
        nibble.current_mood = "neutral"
        nibble.dialogue = random.choice(nibble.dialogues["played_lost"])
        print(c("═" * 50, DIM))
        print(c("  Missed...", DIM))
        print(c("═" * 50, DIM))
        print()
        print(f"  {nibble.name} couldn't find it... but had fun trying! +Joy +XP")

    print()
    print(f"  {c(nibble.dialogue, ITALIC + PEACH)}")
    print()
    print(f"  {c('Press Enter to continue...', DIM)}", end="", flush=True)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def use_menu(nibble):
        """Sub-menu for using inventory items."""
        # Use a localized clear for the menu so it doesn't break the render flow
        sys.stdout.write("\033[H\033[J")
        print(c("═" * 50, DIM))
        print(c("  🎒  INVENTORY  🎒", BOLD + PURPLE))
        print(c("═" * 50, DIM))
        print(f"\n  (1) Use Treat    (x{nibble.inventory['treat']})")
        print(f"  (2) Use Toy      (x{nibble.inventory['toy']})")
        print(f"  (3) Use Medicine (x{nibble.inventory['medicine']})")
        print(f"  (4) Cancel\n")
        print(f"  >> ", end="", flush=True)

        choice = sys.stdin.readline().strip()
        item_map = {"1": "treat", "2": "toy", "3": "medicine"}
        
        if choice in item_map:
            res = nibble.use_item(item_map[choice])
            if res == "no_item":
                print(c("\n  You don't have any of those!", RED))
                time.sleep(1)
        
        # Clear menu and return to main render
        sys.stdout.write("\033[H\033[J")

def main():
    pet = Nibble("Nibble")
    # Clear screen once at start
    sys.stdout.write("\033[2J\033[H")
    # Hide terminal cursor for better visuals
    sys.stdout.write("\033[?25l")

    try:
        while True:
            render(pet)
            
            # Position cursor for input (Line 24) and clear that line
            sys.stdout.write("\033[24;1H\033[2K" + c("  >> ", CYAN))
            sys.stdout.flush()
            
            choice = sys.stdin.readline().strip().lower()

            if choice == 'q': 
                break
            elif choice == 'f': pet.feed()
            elif choice == 'p': pet.pet()
            elif choice == 't': pet.talk()
            elif choice == 'g': pet.groom()
            elif choice == 'l': play_fetch(pet)
            elif choice == 'u': use_menu(pet)
            elif choice == 'n': pet.nap()
            elif choice == 'w': # Wait / Next Day
                state = pet.tick()
                if state == "left":
                    sys.stdout.write("\033[H\033[J")
                    print(c("\n\n  *** Nibble ran away to find snacks! GAME OVER ***\n", RED + BOLD))
                    break
            
            # Brief pause to let the user see the "eating" or "happy" frames
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore cursor and clear screen on exit
        sys.stdout.write("\033[?25h\033[2J\033[H")
        print(c("Saving your pet data... Goodbye!", DIM))

if __name__ == "__main__":
    main()
