# GistLick
**Python Library for Interacting with GitHub Gist API for License Management**

GistLick is a powerful and flexible Python library designed to simplify interactions with GitHub's Gist API. It provides a straightforward way to manage your Gists programmatically, including creating, retrieving, updating, and deleting Gists. Furthermore, GistLick extends this functionality to manage custom license keys directly within your Gists, offering tools for license creation, verification, and expiration tracking.

## Features

-   **Gist Management:**
    -   List all authenticated user's Gists.
    -   Retrieve details and content of a specific Gist.
    -   Create new Gists (with optional description and public/private status).
    -   Update existing Gists (change name, public status, content, description).
    -   Delete Gists by ID.
-   **License Key Management:**
    -   Create unique license keys within a specified Gist, including user, plan, machine ID, and expiration date.
    -   Delete specific license keys from a Gist.
    -   Delete all expired license keys from a Gist.
    -   Client-side license verification with machine ID generation.
-   **Authentication:** Utilizes GitHub Personal Access Tokens for secure API access.
-   **Customization:** Supports customization of User-Agent strings for API requests.

## Requirements
| Library       | Installation                  |
|---------------|-------------------------------|
| Requests      | `pip install requests`        |

## Installation
Install with pip
```bash
pip install gistlick
```

## Quick Start
Here's a quick example to get you started with GistLick:
```python
from gistlick import GistLick, GistLickey

# --- Initialize GistLick ---
# Replace 'YOUR_GITHUB_TOKEN' with your actual GitHub Personal Access Token.
# Ensure your token has the 'gist' scope enabled.
gist_lick = GistLick(token='YOUR_GITHUB_TOKEN')

# Verify authentication
if gist_lick.user:
    print(f"Authenticated as: {gist_lick.user.get('user')} (ID: {gist_lick.user.get('id')})")
else:
    print("Authentication failed. Please check your GitHub token.")
    exit()

# --- Gist Management: Create a new Gist ---
try:
    new_gist = gist_lick.create_gist(
        name='my_licenses.json',
        public=False,
        description='A private Gist to store license keys'
    )
    print(f"\nCreated Gist: '{new_gist.get('name')}' (ID: {new_gist.get('id')})")
    print(f"Raw URL: {new_gist.get('url')}")
    my_gist_id = new_gist.get('id')
except Exception as e:
    print(f"\nError creating Gist: {e}")
    my_gist_id = None # Ensure my_gist_id is set to None on failure

if my_gist_id:
    # --- License Management: Create a new License ---
    # Using GistLickey to get a sample machine ID for demonstration
    gist_lickey_client = GistLickey(gist_url=f"[https://gist.githubusercontent.com/](https://gist.githubusercontent.com/){gist_lick.user.get('user')}/{my_gist_id}/raw")
    
    try:
        new_license = gist_lick.create_license(
            id=my_gist_id,
            user='client_app_user_1',
            plan='premium',
            machine=gist_lickey_client.get_machine_id(), # Generate machine ID
            expired=30 # Expires in 30 days
        )
        print(f"\nCreated License: {new_license.get('license')}")
        print(f"For user: {new_license.get('user')}, expires: {new_license.get('expired')}")
    except Exception as e:
        print(f"\nError creating License: {e}")

    # --- License Management: Verify a License ---
    if new_license:
        try:
            # Note: For verification, the GistLickey needs the raw Gist URL
            # The URL points to the raw content, not the GitHub API itself.
            verify_result = gist_lickey_client.verify_license(new_license.get('license'))
            print(f"\nLicense Verification: {verify_result.get('message')}")
            print(f"Status: {'Valid' if verify_result.get('status') else 'Expired/Invalid'}")
        except Exception as e:
            print(f"\nError verifying License: {e}")

    # --- Clean up: Delete the created Gist (Optional) ---
    try:
        if input("\nDo you want to delete the created Gist? (yes/no): ").lower() == 'yes':
            delete_message = gist_lick.delete_gist(my_gist_id)
            print(f"Gist deleted: {delete_message.get('message')}")
    except Exception as e:
        print(f"\nError deleting Gist: {e}")
```
