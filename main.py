from datetime import datetime
from collections import defaultdict

log_data = [
    {"user": "User2", "time": "2024-12-01 12:00", "action": "login"},
    {"user": "User1", "time": "2024-12-01 13:30", "action": "logout"},
    {"user": "User3", "time": "2024-12-01 14:00", "action": "login"},
    {"user": "User2", "time": "2024-12-01 16:00", "action": "logout"},
    {"user": "User1", "time": "2024-12-01 17:00", "action": "login"},
    {"user": "User3", "time": "2024-12-01 17:30", "action": "logout"}
]


for log in log_data:
    log["time"] = datetime.strptime(log["time"], "%Y-%m-%d %H:%M")

log_data.sort(key=lambda x: x["time"])

active_sessions = defaultdict(list)
finished_sessions = defaultdict(list)

for log in log_data:
    user = log["user"]
    if log["action"] == "login":
        active_sessions[user].append(log["time"])
    elif log["action"] == "logout":
        if active_sessions[user]:
            start_time = active_sessions[user].pop(0)
            finished_sessions[user].append((start_time, log["time"]))

longest_sessions = {}
for user, sessions in finished_sessions.items():
    max_duration = 0
    longest_session = None
    for start, end in sessions:
        duration = (end - start).total_seconds()
        if duration > max_duration:
            max_duration = duration
            longest_session = (start, end)
    longest_sessions[user] = longest_session

total_time = sum((end - start).total_seconds() for sessions in finished_sessions.values() for start, end in sessions)
total_sessions = sum(len(sessions) for sessions in finished_sessions.values())
average_time = total_time / total_sessions / 3600 if total_sessions else 0

total_durations = {user: sum((end - start).total_seconds() / 3600 for start, end in sessions) for user, sessions in finished_sessions.items()}


most_active_user = None
most_active_time = 0
for user, total_time in total_durations.items():
    if total_time > most_active_time:
        most_active_time = total_time
        most_active_user = user

open_sessions = {user: times for user, times in active_sessions.items() if times}

print("Самая долгая сессия для каждого пользователя:")
for user, session in longest_sessions.items():
    if session:
        start, end = session
        duration = (end - start).total_seconds() / 3600
        print(f"{user}: {start} - {end} ({duration:.2f} часов)")

print(f"\nСреднее время пребывания всех пользователей: {average_time:.2f} часов")


print("\nСамый активный пользователь:")
if most_active_user:
    print(f"{most_active_user} с {most_active_time:.2f} часами")

print("\nНезакрытые сессии:")
for user, times in open_sessions.items():
    print(f"{user}: {times}")