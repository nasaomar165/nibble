# 🐾 Nibble — Terminal Virtual Pet

A fluffy, sassy virtual pet living right inside your terminal.  
Feed it, pet it, groom it, play fetch with it — or watch it get dramatically upset when you ignore it.  
Nibble evolves through four life stages, has a dynamic personality that shifts between proud and needy, and will absolutely let you know when it's unhappy.

---

## 📦 Requirements
- Python 3.6+
- A terminal with ANSI support (basically any modern terminal)
- No external dependencies — uses only `time`, `random`, and `sys`

---

## 🚀 Running
```bash
python nibble.py
```

---

## 🎮 Controls
| Key | Action | Description |
| --- | --- | --- |
| F | Feed | Reduces hunger by 25. Costs 1 stamina. |
| P | Pet | +10 affection, +3 joy. Petting too many times in a row makes Nibble flustered. Costs 1 stamina. |
| T | Talk | +3 affection. Nibble shares its current thought. Costs 1 stamina. |
| G | Groom | +8 affection, +12 joy, −5 pride. Costs 1 stamina. |
| L | Play | Launches the fetch mini-game. Costs 1 stamina. |
| N | Nap | Fully restores stamina. Slightly increases hunger and joy. |
| U | Use Item | Opens inventory submenu (Treats, Toys, Medicine). |
| W | Wait | Advances to the next day. Stats decay, stamina restores, random events may occur. |
| Q | Quit | Exit the game. |

---

## 📊 Stats
| Stat | Range | Behavior |
| --- | --- | --- |
| Hunger | 0–100 | +8/day. At 100, Nibble runs away (Game Over). Above 80 for 2+ days risks sickness. |
| Love | 0–100 | −3/day. Raised by petting, talking, grooming, playing. |
| Joy | 0–100 | −5/day (−10 if sick). Raised by most interactions. |
| Pride | 0–100 | Hidden personality meter. >50 = SASSY, ≤50 = NEEDY. Grooming lowers, feeding raises. |
| Stamina | 0–3 | Each action costs 1. Restored by napping or waiting. |
| XP | ∞ | Gained from interactions. Drives evolution. |

---

Stat bars are color-coded: 🟢 >60, 🟡 30–60, 🔴 <30
## 🧬 Evolution Phases
| XP Threshold | Phase | Description |
| --- | --- | --- |
| 0 | SEED | Tiny fluffball. |
| 10 | SPROUT | Ears and tail appear. |
| 30 | TEEN | Bigger, fluffier, sparkles. |
| 70 | GUARDIAN | Majestic mane, full tail. Final form. |

---

## 🎭 Moods
- Neutral: `>.<`
- Happy: `>w<`
- Eating: `>O<`
- Overwhelmed: `× ×` eyes, `-_`
- Sick: `>~<`
- Sleeping: `- -` eyes, `z Z z`

---

## 🎒 Inventory & Items
- Treat: −35 hunger, +10 joy (starts with 1)
- Toy: +20 joy, +5 affection
- Medicine: Cures sickness
- Items are found via random events when you Wait.

---

## 🎾 Fetch Mini-Game
- Ball thrown Left (1), Center (2), Right (3)
- Guess correctly:
- Win: +15 joy, +5 affection, +2 XP
- Lose: +5 joy, +1 XP

---

## 🌅 Random Events (on Wait)
- `12%` Found an item (+1 random item)
- `8%` Chased a butterfly (+10 joy)
- `7%` Curled up near you (+5 affection)
- `6%` Sniffed something weird (+5 hunger)

---

## 🏆 Achievements
- Beloved Pet: Pet 20 times
- Well Fed: Feed 15 times
- Playful: Play 10 times
- Guardian: Reach final evolution (70 XP)
- Survivor: Survive 7 days
- Flawless: Groom 10 times
- Collector: Hold 5+ items in inventory

---

## 💀 Sickness
- Cause: Hunger >80 for 2+ days
- Effects: Joy −10/day, Affection −5/day
- Cures: Medicine or feeding (30% chance per feed)
- Visual: Red SICK status, sick face

---

🧠 Personality System
- Sassy (Pride > 50)
 ```
  "My internal sensors indicate a void. Fix it."
  "I suppose this environment is adequate. For now."
  "Don't let this go to your head, human."
```
- Needy (Pride ≤ 50)
  ```
  "I... I think I'm hungry. Please don't forget me."
  "You're okay for a human. Don't tell anyone."
  "Thanks for paying attention to me... please stay."
  ```

---

## ⚠️ Game Over
If Hunger reaches 100, Nibble runs away.
No save system — Nibble lives in the moment.

---

## 💡 Tips
- Don’t spam petting — after 3, Nibble gets overwhelmed.
- Groom strategically — boosts joy but lowers pride.
- Keep hunger <60 to avoid sickness.
- Nap when stamina is low.
- Save medicine for actual sickness.
- Fetch is efficient for XP.
- Balance pride to see both dialogue modes.
- Evolution is permanent — Guardian form stays magnificent.

---

## 🎨 Technical Notes
- Renders at 22 lines fixed height (prevents flicker)
- ANSI 256-color pastel palette
- Cursor hidden during gameplay
- Each line padded to 80 characters
- ASCII art handcrafted with `·, ~, *, °`

---

## ✨ Enjoy raising your fluffy, sassy companion right in your terminal!
```
       ·~~~~~~~·
      / · °  ° · \
     | *  >w<   * |   "...Take care of your fluff."
     |  ~~~~~~~~  |
      \ ·~~~~~~· /
       ·~~~~~~~·
```
