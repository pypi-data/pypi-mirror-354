import requests

def create_asana_task(personal_access_token, project_id, task_name, notes=None, assignee=None):
    url = "https://app.asana.com/api/1.0/tasks"
    headers = {
        "Authorization": f"Bearer {personal_access_token}"
    }

    data = {
        "name": task_name,
        "projects": [project_id],  # Important: must be a list
    }

    if notes:
        data["notes"] = notes
    if assignee:
        data["assignee"] = assignee

    print("🔍 Requesting Asana with payload:")
    print(data)

    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("❌ API Status Code:", response.status_code)
        try:
            print("❌ Asana API Response:", response.json())
        except Exception:
            print("❌ Couldn't parse response JSON")
        raise

    print("✅ Task created successfully!")
    return response.json()
