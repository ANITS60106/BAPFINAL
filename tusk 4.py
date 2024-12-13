from datetime import datetime


transactions = [
    {"id": "TX123", "amount": 150, "timestamp": "2024-12-10 10:00:00"},
    {"id": "TX124", "amount": 200, "timestamp": "2024-12-10 10:05:00"},
    {"id": "TX123", "amount": 150, "timestamp": "2024-12-10 10:01:00"},
    {"id": "TX125", "amount": 100, "timestamp": "2024-12-10 10:10:00"},
    {"id": "TX123", "amount": 150, "timestamp": "2024-12-10 10:15:00"},
    {"id": "TX124", "amount": 200, "timestamp": "2024-12-10 10:06:00"},
    {"id": "TX126", "amount": 300, "timestamp": "2024-12-10 10:20:00"}
]
def find_duplicate_transactions(transactions, time_window_seconds=60):

    transaction_groups = {}
    duplicates = []

    for transaction in transactions:
        key = (transaction["id"], transaction["amount"])
        timestamp = datetime.strptime(transaction["timestamp"], "%Y-%m-%d %H:%M:%S")
        if key not in transaction_groups:
            transaction_groups[key] = []
        transaction_groups[key].append(timestamp)

    for key, timestamps in transaction_groups.items():
        timestamps.sort()
        for i in range(1, len(timestamps)):
            if (timestamps[i] - timestamps[i - 1]).total_seconds() <= time_window_seconds:
                duplicates.append({
                    "id": key[0],
                    "amount": key[1],
                    "timestamp1": timestamps[i - 1].strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp2": timestamps[i].strftime("%Y-%m-%d %H:%M:%S")
                })

    return duplicates

duplicates = find_duplicate_transactions(transactions, time_window_seconds=60)

for duplicate in duplicates:
    print(duplicate)