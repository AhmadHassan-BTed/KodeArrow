import subprocess
import requests
import os
import sys

def get_github_token():
    try:
        p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = p.communicate('protocol=https\nhost=github.com\n\n')
        token = None
        for line in stdout.split('\n'):
            if line.startswith('password='):
                token = line.split('=', 1)[1].strip()
                break
        return token
    except Exception as e:
        print(f"Error fetching token from credential manager: {e}")
        return None

def update_release_asset():
    token = get_github_token()
    if not token:
        print("Could not retrieve GitHub Token from Credential Manager.")
        sys.exit(1)

    owner = "AhmadHassan-BTed"
    repo = "KodeArrow"
    tag = "v2.5-r-edition"
    exe_path = "dist/KodeArrow.exe"

    if not os.path.exists(exe_path):
        print(f"Executable not found at {exe_path}!")
        sys.exit(1)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Get Release by Tag
    release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    print(f"Fetching release for tag {tag}...")
    r = requests.get(release_url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to find release for tag {tag}: status {r.status_code}, response: {r.text}")
        sys.exit(1)

    release_data = r.json()
    release_id = release_data["id"]
    assets = release_data.get("assets", [])

    # 2. Check and Delete existing KodeArrow.exe asset
    for asset in assets:
        if asset["name"] == "KodeArrow.exe":
            asset_id = asset["id"]
            delete_url = f"https://api.github.com/repos/{owner}/{repo}/releases/assets/{asset_id}"
            print(f"Deleting existing asset KodeArrow.exe (ID: {asset_id})...")
            dr = requests.delete(delete_url, headers=headers)
            if dr.status_code in (200, 204):
                print("Successfully deleted old asset.")
            else:
                print(f"Failed to delete old asset: status {dr.status_code}, response: {dr.text}")
                sys.exit(1)
            break

    # 3. Upload New Asset
    upload_url_template = release_data["upload_url"] # e.g. "https://uploads.github.com/.../assets{?name,label}"
    base_upload_url = upload_url_template.split("{")[0]
    upload_url = f"{base_upload_url}?name=KodeArrow.exe"

    print("Reading new binary data...")
    with open(exe_path, "rb") as f:
        binary_data = f.read()

    upload_headers = headers.copy()
    upload_headers["Content-Type"] = "application/octet-stream"
    upload_headers["Content-Length"] = str(len(binary_data))

    print(f"Uploading new KodeArrow.exe ({len(binary_data)} bytes) to release {tag}...")
    ur = requests.post(upload_url, headers=upload_headers, data=binary_data)
    if ur.status_code == 201:
        print("Success! New KodeArrow.exe asset uploaded successfully to GitHub Release v2.5!")
    else:
        print(f"Failed to upload asset: status {ur.status_code}, response: {ur.text}")
        sys.exit(1)

if __name__ == "__main__":
    update_release_asset()
