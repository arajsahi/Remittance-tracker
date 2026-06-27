import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
from flask import Flask, render_template_string
from dotenv import load_dotenv
load_dotenv()

def get_wise_rate():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    data = response.json()
    rate = data["rates"]["NPR"]
    print(f"Market USD rate: {rate} NPR")
    return rate

def get_nrb_rate():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://www.nrb.org.np/api/forex/v1/rates?from={today}&to={today}&per_page=5&page=1"
    response = requests.get(url)
    data = response.json()
    rates = data["data"]["payload"][0]["rates"]
    for rate in rates:
        if rate["currency"]["iso3"] == "USD":
            buy = rate["buy"]
            sell = rate["sell"]
            print(f"NRB USD buy rate: {buy} NPR")
            print(f"NRB USD sell rate: {sell} NPR")
            return buy, sell


def save_to_db(service,buy,sell):
    conn = psycopg2.connect(
        dbname="mydb",
        user="arajsahi",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rates(service,rate,currency,timestamp) VALUES(%s,%s,%s,%s)",
        (service,float(buy),"USD-NPR",datetime.now())
    )
    conn.commit()
    conn.close()
    print(f"Saved{service} rate to database!")

buy, sell = get_nrb_rate()
save_to_db("NRB",buy,sell)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Nepal Remittance Tracker</title>
<style>
  body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; background: #f5f5f5; padding: 20px; }
  h1 { color: #c0392b; }
  table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
  th { background: #c0392b; color: white; padding: 12px; text-align: left; }
  td { padding: 12px; border-bottom: 1px solid #eee; }
  tr:hover { background: #f9f9f9; }
</style>
</head>
<body>
<h1>🇳🇵 Nepal Remittance Rate Tracker</h1>
<h3>USD to NPR rates</h3>
<table>
  <tr><th>Service</th><th>Rate</th><th>Currency</th><th>Updated</th></tr>
  {% for row in rates %}
  <tr>
    <td>{{ row[1] }}</td>
    <td>{{ row[2] }} NPR</td>
    <td>{{ row[3] }}</td>
    <td>{{ row[4] }}</td>
  </tr>
  {% endfor %}
</table>
</body>
</html>
"""

@app.route("/")
def index():
    conn = psycopg2.connect(dbname="mydb", user="arajsahi", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rates ORDER BY timestamp DESC LIMIT 10")
    rates = cursor.fetchall()
    conn.close()
    return render_template_string(HTML, rates=rates)
wise_rate = get_wise_rate()
save_to_db("WISE",wise_rate,wise_rate)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

