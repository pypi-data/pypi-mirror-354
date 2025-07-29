"""Main file for the client."""

import json
import os
import requests
import sys

CLIENT_KB_DIR = os.path.join(os.getcwd(), ".luca")
LOCAL_KB_PATH = os.path.join(CLIENT_KB_DIR, "kb.txt")
CLIENT_ARTIFACTS_DIR = os.path.join(CLIENT_KB_DIR, "artifacts")

# Gateway configuration
GATEWAY_URL = os.getenv("LUCA_GATEWAY_URL", "https://www.myluca.ai/api/gateway")
API_KEY = os.getenv("LUCA_API_KEY")

def ensure_dirs():
    """Ensure the client's directories exist."""
    for directory in [CLIENT_KB_DIR, CLIENT_ARTIFACTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def ensure_kb_dir():
    """Ensure the client's KB directory exists."""
    if not os.path.exists(CLIENT_KB_DIR):
        os.makedirs(CLIENT_KB_DIR)

def get_headers():
    """Get headers for authenticated requests."""
    if not API_KEY:
        print("❌ Error: LUCA_API_KEY environment variable not set.")
        print("Please set your API key:")
        print("  export LUCA_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://www.myluca.ai/dashboard")
        sys.exit(1)
    
    return {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Luca-CLI/1.0"
    }

def make_authenticated_request(endpoint, method="GET", json_data=None):
    """Make an authenticated request to the gateway."""
    headers = get_headers()
    url = f"{GATEWAY_URL}/{endpoint.lstrip('/')}"
    
    try:
        response = requests.request(method, url, headers=headers, json=json_data, timeout=60)
        
        # Handle authentication errors
        if response.status_code == 401:
            error_data = response.json() if response.content else {}
            print("❌ Authentication Error:")
            print(f"   {error_data.get('message', 'Invalid API key')}")
            print("\nPlease check your API key:")
            print("  1. Get a new API key from: https://www.myluca.ai/dashboard")
            print("  2. Set it as: export LUCA_API_KEY=your_api_key_here")
            sys.exit(1)
        
        # Handle service unavailable errors
        elif response.status_code == 503:
            error_data = response.json() if response.content else {}
            print("❌ Service Unavailable:")
            print(f"   {error_data.get('message', 'Your agent is not ready')}")
            if 'vmStatus' in error_data:
                print(f"   VM Status: {error_data['vmStatus']}")
            print("\nPlease wait a few minutes and try again.")
            sys.exit(1)
        
        # Handle other client errors
        elif response.status_code >= 400:
            try:
                error_data = response.json()
                print(f"❌ Error ({response.status_code}): {error_data.get('message', 'Request failed')}")
            except:
                print(f"❌ Error ({response.status_code}): {response.text or 'Request failed'}")
            sys.exit(1)
        
        response.raise_for_status()
        return response
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout. Your agent may be slow to respond.")
        print("Please try again in a moment.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Please check your internet connection.")
        print("If the problem persists, visit: https://www.myluca.ai/dashboard")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)

def sync_kb():
    """Sync the knowledge base from the server."""
    ensure_kb_dir()
    response = make_authenticated_request("kb")
    response_data = json.loads(response.content)
    with open(LOCAL_KB_PATH, "w") as f:
        f.write(response_data["text"])

def update_kb(content: str):
    """Update the knowledge base."""
    ensure_kb_dir()
    kb_text = json.loads(content)["text"]
    with open(LOCAL_KB_PATH, "w") as f:
        f.write(kb_text)

def download_artifact(filename: str) -> bool:
    """Download a specific artifact from the server."""
    try:
        response = make_authenticated_request(f"artifacts/{filename}")
        
        local_path = os.path.join(CLIENT_ARTIFACTS_DIR, filename)
        with open(local_path, "wb") as f:
            f.write(response.content)
        return True
    except SystemExit:
        # Re-raise authentication/service errors
        raise
    except Exception as e:
        print(f"Error downloading artifact {filename}: {e}")
        return False

def download_artifacts(artifacts: list) -> list:
    """Download multiple artifacts and return successful downloads."""
    ensure_dirs()
    downloaded = []
    
    for artifact in artifacts:
        filename = artifact["filename"]
        size = artifact["size"]
        
        print(f"Downloading {filename} ({size} bytes)...")
        try:
            if download_artifact(filename):
                downloaded.append(filename)
                local_path = os.path.join(CLIENT_ARTIFACTS_DIR, filename)
                print(f"✓ Saved to {local_path}")
            else:
                print(f"✗ Failed to download {filename}")
        except SystemExit:
            # Don't continue downloading if there's an auth error
            break
    
    return downloaded

def init():
    """Initialize the client and the server."""
    print("🚀 Initializing Luca...")
    request_params = {
        "WANDB_API_KEY": os.getenv("WANDB_API_KEY"),
        "WANDB_ENTITY": os.getenv("WANDB_ENTITY")
    }
    
    response = make_authenticated_request("init", "POST", request_params)
    update_kb(response.content)
    print("✅ Luca initialized successfully!")

