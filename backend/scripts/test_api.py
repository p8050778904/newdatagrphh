import httpx

BASE_URL = "http://127.0.0.1:8000/api"

queries = [
    "Give me sales by region",
    "Show brand performance",
    "Top employees by revenue"
]

def test_query(query):
    print(f"\nTesting query: {query}")
    try:
        r = httpx.post(f"{BASE_URL}/query", json={"query": query}, timeout=30.0)
        # Print full JSON response as requested by the instruction description
        print(f"Full JSON Response: {r.json()}")
        
        data = r.json()
        print(f"Title: {data.get('title')}")
        print(f"Chart Type: {data.get('chart_type')}")
        print(f"Data count: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"First 2 records: {data.get('data')[:2]}")
        else:
            print("DATA IS EMPTY")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    for q in queries:
        test_query(q)
