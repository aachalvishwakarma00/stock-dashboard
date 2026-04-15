from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import get_stock_data, process_data

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

companies = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]

@app.get("/")
def home():
    return {"message": "Stock Dashboard API Running 🚀"}

@app.get("/companies")
def get_companies():
    return companies

@app.get("/data/{symbol}")
def get_data(symbol: str):
    try:
        df = get_stock_data(symbol)

        if df.empty:
            return {"error": "No data found"}

        df, _, _ = process_data(df)

        # SAFE conversion
        df = df.tail(30)

        df = df.fillna(0)

        # Convert all values to serializable
        result = []
        for _, row in df.iterrows():
            result.append({
                "Date": str(row.get("Date", "")),
                "Open": float(row.get("Open", 0)),
                "Close": float(row.get("Close", 0)),
                "High": float(row.get("High", 0)),
                "Low": float(row.get("Low", 0))
            })

        return result

    except Exception as e:
        return {"error": str(e)}

@app.get("/summary/{symbol}")
def summary(symbol: str):
    df = get_stock_data(symbol)
    df, high, low = process_data(df)

    return {
        "52_week_high": float(high),
        "52_week_low": float(low),
        "average_close": float(df["Close"].mean())
    }

@app.get("/compare")
def compare(symbol1: str, symbol2: str):
    df1 = get_stock_data(symbol1)
    df2 = get_stock_data(symbol2)

    return {
        symbol1: float(df1["Close"].mean()),
        symbol2: float(df2["Close"].mean())
    }