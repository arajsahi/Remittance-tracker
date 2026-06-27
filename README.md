# Nepal Remittance Rate Tracker 🇳🇵

A Flask web app that fetches live USD to NPR exchange rates from Nepal Rastra Bank (NRB) and stores historical data in a PostgreSQL database.

## What it does

- Fetches live USD to NPR exchange rates from Nepal Rastra Bank official API
- Saves rates to PostgreSQL database with timestamps
- Displays rate history in a clean web interface
- Tracks how rates change over time

## Tools and Technologies

- Python
- Flask
- PostgreSQL + psycopg2
- Nepal Rastra Bank (NRB) FOREX API
- BeautifulSoup
- python-dotenv

## Setup

1. Clone the repo
2. Install PostgreSQL and create a database called `mydb`
3. Create a `rates` table:
```sql
CREATE TABLE rates (
    id SERIAL PRIMARY KEY,
    service VARCHAR(50),
    rate FLOAT,
    currency VARCHAR(20),
    timestamp TIMESTAMP
);
```
4. Run `pip install flask requests psycopg2-binary beautifulsoup4 python-dotenv`
5. Run `python remittance.py`
6. Open `http://127.0.0.1:5001`

## Built by

Araj Sahi — Python Developer based in Toronto 🇨🇦
github.com/arajsahi
