# Skylark Drones - Monday.com Business Intelligence Agent

## Overview

This project is a FastAPI-based Business Intelligence Agent that connects
dynamically to Monday.com and answers founder-level business questions
across Deals and Work Orders boards.

The agent retrieves data directly from Monday.com rather than using
hardcoded CSV data.

## Architecture

User
  ↓
FastAPI API
  ↓
Question Understanding
  ↓
Monday.com API
  ↓
Deals / Work Orders Boards
  ↓
Data Processing & Business Logic
  ↓
Business Intelligence Response

## Features

- Monday.com API integration
- Dynamic retrieval of Deals data
- Dynamic retrieval of Work Orders data
- Deal status analysis
- Deal sector analysis
- Deal value analysis
- Work order status analysis
- Work order sector analysis
- Pipeline health analysis
- Data quality reporting
- Comparison between sectors
- Missing/null value handling
- Graceful API error handling

## Example Questions

- How many deals are there?
- How many open deals are there?
- What is the total pipeline value?
- Which sector has the most deals?
- Which sector has the highest deal value?
- How many work orders are there?
- How many open work orders are there?
- Which sector has the most work orders?
- Compare Mining and Renewables.
- Give me a pipeline health summary.
- Give me a data quality summary.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Requests
- python-dotenv
- Monday.com GraphQL API
- Render

## Environment Variables

Create a `.env` file locally:

MONDAY_API_TOKEN=your_monday_api_token
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id

Do not commit `.env` or API tokens to GitHub.

## Local Setup

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY>

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

uvicorn app:app --reload

Open:

http://127.0.0.1:8000/docs

## Hosted Prototype

https://business-intelligence-agent-p8ry.onrender.com

Swagger API:

https://business-intelligence-agent-p8ry.onrender.com/docs

## Monday.com Configuration

Two separate Monday.com boards are used:

1. Deals
2. Work Orders

The application reads the board data dynamically through the Monday.com API.

## Data Resilience

The application handles:

- Missing values
- Missing statuses
- Empty fields
- Numeric values containing commas
- Incomplete records
- API retrieval failures

Data-quality summaries are provided where missing fields may affect analysis.

## API Endpoint

POST /monday/ask

Example request:

{
  "question": "How many open deals are there?"
}

Example response:

{
  "answer": "There are 49 Open deals."
}

## Leadership Updates

The agent can provide summarized business information such as:

- Pipeline health
- Open and won deals
- Pipeline value
- Win rate
- Work order status
- Sector performance
- Data quality caveats

## Limitations and Future Improvements

With more development time, the agent could include:

- More advanced natural-language query understanding
- Date/quarter filtering
- More sophisticated normalization
- Automated charts
- Automated leadership reports
- More comprehensive API retry handling
