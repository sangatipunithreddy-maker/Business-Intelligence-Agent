import os
import requests
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"

MONDAY_API_TOKEN = os.getenv("MONDAY_API_TOKEN")

DEALS_BOARD_ID = 5030963358
WORK_ORDERS_BOARD_ID = 5030963216


def monday_query(query, variables=None):
    """Send a read-only GraphQL query to monday.com."""

    if not MONDAY_API_TOKEN:
        raise RuntimeError("MONDAY_API_TOKEN is not configured.")

    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json",
    }

    response = requests.post(
        MONDAY_API_URL,
        json={
            "query": query,
            "variables": variables or {},
        },
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        raise RuntimeError(str(result["errors"]))

    return result["data"]


def get_board_items(board_id):
    """Get items from a monday.com board."""

    query = """
    query ($board_id: ID!) {
        boards(ids: [$board_id]) {
            id
            name
            columns {
                id
                title
                type
            }
            items_page(limit: 500) {
                cursor
                items {
                    id
                    name
                    column_values {
                        id
                        text
                        value
                    }
                }
            }
        }
    }
    """

    data = monday_query(
        query,
        {"board_id": str(board_id)}
    )

    boards = data.get("boards", [])

    if not boards:
        raise RuntimeError(f"Board {board_id} was not found.")

    return boards[0]

if __name__ == "__main__":
    print("Testing monday.com connection...")

    work_orders = get_board_items(WORK_ORDERS_BOARD_ID)
    print("Board:", work_orders["name"])
    print("Columns:", len(work_orders["columns"]))
    print("Items returned:", len(work_orders["items_page"]["items"]))
    print("\nCOLUMNS:")

    for column in work_orders["columns"]:
        print(column["id"], "=>", column["title"], "=>", column["type"])