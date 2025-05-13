import requests
import sqlite3
from datetime import datetime
import time 
while True:
    
    API_KEY = "05993134-5ba3-48c3-a076-9b9948a83aef"

    
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    
    symbols = "BTC,ETH,XRP,SOL,ADA,USDT"

    
    params = {
        "symbol": symbols,
        "convert": "EUR"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    }

    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    
    timestamp = datetime.now().isoformat()

    
    conn = sqlite3.connect("cryptos.db")
    cursor = conn.cursor()

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crypto TEXT,
        symbol TEXT,
        price REAL,
        timestamp TEXT
    )
    """)

    print("\n📊 Prix des cryptomonnaies (en EUR) :\n")

    
    for symbol in symbols.split(","):
        info = data["data"][symbol]
        name = info["name"]
        price = info["quote"]["EUR"]["price"]
        
        
        cursor.execute(
            "INSERT INTO prices (crypto, symbol, price, timestamp) VALUES (?, ?, ?, ?)",
            (name, symbol, price, timestamp)
        )
        
        
        print(f"{name} ({symbol}) : {price:.2f} €")

    
    conn.commit()
    conn.close()

    print(f"\n✅ Données enregistrées à {timestamp}\n")
    time.sleep(10)
