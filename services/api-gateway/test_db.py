import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in your .env file.")
    exit(1)

supabase: Client = create_client(url, key)

try:
    # A basic test query to check connection (e.g. attempting to list tables or get a mock table)
    # Since we haven't created tables yet, just authenticating and doing a dummy query works.
    response = supabase.table("users").select("*").limit(1).execute()
    print("Successfully connected to Supabase!")
    print(f"Data: {response.data}")
except Exception as e:
    print(f"Connection test failed: {e}")
