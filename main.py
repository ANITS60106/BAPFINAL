from datetime import datetime, timedelta
from collections import defaultdict
import json

with open('log_data.json', 'r') as file:
    log_data = json.load(file)

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

most_active_user = max(total_durations, key=total_durations.get, default=None)
most_active_time = total_durations.get(most_active_user, 0)

open_sessions = {user: times for user, times in active_sessions.items() if times}

print("Самая долгая сессия для каждого пользователя:")
for user, session in longest_sessions.items():
    if session:
        start, end = session
        duration = (end - start).total_seconds() / 3600
        print(f"{user}: {start} - {end} ({duration:.2f} часов)")

print(f"\nСреднее время пребывания всех пользователей: {average_time:.2f} часов")

print("\nСамый активный пользователь по суммарной длительности сессий:")
if most_active_user:
    print(f"{most_active_user} с {most_active_time:.2f} часами")

print("\nНезакрытые сессии:")
for user, times in open_sessions.items():
    print(f"{user}: {times}")

def find_login_anomalies(log_data):
    anomalies = defaultdict(list)
    active_sessions = defaultdict(list)
    logout_times = defaultdict(list)

    last_action = defaultdict(str)

    for log in log_data:
        user = log["user"]
        action = log["action"]
        time = log["time"]

        if action == "login":
            if last_action[user] == "login":
                anomalies[user].append(f"Последовательные логины в {time}")
            if time in active_sessions[user]:
                anomalies[user].append(f"Повторный логин в {time}")
            active_sessions[user].append(time)
            last_action[user] = "login"
        elif action == "logout":
            if last_action[user] == "logout":
                anomalies[user].append(f"Последовательные логауты в {time}")
            if time in logout_times[user]:
                anomalies[user].append(f"Повторный логаут в {time}")
            logout_times[user].append(time)
            if active_sessions[user]:
                start_time = active_sessions[user].pop(0)
                if (time - start_time) <= timedelta(minutes=1):
                    anomalies[user].append(f"Сессия {start_time} - {time} длительностью менее 1 минуты")
            last_action[user] = "logout"

    return anomalies

anomalies = find_login_anomalies(log_data)

if anomalies:
    print("Найдены аномалии с несколькими активными сессиями:")
    for user, messages in anomalies.items():
        print(f"{user}: {', '.join(messages)}")
else:
    print("Аномалий не найдено.")
