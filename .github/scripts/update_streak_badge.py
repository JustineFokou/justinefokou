import requests, datetime, os

USERNAME = "JustineFokou"
TOKEN = os.getenv("GITHUB_TOKEN")

# Récupérer les événements publics récents
events_url = f"https://api.github.com/users/{USERNAME}/events/public"
r = requests.get(events_url, headers={"Authorization": f"token {TOKEN}"})
events = r.json()

# Extraire les dates de commit (PushEvent)
commit_dates = set()
for e in events:
    if e["type"] == "PushEvent":
        date_str = e["created_at"].split("T")[0]
        commit_dates.add(date_str)

# Calculer les streaks
today = datetime.date.today()
current_streak = 0
longest_streak = 0
temp_streak = 0

# On parcourt les 365 derniers jours
for i in range(365):
    day = today - datetime.timedelta(days=i)
    if str(day) in commit_dates:
        temp_streak += 1
        longest_streak = max(longest_streak, temp_streak)
    else:
        # Si on atteint aujourd'hui sans commit, le current streak s'arrête
        if i == 0:
            current_streak = 0
        elif current_streak == 0:
            current_streak = temp_streak
        temp_streak = 0

# Générer un badge combiné
label = "🔥 Streak"
message = f"Current: {current_streak}d | Longest: {longest_streak}d"
color = "FF005C"

badge_url = f"https://img.shields.io/badge/{label}-{message}-{color}?style=for-the-badge"
badge_url = badge_url.replace(" ", "%20").replace("|", "%7C")

# Télécharger le SVG
svg = requests.get(badge_url).text
with open("streak_badge.svg", "w") as f:
    f.write(svg)

print(f"✅ Badge mis à jour : Current {current_streak} | Longest {longest_streak}")
