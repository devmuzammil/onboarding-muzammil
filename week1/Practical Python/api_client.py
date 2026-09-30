import requests
import logging
import json

logging.basicConfig(
    filename="api_client.log",
    level=logging.INFO
)
users_url = "https://jsonplaceholder.typicode.com/users"
posts_url = "https://jsonplaceholder.typicode.com/posts"
logging.info("Fetching users")

try:
    response = requests.get(users_url, timeout=10)
    response.raise_for_status()
    users = response.json()

    logging.info("Users fetched successfully")

except requests.RequestException as e:
    logging.error(f"Failed to fetch users: {e}")
    users = []
logging.info("Fetching posts")

try:
    response = requests.get(posts_url, timeout=10)
    response.raise_for_status()
    posts = response.json()

    logging.info("Posts fetched successfully")

except requests.RequestException as e:
    logging.error(f"Failed to fetch posts: {e}")
    posts = []
logging.info("Building report")

report = []

for user in users:
    count = 0

    for post in posts:
        if post["userId"] == user["id"]:
            count += 1

    report.append({
        "userId": user["id"],
        "name": user["name"],
        "post_count": count
    })
logging.info("Report built successfully")
logging.info("Saving report")

with open("report.json", "w") as file:
    json.dump(report, file, indent=4)


logging.info("Report saved successfully")

print("Report generated successfully.")
