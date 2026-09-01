import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_workflow():
    print("1. Testing Root endpoint...")
    r = client.get("/")
    assert r.status_code == 200, f"Root failed: {r.text}"
    print("   [OK] Root OK")

    print("2. Testing Parse endpoint with Mock/Demo data (query='барбершоп москва', limit=5)...")
    r = client.post("/api/parse", json={
        "query": "барбершоп москва",
        "limit": 5,
        "filter_type": "all",
        "is_mock": True
    })
    assert r.status_code == 200, f"Parse failed: {r.text}"
    session_data = r.json()
    session_id = session_data["id"]
    leads = session_data["leads"]
    print(f"   [OK] Session created: {session_id}, leads count: {len(leads)}")
    assert len(leads) > 0, "No leads returned"

    first_lead = leads[0]
    lead_id = first_lead["id"]
    print(f"   [OK] First lead: @{first_lead['username']}, link_type={first_lead['link_type']}, status={first_lead['link_label']}")

    print("3. Testing Lead update (contacted=True, reply_status='В диалоге')...")
    r = client.patch(f"/api/leads/{lead_id}", json={
        "contacted": True,
        "reply_status": "В диалоге",
        "notes": "Написал в директ, жду ответ"
    })
    assert r.status_code == 200, f"Lead update failed: {r.text}"
    updated_lead = r.json()
    assert updated_lead["contacted"] is True
    assert updated_lead["reply_status"] == "В диалоге"
    print("   [OK] Lead updated successfully")

    print("4. Testing Sessions list...")
    r = client.get("/api/sessions")
    assert r.status_code == 200
    sessions = r.json()
    assert len(sessions) >= 1
    print(f"   [OK] Found {len(sessions)} session(s)")

    print("5. Testing Excel export generation...")
    r = client.get(f"/api/sessions/{session_id}/export")
    assert r.status_code == 200
    assert len(r.content) > 1000
    print(f"   [OK] Excel generated ({len(r.content)} bytes)")

    print("6. Testing AI Offer template generation...")
    r = client.post("/api/generate-offer", json={
        "username": first_lead["username"],
        "full_name": first_lead["full_name"],
        "niche": "барбершоп",
        "link_type": "no_site",
        "tone": "business"
    })
    assert r.status_code == 200
    offer = r.json()
    print(f"   [OK] Offer generated subject: '{offer['subject']}'")

    print("\nAll automated tests passed successfully!")

if __name__ == "__main__":
    test_workflow()