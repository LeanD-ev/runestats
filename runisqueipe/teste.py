from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Lista original usada para os Hiscores
skills = [
    "Overall", "Attack", "Defence", "Strength", "Constitution",
    "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
    "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing",
    "Mining", "Herblore", "Agility", "Thieving", "Slayer",
    "Farming", "Runecrafting", "Hunter", "Construction", "Summoning",
    "Dungeoneering", "Divination", "Invention", "Archaeology"
]

# Mapeamento dos IDs da API para os nomes corretos das habilidades
skills_map = {
    14: 'Mining',
    13: 'Smithing',
    3:  'Constitution',
    1:  'Defence',
    0:  'Attack',
    2:  'Strength',
    8:  'Woodcutting',
    4:  'Ranged',
    7:  'Cooking',
    5:  'Prayer',
    12: 'Crafting',
    10: 'Fishing',
    11: 'Firemaking',
    9:  'Fletching',
    19: 'Farming',
    28: 'Necromancy',
    27: 'Archaeology',
    26: 'Invention',
    25: 'Divination',
    24: 'Dungeoneering',
    23: 'Summoning',
    22: 'Construction',
    21: 'Hunter',
    20: 'Runecrafting',
    18: 'Slayer',
    17: 'Thieving',
    16: 'Agility',
    15: 'Herblore',
    6:  'Magic'
}

# Ordem exata conforme o site oficial
correct_order = [
    'Mining', 'Smithing', 'Constitution', 'Defence', 'Attack', 'Strength',
    'Woodcutting', 'Ranged', 'Cooking', 'Prayer', 'Crafting', 'Fishing',
    'Firemaking', 'Fletching', 'Farming', 'Necromancy', 'Archaeology',
    'Invention', 'Divination', 'Dungeoneering', 'Summoning', 'Construction',
    'Hunter', 'Runecrafting', 'Slayer', 'Thieving', 'Agility', 'Herblore',
    'Magic'
]

def get_runemetrics(username):
    url = f"https://apps.runescape.com/runemetrics/profile/profile?user={username}&activities=0"
    res = requests.get(url)
    if res.status_code != 200 or "error" in res.text:
        return None
    api_data = res.json().get("skillvalues", [])

    # Prepara dicionário com todos os skills zerados
    skill_dict = {name: {"level": 0, "xp": 0} for name in correct_order}

    # Preenche com os valores retornados pela API
    for entry in api_data:
        sid = entry["id"]
        name = skills_map.get(sid)
        if name in skill_dict:
            skill_dict[name]["level"] = entry["level"]
            skill_dict[name]["xp"]    = entry["xp"]

    # Retorna lista ordenada
    return [
        {"name": name, "level": skill_dict[name]["level"], "xp": skill_dict[name]["xp"]}
        for name in correct_order
    ]

def get_hiscores(username):
    url = f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={username}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    lines = res.text.strip().split('\n')
    data = []
    for i, line in enumerate(lines[:len(skills)]):
        _, level, xp = line.split(',')
        data.append({"name": skills[i], "level": int(level), "xp": int(xp)})
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    username = request.form.get("username")
    data = source = None

    if username:
        data = get_runemetrics(username)
        if data:
            source = "RuneMetrics"
        else:
            data = get_hiscores(username)
            source = "Hiscores" if data else None

    return render_template("index.html", data=data, username=username, source=source)

if __name__ == "__main__":
    app.run(debug=True)
