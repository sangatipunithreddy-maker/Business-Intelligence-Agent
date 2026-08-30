from fastapi import FastAPI
from monday_client import (
    monday_query,
    DEALS_BOARD_ID,
    WORK_ORDERS_BOARD_ID
)
app = FastAPI(title="Skylark BI Agent")


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Skylark BI Agent is running"
    }


@app.get("/monday/deals")
def monday_deals():

    query = """
    query ($board_id: ID!) {
        boards(ids: [$board_id]) {
            id
            name
            items_page(limit: 500) {
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

    result = monday_query(
        query,
        {"board_id": str(DEALS_BOARD_ID)}
    )

    return result

@app.get("/monday/summary")
def monday_summary():

    result = monday_deals()

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No board data found"
        }

    items = boards[0]["items_page"]["items"]

    total_deals = len(items)

    status_counts = {}
    total_market_value = 0

    for item in items:

        for column in item["column_values"]:

            # Deal Status
            if column["id"] == "color_mm6qw8p6":

                status = column.get("text")

                if status:
                    status_counts[status] = (
                        status_counts.get(status, 0) + 1
                    )

            # Market Deal Value
            if column["id"] == "numeric_mm6q6w2g":

                value = column.get("text")

                if value:
                    try:
                        value = value.replace(",", "")
                        total_market_value += float(value)
                    except ValueError:
                        pass

    return {
        "total_deals": total_deals,
        "status_counts": status_counts,
        "total_market_value": total_market_value
    }
@app.get("/monday/stages")
def monday_stages():

    result = monday_deals()

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No board data found"
        }

    items = boards[0]["items_page"]["items"]

    stage_counts = {}

    for item in items:

        for column in item["column_values"]:

            # Deal Stage
            if column["id"] == "color_mm6qjpkj":

                stage = column.get("text")

                if stage:
                    stage_counts[stage] = (
                        stage_counts.get(stage, 0) + 1
                    )

    return {
        "stage_counts": stage_counts
    }
@app.get("/monday/sectors")
def monday_sectors():

    result = monday_deals()

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No board data found"
        }

    items = boards[0]["items_page"]["items"]

    sector_counts = {}

    for item in items:

        for column in item["column_values"]:

            # Sector / Service
            if column["id"] == "color_mm6qqdye":

                sector = column.get("text")

                if sector:
                    sector_counts[sector] = (
                        sector_counts.get(sector, 0) + 1
                    )

    return {
        "sector_counts": sector_counts
    }
@app.get("/monday/sector-values")
def monday_sector_values():

    result = monday_deals()

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No board data found"
        }

    items = boards[0]["items_page"]["items"]

    sector_values = {}

    for item in items:

        sector = None
        deal_value = 0

        for column in item["column_values"]:

            # Sector / Service
            if column["id"] == "color_mm6qqdye":
                sector = column.get("text")

            # Market Deal Value
            if column["id"] == "numeric_mm6q6w2g":

                value = column.get("text")

                if value:
                    try:
                        value = value.replace(",", "")
                        deal_value = float(value)
                    except ValueError:
                        deal_value = 0

        if sector:

            if sector not in sector_values:
                sector_values[sector] = {
                    "deal_count": 0,
                    "total_value": 0
                }

            sector_values[sector]["deal_count"] += 1
            sector_values[sector]["total_value"] += deal_value

    return {
        "sector_values": sector_values
    }
@app.get("/monday/sector/{sector_name}")
def monday_sector(sector_name: str):

    result = monday_deals()

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No board data found"
        }

    items = boards[0]["items_page"]["items"]

    matching_deals = []

    for item in items:

        sector = None
        deal_value = 0
        status = None

        for column in item["column_values"]:

            # Sector / Service
            if column["id"] == "color_mm6qqdye":
                sector = column.get("text")

            # Deal Status
            if column["id"] == "color_mm6qw8p6":
                status = column.get("text")

            # Market Deal Value
            if column["id"] == "numeric_mm6q6w2g":

                value = column.get("text")

                if value:
                    try:
                        deal_value = float(
                            value.replace(",", "")
                        )
                    except ValueError:
                        deal_value = 0

        if sector and sector.lower() == sector_name.lower():

            matching_deals.append({
                "deal_name": item["name"],
                "status": status,
                "value": deal_value
            })

    total_value = sum(
        deal["value"] for deal in matching_deals
    )

    return {
        "sector": sector_name,
        "deal_count": len(matching_deals),
        "total_value": total_value,
        "deals": matching_deals
    }
@app.get("/monday/sector/{sector_name}/status")
def monday_sector_status(sector_name: str):

    result = monday_deals()

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No board data found"
        }

    items = boards[0]["items_page"]["items"]

    status_counts = {}
    status_values = {}

    for item in items:

        sector = None
        status = None
        deal_value = 0

        for column in item["column_values"]:

            # Sector / Service
            if column["id"] == "color_mm6qqdye":
                sector = column.get("text")

            # Deal Status
            if column["id"] == "color_mm6qw8p6":
                status = column.get("text")

            # Market Deal Value
            if column["id"] == "numeric_mm6q6w2g":

                value = column.get("text")

                if value:
                    try:
                        deal_value = float(
                            value.replace(",", "")
                        )
                    except ValueError:
                        deal_value = 0

        if sector and sector.lower() == sector_name.lower():

            if status:

                status_counts[status] = (
                    status_counts.get(status, 0) + 1
                )

                status_values[status] = (
                    status_values.get(status, 0) + deal_value
                )

    return {
        "sector": sector_name,
        "status_counts": status_counts,
        "status_values": status_values
    }
@app.get("/monday/work-orders")
def monday_work_orders():

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

    result = monday_query(
        query,
        {"board_id": str(WORK_ORDERS_BOARD_ID)}
    )

    boards = result.get("boards", [])

    if not boards:
        return {
            "error": "No work orders board found"
        }

    board = boards[0]

    return {
        "board_name": board["name"],
        "columns": board["columns"],
        "total_work_orders": len(
            board["items_page"]["items"]
        ),
        "items": board["items_page"]["items"]
    }
@app.get("/monday/work-orders/summary")
def work_orders_summary():

    result = monday_work_orders()

    items = result.get("items", [])

    total_work_orders = len(items)

    total_amount = 0
    total_billed = 0
    total_collected = 0
    total_receivable = 0

    for item in items:

        for column in item.get("column_values", []):

            column_id = column.get("id")
            value = column.get("text")

            if not value:
                continue

            try:
                number = float(value.replace(",", ""))
            except (ValueError, AttributeError):
                continue

            if column_id == "numeric_mm6qrd49":
                total_amount += number

            elif column_id == "numeric_mm6q14rv":
                total_billed += number

            elif column_id == "numeric_mm6q6ra":
                total_collected += number

            elif column_id == "numeric_mm6q9jkk":
                total_receivable += number

    return {
        "total_work_orders": total_work_orders,
        "total_amount": total_amount,
        "total_billed": total_billed,
        "total_collected": total_collected,
        "total_receivable": total_receivable
    }
@app.get("/monday/work-orders/status")
def work_orders_status():

    result = monday_work_orders()

    items = result.get("items", [])

    status_counts = {}

    for item in items:

        for column in item.get("column_values", []):

            if column.get("id") == "color_mm6qbp3h":

                status = column.get("text")

                if status:
                    status_counts[status] = (
                        status_counts.get(status, 0) + 1
                    )

    return {
        "status_counts": status_counts
    }
@app.get("/monday/work-orders/sectors")
def work_orders_sectors():

    result = monday_work_orders()

    items = result.get("items", [])

    sector_counts = {}

    for item in items:

        for column in item.get("column_values", []):

            if column.get("id") == "dropdown_mm6qbgtc":

                sector = column.get("text")

                if sector:
                    sector_counts[sector] = (
                        sector_counts.get(sector, 0) + 1
                    )

    return {
        "sector_counts": sector_counts
    }
@app.get("/monday/business-overview")
def business_overview():

    # Get Deals data
    deals_result = monday_deals()

    deal_boards = deals_result.get("boards", [])

    if not deal_boards:
        return {
            "error": "Deals board data not found"
        }

    deal_items = deal_boards[0]["items_page"]["items"]

    # Get Work Orders data
    work_result = monday_work_orders()

    work_items = work_result.get("items", [])

    # -------------------------
    # DEAL METRICS
    # -------------------------

    total_deals = len(deal_items)

    open_deals = 0
    won_deals = 0
    dead_deals = 0

    total_pipeline_value = 0

    for item in deal_items:

        status = None
        value = 0

        for column in item.get("column_values", []):

            # Deal Status
            if column.get("id") == "color_mm6qw8p6":
                status = column.get("text")

            # Deal Value
            if column.get("id") == "numeric_mm6q6w2g":

                raw_value = column.get("text")

                if raw_value:
                    try:
                        value = float(
                            raw_value.replace(",", "")
                        )
                    except ValueError:
                        value = 0

        if status == "Open":
            open_deals += 1

        elif status == "Won":
            won_deals += 1

        elif status == "Dead":
            dead_deals += 1

        total_pipeline_value += value

    # -------------------------
    # WORK ORDER METRICS
    # -------------------------

    total_work_orders = len(work_items)

    open_work_orders = 0
    closed_work_orders = 0

    for item in work_items:

        for column in item.get("column_values", []):

            if column.get("id") == "color_mm6qbp3h":

                status = column.get("text")

                if status == "Open":
                    open_work_orders += 1

                elif status == "Closed":
                    closed_work_orders += 1

    # -------------------------
    # RETURN OVERVIEW
    # -------------------------

    return {
        "deals": {
            "total": total_deals,
            "open": open_deals,
            "won": won_deals,
            "dead": dead_deals,
            "pipeline_value": total_pipeline_value
        },

        "work_orders": {
            "total": total_work_orders,
            "open": open_work_orders,
            "closed": closed_work_orders
        }
    }
@app.get("/monday/data-quality")
def data_quality():

    # Get deals
    deals_result = monday_deals()

    deal_boards = deals_result.get("boards", [])

    if not deal_boards:
        return {
            "error": "Deals board data not found"
        }

    deal_items = deal_boards[0]["items_page"]["items"]

    # Get work orders
    work_result = monday_work_orders()

    work_items = work_result.get("items", [])

    # -------------------------
    # DEAL QUALITY
    # -------------------------

    deals_missing_value = 0
    deals_missing_status = 0

    for item in deal_items:

        has_value = False
        has_status = False

        for column in item.get("column_values", []):

            if column.get("id") == "numeric_mm6q6w2g":
                if column.get("text"):
                    has_value = True

            if column.get("id") == "color_mm6qw8p6":
                if column.get("text"):
                    has_status = True

        if not has_value:
            deals_missing_value += 1

        if not has_status:
            deals_missing_status += 1

    # -------------------------
    # WORK ORDER QUALITY
    # -------------------------

    work_orders_missing_status = 0

    for item in work_items:

        has_status = False

        for column in item.get("column_values", []):

            if column.get("id") == "color_mm6qbp3h":

                if column.get("text"):
                    has_status = True

        if not has_status:
            work_orders_missing_status += 1

    # -------------------------
    # RETURN
    # -------------------------

    return {
        "deals": {
            "total": len(deal_items),
            "missing_value": deals_missing_value,
            "missing_status": deals_missing_status
        },

        "work_orders": {
            "total": len(work_items),
            "missing_status": work_orders_missing_status
        }
    }
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


@app.post("/monday/ask")
def ask_monday(request: QuestionRequest):

    question = request.question.lower()

    # -------------------------
    # GET DEAL DATA
    # -------------------------

    try:
        deals_result = monday_deals()

    except Exception as e:
        return {
            "error": "Unable to retrieve Deals data from Monday.com."
        }

    deal_boards = deals_result.get("boards", [])

    if not deal_boards:
        return {
            "error": "Deals board data not found"
        }

    deal_items = deal_boards[0]["items_page"]["items"]

    # -------------------------
    # GET WORK ORDER DATA
    # -------------------------

    try:
        work_result = monday_work_orders()

    except Exception as e:
        return {
            "error": "Unable to retrieve Work Orders data from Monday.com."
        }

    work_items = work_result.get("items", [])

    # -------------------------
    # TOTAL DEALS
    # -------------------------

    if "how many deals" in question:

        return {
            "answer": f"There are {len(deal_items)} deals."
        }

    # -------------------------
    # TOTAL WORK ORDERS
    # -------------------------

    if "how many work orders" in question:

        return {
            "answer": f"There are {len(work_items)} work orders."
        }

    # -------------------------
    # WORK ORDERS BY STATUS
    # -------------------------

    work_order_statuses = [
        "open",
        "closed"
    ]

    for status in work_order_statuses:

        if (
            status in question
            and "work order" in question
            and not (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
        ):

            count = 0

            for item in work_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "color_mm6qbp3h":

                        if column.get("text", "").lower() == status:
                            count += 1

            return {
                "answer": (
                    f"There are {count} "
                    f"{status.title()} work orders."
                )
            }
         # -------------------------
    # DEALS BY STATUS
    # -------------------------

    deal_statuses = [
        "open",
        "won",
        "dead",
        "on hold"
    ]

    for status in deal_statuses:

        if (
            status in question
            and "deal" in question
            and not (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
        ):

            count = 0

            for item in deal_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "color_mm6qw8p6":

                        if column.get("text", "").lower() == status:
                            count += 1

            return {
                "answer": f"There are {count} {status.title()} deals."
            }
        # -------------------------
    # DEAL VALUE BY STATUS
    # -------------------------

    for status in deal_statuses:

        if (
            status in question
            and "deal" in question
            and (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
        ):

            total_value = 0
            deal_count = 0

            for item in deal_items:

                item_status = None
                item_value = 0

                for column in item.get("column_values", []):

                    # Deal Status
                    if column.get("id") == "color_mm6qw8p6":

                        item_status = column.get(
                            "text", ""
                        ).lower()

                    # Deal Value
                    if column.get("id") == "numeric_mm6q6w2g":

                        raw_value = column.get("text")

                        if raw_value:

                            try:
                                item_value = float(
                                    raw_value.replace(",", "")
                                )

                            except ValueError:
                                item_value = 0

                if item_status == status:

                    deal_count += 1
                    total_value += item_value

            return {
                "answer": (
                    f"{status.title()} deals: "
                    f"{deal_count} deals with a total value of "
                    f"{total_value:,.2f}."
                )
            }


    # -------------------------
    # SECTORS
    # -------------------------

    sectors = [
        "mining",
        "powerline",
        "renewables",
        "railways",
        "construction",
        "tender",
        "dsp",
        "aviation",
        "manufacturing",
        "others"
    ]


    # -------------------------
    # COMPARE DEAL VALUES
    # -------------------------

    if (
    "compare" in question
    and "work order" not in question
    and (
        "value" in question
        or "amount" in question
        or "worth" in question
    )
    ):

        found_sectors = []

        for sector in sectors:

            if sector in question:
                found_sectors.append(sector)

        if len(found_sectors) >= 2:

            sector1 = found_sectors[0]
            sector2 = found_sectors[1]

            value1 = 0
            value2 = 0

            for item in deal_items:

                item_sector = None
                item_value = 0

                for column in item.get("column_values", []):

                    # Sector
                    if column.get("id") == "color_mm6qqdye":

                        item_sector = column.get(
                            "text", ""
                        ).lower()

                    # Deal Value
                    if column.get("id") == "numeric_mm6q6w2g":

                        raw_value = column.get("text")

                        if raw_value:

                            try:
                                item_value = float(
                                    raw_value.replace(",", "")
                                )

                            except ValueError:
                                item_value = 0

                if item_sector == sector1:
                    value1 += item_value

                elif item_sector == sector2:
                    value2 += item_value


            if value1 > value2:

                comparison = (
                    f"{sector1.title()} has the higher deal value."
                )

            elif value2 > value1:

                comparison = (
                    f"{sector2.title()} has the higher deal value."
                )

            else:

                comparison = (
                    "Both sectors have the same deal value."
                )


            return {
                "answer": (
                    f"{sector1.title()} has a total deal value of "
                    f"{value1:,.2f}, while {sector2.title()} has "
                    f"{value2:,.2f}. {comparison}"
                )
            }


    # -------------------------
    # COMPARE TWO DEAL SECTORS
    # -------------------------

    if (
        "compare" in question
        and "deal" in question
        and "work order" not in question
        and (
            "value" in question
            or "amount" in question
            or "worth" in question
        )
    ):

        found_sectors = []

        for sector in sectors:

            if sector in question:
                found_sectors.append(sector)

        if len(found_sectors) >= 2:

            sector1 = found_sectors[0]
            sector2 = found_sectors[1]

            count1 = 0
            count2 = 0

            for item in deal_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "color_mm6qqdye":

                        sector_name = column.get(
                            "text", ""
                        ).lower()

                        if sector_name == sector1:
                            count1 += 1

                        elif sector_name == sector2:
                            count2 += 1


            if count1 > count2:

                comparison = (
                    f"{sector1.title()} has more deals."
                )

            elif count2 > count1:

                comparison = (
                    f"{sector2.title()} has more deals."
                )

            else:

                comparison = (
                    "Both sectors have the same number of deals."
                )


            return {
                "answer": (
                    f"{sector1.title()} has {count1} deals, "
                    f"while {sector2.title()} has {count2} deals. "
                    f"{comparison}"
                )
            }
    # -------------------------
    # COMPARE TWO WORK ORDER SECTORS
    # -------------------------

    if (
        "compare" in question
        and "work order" in question
        and not (
            "value" in question
            or "amount" in question
            or "worth" in question
        )
    ):

        found_sectors = []

        for sector in sectors:

            if sector in question:
                found_sectors.append(sector)

        if len(found_sectors) >= 2:

            sector1 = found_sectors[0]
            sector2 = found_sectors[1]

            count1 = 0
            count2 = 0

            for item in work_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "dropdown_mm6qbgtc":

                        sector_name = column.get(
                            "text", ""
                        ).lower()

                        if sector_name == sector1:
                            count1 += 1

                        elif sector_name == sector2:
                            count2 += 1

            if count1 > count2:

                comparison = (
                    f"{sector1.title()} has more work orders."
                )

            elif count2 > count1:

                comparison = (
                    f"{sector2.title()} has more work orders."
                )

            else:

                comparison = (
                    "Both sectors have the same number "
                    "of work orders."
                )

            return {
                "answer": (
                    f"{sector1.title()} has {count1} work orders, "
                    f"while {sector2.title()} has {count2} work orders. "
                    f"{comparison}"
                )
            }
    # -------------------------
    # COMPARE WORK ORDER VALUES BY SECTOR
    # -------------------------

    if (
        "compare" in question
        and "work order" in question
        and (
            "value" in question
            or "amount" in question
            or "worth" in question
        )
    ):

        found_sectors = []

        for sector in sectors:

            if sector in question:
                found_sectors.append(sector)

        if len(found_sectors) >= 2:

            sector1 = found_sectors[0]
            sector2 = found_sectors[1]

            value1 = 0
            value2 = 0

            for item in work_items:

                item_sector = None
                item_value = 0

                for column in item.get("column_values", []):

                    # Sector
                    if column.get("id") == "dropdown_mm6qbgtc":

                        item_sector = column.get(
                            "text", ""
                        ).lower()

                    # Work Order Amount
                    if column.get("id") == "numeric_mm6qrd49":

                        raw_value = column.get("text")

                        if raw_value:

                            try:
                                item_value = float(
                                    raw_value.replace(",", "")
                                )

                            except ValueError:
                                item_value = 0

                if item_sector == sector1:
                    value1 += item_value

                elif item_sector == sector2:
                    value2 += item_value

            if value1 > value2:

                comparison = (
                    f"{sector1.title()} has the higher work order value."
                )

            elif value2 > value1:

                comparison = (
                    f"{sector2.title()} has the higher work order value."
                )

            else:

                comparison = (
                    "Both sectors have the same work order value."
                )

            return {
                "answer": (
                    f"{sector1.title()} has a total work order value of "
                    f"{value1:,.2f}, while {sector2.title()} has "
                    f"{value2:,.2f}. {comparison}"
                )
            }
    # -------------------------
    # DEALS BY SECTOR
    # -------------------------

    for sector in sectors:

        if (
            sector in question
            and "deal" in question
            and "compare" not in question
        ):

            count = 0

            for item in deal_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "color_mm6qqdye":

                        if column.get(
                            "text", ""
                        ).lower() == sector:

                            count += 1


            return {
                "answer": (
                    f"There are {count} deals "
                    f"in {sector.title()}."
                )
            }

        # -------------------------
    # WORK ORDER VALUE BY STATUS
    # -------------------------

    work_order_statuses = [
        "open",
        "closed"
    ]

    for status in work_order_statuses:

        if (
            status in question
            and "work order" in question
            and (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
        ):

            total_value = 0
            work_order_count = 0

            for item in work_items:

                item_status = None
                item_value = 0

                for column in item.get("column_values", []):

                    # Work Order Status
                    if column.get("id") == "color_mm6qbp3h":

                        item_status = column.get(
                            "text", ""
                        ).lower()

                    # Work Order Amount
                    if column.get("id") == "numeric_mm6qrd49":

                        raw_value = column.get("text")

                        if raw_value:

                            try:
                                item_value = float(
                                    raw_value.replace(",", "")
                                )

                            except ValueError:
                                item_value = 0

                if item_status == status:

                    work_order_count += 1
                    total_value += item_value

            return {
                "answer": (
                    f"{status.title()} work orders: "
                    f"{work_order_count} work orders with a "
                    f"total value of {total_value:,.2f}."
                )
            }
       # -------------------------
    # WORK ORDER VALUE BY SECTOR
    # -------------------------

    for sector in sectors:

        if (
            sector in question
            and "work order" in question
            and (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
        ):

            total_value = 0
            work_order_count = 0

            for item in work_items:

                item_sector = None
                item_value = 0

                for column in item.get(
                    "column_values", []
                ):

                    # Sector
                    if column.get(
                        "id"
                    ) == "dropdown_mm6qbgtc":

                        item_sector = column.get(
                            "text", ""
                        ).lower()

                    # Work Order Amount
                    if column.get(
                        "id"
                    ) == "numeric_mm6qrd49":

                        raw_value = column.get("text")

                        if raw_value:

                            try:
                                item_value = float(
                                    raw_value.replace(",", "")
                                )

                            except ValueError:
                                item_value = 0

                if item_sector == sector:

                    work_order_count += 1
                    total_value += item_value

            return {
                "answer": (
                    f"{sector.title()} work orders: "
                    f"{work_order_count} work orders with a "
                    f"total value of {total_value:,.2f}."
                )
            }


    # -------------------------
    # WORK ORDERS BY SECTOR
    # -------------------------

    for sector in sectors:

        if (
            sector in question
            and "work order" in question
            and not (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
        ):

            count = 0

            for item in work_items:

                for column in item.get(
                    "column_values", []
                ):

                    if column.get(
                        "id"
                    ) == "dropdown_mm6qbgtc":

                        if column.get(
                            "text", ""
                        ).lower() == sector:

                            count += 1

            return {
                "answer": (
                    f"There are {count} work orders "
                    f"in {sector.title()}."
                )
            }

    # -------------------------
    # DEAL VALUE BY SECTOR
    # -------------------------

    for sector in sectors:

        if (
            sector in question
            and (
                "value" in question
                or "amount" in question
                or "worth" in question
            )
            and "compare" not in question
        ):

            total_value = 0
            deal_count = 0

            for item in deal_items:

                item_sector = None
                item_value = None

                for column in item.get(
                    "column_values", []
                ):

                    # Sector
                    if column.get(
                        "id"
                    ) == "color_mm6qqdye":

                        item_sector = column.get(
                            "text", ""
                        ).lower()

                    # Market Deal Value
                    if column.get(
                        "id"
                    ) == "numeric_mm6q6w2g":

                        raw_value = column.get("text")

                        if raw_value:

                            try:

                                item_value = float(
                                    raw_value.replace(",", "")
                                )

                            except ValueError:

                                item_value = 0


                if item_sector == sector:

                    deal_count += 1

                    if item_value is not None:

                        total_value += item_value


            return {
                "sector": sector.title(),
                "deal_count": deal_count,
                "total_value": total_value
            }
        # -------------------------
    # HIGHEST VALUE SECTOR
    # -------------------------

    if (
        "highest value" in question
        or "highest deal value" in question
        or "largest deal value" in question
        or "most valuable sector" in question
    ):

        sector_values = {}

        for item in deal_items:

            item_sector = None
            item_value = 0

            for column in item.get("column_values", []):

                # Sector
                if column.get("id") == "color_mm6qqdye":

                    item_sector = column.get(
                        "text", ""
                    )

                # Deal Value
                if column.get("id") == "numeric_mm6q6w2g":

                    raw_value = column.get("text")

                    if raw_value:

                        try:
                            item_value = float(
                                raw_value.replace(",", "")
                            )

                        except ValueError:
                            item_value = 0

            if item_sector:

                sector_values[item_sector] = (
                    sector_values.get(item_sector, 0)
                    + item_value
                )

        if sector_values:

            highest_sector = max(
                sector_values,
                key=sector_values.get
            )

            highest_value = sector_values[highest_sector]

            return {
                "answer": (
                    f"{highest_sector} has the highest "
                    f"deal value at "
                    f"{highest_value:,.2f}."
                )
            }

    # -------------------------
    # LARGEST DEAL SECTOR
    # -------------------------

    if (
        "which sector" in question
        or "largest sector" in question
        or "most deals" in question
        or "highest number of deals" in question
    ):

        sector_counts = {}

        for item in deal_items:

            for column in item.get(
                "column_values", []
            ):

                if column.get(
                    "id"
                ) == "color_mm6qqdye":

                    sector = column.get("text")

                    if sector:

                        sector_counts[sector] = (
                            sector_counts.get(
                                sector, 0
                            ) + 1
                        )


        if sector_counts:

            largest_sector = max(
                sector_counts,
                key=sector_counts.get
            )

            return {
                "answer": (
                    f"{largest_sector} has the most deals "
                    f"with {sector_counts[largest_sector]} deals."
                )
            }

        # -------------------------
    # TOTAL PIPELINE VALUE
    # -------------------------

    if (
        "pipeline value" in question
        or "total pipeline" in question
        or "total deal value" in question
    ):

        total_pipeline_value = 0

        for item in deal_items:

            for column in item.get("column_values", []):

                if column.get("id") == "numeric_mm6q6w2g":

                    raw_value = column.get("text")

                    if raw_value:

                        try:
                            total_pipeline_value += float(
                                raw_value.replace(",", "")
                            )

                        except ValueError:
                            pass

        return {
            "answer": (
                f"The total pipeline value is "
                f"{total_pipeline_value:,.2f}."
            )
        }
        # -------------------------
    # BUSINESS SUMMARY
    # -------------------------

    if (
        "summary" in question
        or "overall summary" in question
        or "business summary" in question
    ):

        # -------------------------
        # DEAL SUMMARY
        # -------------------------

        deal_total = len(deal_items)

        deal_open = 0
        deal_won = 0
        deal_dead = 0
        deal_pipeline_value = 0

        for item in deal_items:

            item_status = None
            item_value = 0

            for column in item.get("column_values", []):

                # Deal Status
                if column.get("id") == "color_mm6qw8p6":

                    item_status = column.get(
                        "text", ""
                    ).lower()

                # Deal Value
                if column.get("id") == "numeric_mm6q6w2g":

                    raw_value = column.get("text")

                    if raw_value:

                        try:
                            item_value = float(
                                raw_value.replace(",", "")
                            )

                        except ValueError:
                            item_value = 0

            if item_status == "open":
                deal_open += 1

            elif item_status == "won":
                deal_won += 1

            elif item_status == "dead":
                deal_dead += 1

            deal_pipeline_value += item_value


        # -------------------------
        # WORK ORDER SUMMARY
        # -------------------------

        work_total = len(work_items)

        work_open = 0
        work_closed = 0
        work_total_value = 0

        for item in work_items:

            item_status = None
            item_value = 0

            for column in item.get("column_values", []):

                # Work Order Status
                if column.get("id") == "color_mm6qbp3h":

                    item_status = column.get(
                        "text", ""
                    ).lower()

                # Work Order Amount
                if column.get("id") == "numeric_mm6qrd49":

                    raw_value = column.get("text")

                    if raw_value:

                        try:
                            item_value = float(
                                raw_value.replace(",", "")
                            )

                        except ValueError:
                            item_value = 0

            if item_status == "open":
                work_open += 1

            elif item_status == "closed":
                work_closed += 1

            work_total_value += item_value


        return {
            "answer": (
                f"Deals: {deal_total}\n"
                f"Open deals: {deal_open}\n"
                f"Won deals: {deal_won}\n"
                f"Dead deals: {deal_dead}\n"
                f"Pipeline value: {deal_pipeline_value:,.2f}\n\n"
                f"Work orders: {work_total}\n"
                f"Open work orders: {work_open}\n"
                f"Closed work orders: {work_closed}\n"
                f"Total work order value: "
                f"{work_total_value:,.2f}"
            )
        }
        # -------------------------
    # DATA QUALITY
    # -------------------------

    if (
        "data quality" in question
        or "missing data" in question
        or "data issues" in question
        or "incomplete data" in question
        or "missing values" in question
        or "data complete" in question
    ):

        deal_missing_value = 0
        deal_missing_status = 0

        # Check Deals
        for item in deal_items:

            has_value = False
            has_status = False

            for column in item.get("column_values", []):

                # Deal Value
                if column.get("id") == "numeric_mm6q6w2g":

                    value = column.get("text")

                    if value and value.strip():
                        has_value = True

                # Deal Status
                if column.get("id") == "color_mm6qw8p6":

                    status = column.get("text")

                    if status and status.strip():
                        has_status = True

            if not has_value:
                deal_missing_value += 1

            if not has_status:
                deal_missing_status += 1


        work_missing_value = 0
        work_missing_status = 0

        # Check Work Orders
        for item in work_items:

            has_value = False
            has_status = False

            for column in item.get("column_values", []):

                # Work Order Amount
                if column.get("id") == "numeric_mm6qrd49":

                    value = column.get("text")

                    if value and value.strip():
                        has_value = True

                # Work Order Status
                if column.get("id") == "color_mm6qbp3h":

                    status = column.get("text")

                    if status and status.strip():
                        has_status = True

            if not has_value:
                work_missing_value += 1

            if not has_status:
                work_missing_status += 1


        return {
            "answer": (
                f"Data quality summary:\n\n"
                f"Deals: {len(deal_items)} total, "
                f"{deal_missing_value} missing values, "
                f"{deal_missing_status} missing statuses.\n"
                f"Work orders: {len(work_items)} total, "
                f"{work_missing_value} missing values, "
                f"{work_missing_status} missing statuses.\n\n"
                f"These missing fields may affect financial "
                f"totals and status-based analysis."
            )
        }
        # -------------------------
    # PIPELINE HEALTH
    # -------------------------

    if (
        "pipeline health" in question
        or "how is our pipeline" in question
        or "pipeline looking" in question
        or "pipeline performance" in question
    ):

        total_deals = len(deal_items)

        open_deals = 0
        won_deals = 0
        dead_deals = 0
        pipeline_value = 0

        for item in deal_items:

            status = None
            value = 0

            for column in item.get("column_values", []):

                if column.get("id") == "color_mm6qw8p6":

                    status = column.get(
                        "text", ""
                    ).lower()

                if column.get("id") == "numeric_mm6q6w2g":

                    raw_value = column.get("text")

                    if raw_value:

                        try:
                            value = float(
                                raw_value.replace(",", "")
                            )
                        except ValueError:
                            value = 0

            if status == "open":
                open_deals += 1

            elif status == "won":
                won_deals += 1

            elif status == "dead":
                dead_deals += 1

            if status == "open":
                pipeline_value += value


        if total_deals > 0:

            won_percentage = (
                won_deals / total_deals
            ) * 100

            dead_percentage = (
                dead_deals / total_deals
            ) * 100

        else:

            won_percentage = 0
            dead_percentage = 0


        return {
            "answer": (
                f"Pipeline health:\n\n"
                f"Total deals: {total_deals}\n"
                f"Open deals: {open_deals}\n"
                f"Won deals: {won_deals}\n"
                f"Dead deals: {dead_deals}\n"
                f"Open pipeline value: "
                f"{pipeline_value:,.2f}\n"
                f"Win rate: {won_percentage:.2f}%\n"
                f"Dead deal rate: {dead_percentage:.2f}%"
            )
        }
        # -------------------------
    # WORK ORDER FINANCIAL SUMMARY
    # -------------------------

    if (
        "revenue" in question
        or "billed" in question
        or "collected" in question
        or "receivable" in question
    ):

        total_amount = 0
        total_billed = 0
        total_collected = 0
        total_receivable = 0

        for item in work_items:

            for column in item.get("column_values", []):

                raw_value = column.get("text")

                if not raw_value:
                    continue

                try:
                    value = float(
                        raw_value.replace(",", "")
                    )
                except ValueError:
                    continue


                if column.get("id") == "numeric_mm6q14rv":

                    total_amount += value

                elif column.get("id") == "numeric_mm6qzjxp":

                    total_billed += value

                elif column.get("id") == "numeric_mm6q3khc":

                    total_collected += value

                elif column.get("id") == "numeric_mm6qw021":

                    total_receivable += value


        return {
            "answer": (
                f"Financial summary:\n\n"
                f"Total work order amount: "
                f"{total_amount:,.2f}\n"
                f"Total billed: "
                f"{total_billed:,.2f}\n"
                f"Total collected: "
                f"{total_collected:,.2f}\n"
                f"Total receivable: "
                f"{total_receivable:,.2f}"
            )
        }
        # -------------------------
    # CROSS BOARD SECTOR ANALYSIS
    # -------------------------

    if (
        "compare" in question
        and "deal" in question
        and "work order" in question
        and "value" not in question
        and "amount" not in question
        and "worth" not in question
    ):

        found_sectors = []

        for sector in sectors:

            if sector in question:
                found_sectors.append(sector)

        if len(found_sectors) >= 1:

            sector = found_sectors[0]

            deal_count = 0
            work_count = 0

            # Deals
            for item in deal_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "color_mm6qqdye":

                        if column.get(
                            "text", ""
                        ).lower() == sector:

                            deal_count += 1


            # Work Orders
            for item in work_items:

                for column in item.get("column_values", []):

                    if column.get("id") == "dropdown_mm6qbgtc":

                        if column.get(
                            "text", ""
                        ).lower() == sector:

                            work_count += 1


            return {
                "answer": (
                    f"{sector.title()} has "
                    f"{deal_count} deals and "
                    f"{work_count} work orders."
                )
            }
            # -------------------------
    # FOUNDER PIPELINE QUESTIONS
    # -------------------------

    if (
        "strongest sector" in question
        or "best performing sector" in question
        or "top sector" in question
    ):

        sector_counts = {}

        for item in deal_items:

            for column in item.get("column_values", []):

                if column.get("id") == "color_mm6qqdye":

                    sector = column.get("text")

                    if sector:

                        sector_counts[sector] = (
                            sector_counts.get(
                                sector, 0
                            ) + 1
                        )

        if sector_counts:

            best_sector = max(
                sector_counts,
                key=sector_counts.get
            )

            return {
                "answer": (
                    f"{best_sector} is currently the "
                    f"strongest sector by deal volume, "
                    f"with {sector_counts[best_sector]} deals."
                )
            }
        # -------------------------
    # CLARIFY AMBIGUOUS QUESTIONS
    # -------------------------

    if (
        any(sector in question for sector in sectors)
        and "doing" in question
        and not (
            "deal" in question
            or "work order" in question
            or "value" in question
            or "amount" in question
            or "revenue" in question
        )
    ):

        return {
            "answer": (
                "Do you want me to analyze the "
                "deals, deal value, work orders, "
                "or financial performance?"
            )
        }
        # -------------------------
    # LEADERSHIP UPDATE
    # -------------------------

    if (
        "leadership update" in question
        or "executive update" in question
        or "management update" in question
        or "founder update" in question
    ):

        total_deals = len(deal_items)
        total_work_orders = len(work_items)

        open_deals = 0
        won_deals = 0
        dead_deals = 0
        pipeline_value = 0

        for item in deal_items:

            status = None
            value = 0

            for column in item.get("column_values", []):

                if column.get("id") == "color_mm6qw8p6":

                    status = column.get(
                        "text", ""
                    ).lower()

                if column.get("id") == "numeric_mm6q6w2g":

                    raw_value = column.get("text")

                    if raw_value:

                        try:
                            value = float(
                                raw_value.replace(",", "")
                            )
                        except ValueError:
                            value = 0

            if status == "open":
                open_deals += 1

                pipeline_value += value

            elif status == "won":
                won_deals += 1

            elif status == "dead":
                dead_deals += 1


        open_work_orders = 0
        closed_work_orders = 0

        for item in work_items:

            for column in item.get("column_values", []):

                if column.get("id") == "color_mm6qbp3h":

                    status = column.get(
                        "text", ""
                    ).lower()

                    if status == "open":
                        open_work_orders += 1

                    elif status == "closed":
                        closed_work_orders += 1


        return {
            "answer": (
                "Leadership Update\n\n"
                f"Sales: {total_deals} total deals, "
                f"{open_deals} open, "
                f"{won_deals} won, and "
                f"{dead_deals} dead.\n\n"
                f"Open pipeline value: "
                f"{pipeline_value:,.2f}.\n\n"
                f"Operations: {total_work_orders} "
                f"work orders, including "
                f"{open_work_orders} open and "
                f"{closed_work_orders} closed.\n\n"
                "Management should focus on open pipeline "
                "conversion, dead deals, and outstanding "
                "operational workload."
            )
        }
    # -------------------------
    # UNKNOWN QUESTION
    # -------------------------

    return {
        "answer": (
            "I don't know how to answer that question yet."
        )
    }