def feedback(text: str):
    """Send feedback to the server."""
    response = make_authenticated_request("feedback", "POST", {"text": text})
    response_data = json.loads(response.content)
    print(response_data["text"])

def list_artifacts():
    """List all available artifacts on the server."""
    response = make_authenticated_request("artifacts")
    response_data = json.loads(response.content)
    artifacts = response_data.get("artifacts", [])
    
    if not artifacts:
        print("No artifacts available.")
        return
    
    print("Available artifacts:")
    for artifact in artifacts:
        filename = artifact["filename"]
        size = artifact["size"]
        print(f"  📄 {filename} ({size} bytes)")

def check_auth():
    """Check API key authentication and show status."""
    print("🔍 Checking authentication...")
    
    response = make_authenticated_request("auth", "GET")
    auth_data = json.loads(response.content)
    
    print("✅ Authentication successful!")
    print(f"   User: {auth_data['user']['email']}")
    print(f"   API Key: {auth_data['apiKey']['name'] or 'Unnamed'}")
    print(f"   Created: {auth_data['apiKey']['createdAt'][:10]}")
    
    if auth_data['vm']:
        vm = auth_data['vm']
        status_emoji = "🟢" if vm['ready'] else "🟡" if vm['status'] == 'running' else "🔴"
        print(f"   VM Status: {status_emoji} {vm['status']}")
        print(f"   VM Ready: {'Yes' if vm['ready'] else 'No'}")
        
        if not vm['ready']:
            print("\n⚠️  Your agent is not ready yet. Please wait a few minutes.")
    else:
        print("   VM Status: 🔴 No VM found")
        print("\n⚠️  No VM instance found. Please contact support.")

def setup():
    """Interactive setup for API key configuration."""
    print("🔧 Luca CLI Setup")
    print("================")
    print()
    print("To use Luca CLI, you need an API key from your dashboard.")
    print("1. Visit: https://www.myluca.ai/dashboard")
    print("2. Create an API key")
    print("3. Copy the API key")
    print()
    
    api_key = input("Enter your API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    if not api_key.startswith("luca_"):
        print("❌ Invalid API key format. API keys should start with 'luca_'")
        return
    
    print()
    print("✅ API key received!")
    print()
    print("Add this to your shell configuration (~/.bashrc, ~/.zshrc, etc.):")
    print()
    print(f"export LUCA_API_KEY='{api_key}'")
    print()
    print("Then restart your terminal or run:")
    print(f"export LUCA_API_KEY='{api_key}'")
    print()
    print("Test your setup with: luca auth")

def main(argv):
    """Main function."""
    if len(argv) == 1:
        print("🤖 Luca CLI - AI Copilot for Research")
        print("=====================================")
        print()
        print("Usage: luca <command> or luca <prompt>")
        print()
        print("Commands:")
        print("  setup     - Interactive API key setup")
        print("  auth      - Check authentication status")
        print("  init      - Initialize the client and agent")
        print("  sync      - Sync knowledge base from agent")
        print("  artifacts - List all available artifacts")
        print("  feedback  - Send feedback about your experience")
        print()
        print("Examples:")
        print("  luca setup")
        print("  luca auth")
        print("  luca init")
        print("  luca 'Research papers on reinforcement learning'")
        print("  luca 'Analyze the experiment data in my directory'")
        print()
        print("Configuration:")
        print("  LUCA_API_KEY      - Your API key (required)")
        print("  LUCA_GATEWAY_URL  - Gateway URL (optional)")
        print()
        print("Get your API key: https://www.myluca.ai/dashboard")
        return
    
    command = argv[1]
    
    if command == "setup":
        setup()
    elif command == "auth":
        check_auth()
    elif command == "init":
        init()
    elif command == "sync":
        sync_kb()
        print("✅ Knowledge base synced successfully!")
    elif command == "artifacts":
        list_artifacts()
    elif command == "feedback":
        if len(argv) < 3:
            print("❌ Usage: luca feedback <message>")
            print("Example: luca feedback 'Great tool, works perfectly!'")
            return
        feedback(argv[2])
    else:
        # User query
        prompt = argv[1]
        print(f"🤔 Processing: {prompt}")
        print()
        
        response = make_authenticated_request("query", "POST", {"prompt": prompt})
        response_data = json.loads(response.content)
        print(response_data["text"])
        
        # Handle artifacts
        artifacts = response_data.get("artifacts", [])
        if artifacts:
            print(f"\n📁 Found {len(artifacts)} new artifact(s)")
            downloaded = download_artifacts(artifacts)
            if downloaded:
                print(f"✅ Downloaded {len(downloaded)} artifact(s) successfully")
        
        # Check if KB was updated and sync if needed
        if response_data.get("kb_updated", False):
            print("\n🔄 Syncing knowledge base...")
            sync_kb()
            print("✅ Knowledge base synced successfully!")

def entrypoint():
    """Entry point for the CLI tool."""
    main(sys.argv)

if __name__ == "__main__":
    entrypoint()
