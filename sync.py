import os

api_key = os.getenv("HEVY_API_KEY")

if api_key:
    print("✅ Clé API trouvée.")
else:
    raise Exception("❌ La clé API HEVY_API_KEY est introuvable.")
