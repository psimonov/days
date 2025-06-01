import random
import subprocess
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--days', type=int, default=1)
args = parser.parse_args()
DAYS = args.days
FILENAME = 'days.txt'

ANIMALS = [
    ("жирафа", 'm'), ("пингвина", 'm'), ("слона", 'm'), ("тигра", 'm'), ("волка", 'm'),
    ("кенгуру", 'm'), ("медведя", 'm'), ("грифона", 'm'), ("дракона", 'm'),
    ("феникса", 'm'), ("единорога", 'm'), ("леопарда", 'm'), ("гиппогрифа", 'm'),
    ("манула", 'm'), ("енота", 'm'), ("кентавра", 'm'), ("утконоса", 'm'),
    ("крокодила", 'm'), ("бегемота", 'm'), ("ягуара", 'm'),
    ("панды", 'f'), ("черепахи", 'f'), ("обезьяны", 'f'), ("совы", 'f'),
    ("фламинго", 'm'), ("ламантинa", 'm'), ("зебры", 'f'), ("выдры", 'f'),
    ("лисицы", 'f'), ("чёрной кошки", 'f'), ("птицы-секретаря", 'f'),
    ("русалки", 'f'), ("чупакабры", 'f'), ("лисицы-фенек", 'f'),
    ("русалочки", 'f'), ("русалета", 'm'), ("страуса", 'm'), ("мантикора", 'm'),
    ("гиппопотама", 'm'), ("русалена", 'm'), ("сапсана", 'm')
]
COLORS = [
    ("красного", "красной", "красного"),
    ("синего", "синей", "синего"),
    ("зелёного", "зелёной", "зелёного"),
    ("жёлтого", "жёлтой", "жёлтого"),
    ("оранжевого", "оранжевой", "оранжевого"),
    ("фиолетового", "фиолетовой", "фиолетового"),
    ("розового", "розовой", "розового"),
    ("чёрного", "чёрной", "чёрного"),
    ("белого", "белой", "белого"),
    ("серого", "серой", "серого"),
    ("коричневого", "коричневой", "коричневого"),
    ("золотого", "золотой", "золотого"),
    ("серебряного", "серебряной", "серебряного"),
    ("огненного", "огненной", "огненного"),
    ("ледяного", "ледяной", "ледяного"),
    ("лазурного", "лазурной", "лазурного"),
    ("звёздного", "звёздной", "звёздного"),
    ("неонового", "неоновой", "неонового"),
    ("бархатного", "бархатной", "бархатного"),
    ("металлического", "металлической", "металлического"),
    ("радужного", "радужной", "радужного"),
    ("мятного", "мятной", "мятного"),
    ("ультрафиолетового", "ультрафиолетовой", "ультрафиолетового"),
    ("призрачного", "призрачной", "призрачного"),
    ("сказочного", "сказочной", "сказочного"),
    ("шёлкового", "шёлковой", "шёлкового")
]


def get_lines_dict(lines):
    d = {}
    for line in lines:
        if line.strip():
            date_part = line.split(" День ")[0].strip()
            d[date_part] = line
    return d


try:
    with open(FILENAME, "r", encoding="utf-8") as f:
        existing_lines = [line for line in f.readlines() if line.strip()]
except FileNotFoundError:
    existing_lines = []

existing_dict = get_lines_dict(existing_lines)
existing_dates = set(existing_dict.keys())
animals = ANIMALS.copy()
random.shuffle(animals)
dates_to_add = []
for i in range(DAYS):
    date = datetime.now() - timedelta(days=(DAYS - i - 1))
    date_str = date.strftime("%d.%m.%Y")
    if date_str in existing_dates:
        continue
    if not animals:
        animals = ANIMALS.copy()
        random.shuffle(animals)
    animal, gender = animals.pop()
    color = random.choice(COLORS)
    if gender == 'm':
        color_word = color[0]
    elif gender == 'f':
        color_word = color[1]
    else:
        color_word = color[2]
    line = f"{date_str} День {color_word} {animal}\n"
    dates_to_add.append((date_str, line))

for date_str, line in dates_to_add:
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            current_lines = [l for l in f.readlines() if l.strip()]
    except FileNotFoundError:
        current_lines = []
    curr_dict = get_lines_dict(current_lines)
    curr_dict[date_str] = line
    sorted_lines = []
    for d in sorted(curr_dict.keys(), key=lambda d: datetime.strptime(d, "%d.%m.%Y")):
        sorted_lines.append(curr_dict[d])
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.writelines(sorted_lines)
    commit_msg = line.split(' ', 1)[1].strip()
    commit_time = datetime.strptime(date_str, "%d.%m.%Y").replace(
        hour=random.randint(8, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )
    commit_time_str = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
    subprocess.run(['git', 'add', FILENAME])
    subprocess.run([
        'git', 'commit', '-m', commit_msg,
        '--date', commit_time_str,
    ])
    print(f"{commit_msg} ({date_str})")

if not dates_to_add:
    print("Новых дней не найдено, ничего не добавлено.")
