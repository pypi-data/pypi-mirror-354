import os
import json
import time
import string
import random
import hashlib
import requests

from typing import Optional, Union, List, Dict, Any
from datetime import datetime, timedelta

class GistLick:

    api = 'https://api.github.com'

    def __init__(self, token: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible; GistLickAPI/1.0; +https://github.com/your-repo)'
        })
        self._user_data = None

    def _get_user_info(self) -> Dict[str, Any]:
        """Fetches and caches authenticated user info."""
        if self._user_data:
            return self._user_data

        resp = self.session.get(self.api + '/user')
        resp.raise_for_status()
        user = resp.json()
        self._user_data = {
            'id': user.get('id'),
            'user': user.get('login'),
            'name': user.get('name'),
            'avatar': user.get('avatar_url'),
            'created': user.get('created_at'),
            'updated': user.get('updated_at'),
            'followers': user.get('followers'),
            'following': user.get('following')
        }
        return self._user_data

    @property
    def user(self) -> Dict[str, Any]:
        """Returns authenticated user info, fetching if not cached."""
        return self._get_user_info()

    def _get_gist_file_name(self, resp: Dict[str, Any]) -> Optional[str]:
        """Helper to get the first file name from a Gist response."""
        files = resp.get('files')
        if files and isinstance(files, dict) and len(files) > 0:
            return list(files.keys())[0]
        return None

    def get_gist(self) -> List[Dict[str, Any]]:
        """Retrieves a list of Gists for the authenticated user."""
        gist_list = []
        resp = self.session.get(self.api + '/gists')
        resp.raise_for_status()
        for item in resp.json():
            file_name = self._get_gist_file_name(item)
            if file_name:
                gist_list.append({
                    'id': item.get('id'),
                    'url': f'https://gist.githubusercontent.com/{item.get("owner", {}).get("login")}/{item.get("id")}/raw',
                    'name': file_name,
                    'public': item.get('public'),
                    'created': item.get('created_at'),
                    'updated': item.get('updated_at'),
                    'description': item.get('description')
                })
        return gist_list
    
    def get_gist_data(self, gist_id: str) -> Dict[str, Any]:
        """Retrieves data for a single Gist by ID."""
        gists = self.get_gist()
        gist = next((item for item in gists if item.get('id') == gist_id), None)
        if not gist:
            resp = self.session.get(f"{self.api}/gists/{gist_id}")
            resp.raise_for_status()
            item = resp.json()
            file_name = self._get_gist_file_name(item)
            if file_name:
                return {
                    'id': item.get('id'),
                    'url': f'https://gist.githubusercontent.com/{item.get("owner", {}).get("login")}/{item.get("id")}/raw',
                    'name': file_name,
                    'public': item.get('public'),
                    'created': item.get('created_at'),
                    'updated': item.get('updated_at'),
                    'description': item.get('description')
                }
            raise ValueError(f"Gist with ID '{gist_id}' not found or malformed.")
        return gist
    
    def get_gist_content(self, gist_id: str, file_name: Optional[str] = None) -> Any:
        """Retrieves the content of a specific file within a Gist."""
        resp = self.session.get(f"{self.api}/gists/{gist_id}")
        resp.raise_for_status()
        gist_data = resp.json()
        
        actual_file_name = file_name if file_name is not None else self._get_gist_file_name(gist_data)
        
        if not actual_file_name or actual_file_name not in gist_data.get('files', {}):
            raise ValueError(f"File '{file_name or 'default'}' not found in Gist '{gist_id}'.")
        
        content = gist_data['files'][actual_file_name]['content']
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content
    
    def create_gist(self, name: str, public: Optional[bool] = False, description: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new Gist."""
        payload = {
            'description': description if isinstance(description, str) else '',
            'public': public if isinstance(public, bool) else False,
            'files': {name: {'content': json.dumps([])}}
        }
        resp = self.session.post(self.api + '/gists', json=payload)
        resp.raise_for_status()
        new_gist = resp.json()
        file_name = self._get_gist_file_name(new_gist)
        if not file_name:
            raise ValueError("Created Gist has no files.")
        
        return {
            'id': new_gist.get('id'),
            'url': f'https://gist.githubusercontent.com/{new_gist.get("owner", {}).get("login")}/{new_gist.get("id")}/raw',
            'name': file_name,
            'public': new_gist.get('public'),
            'created': new_gist.get('created_at'),
            'updated': new_gist.get('updated_at'),
            'description': new_gist.get('description')
        }
    
    def delete_gist(self, gist_id: str) -> Dict[str, str]:
        """Deletes a Gist by ID."""
        resp = self.session.delete(f"{self.api}/gists/{gist_id}")
        resp.raise_for_status()
        return {'message': f'Gist with ID "{gist_id}" has been deleted.'}
    
    def update_gist(self, gist_id: str, name: Optional[str] = None, public: Optional[bool] = None, content: Optional[Any] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Updates an existing Gist."""
        current_gist_data = self.get_gist_data(gist_id)
        current_file_name = current_gist_data['name']
        
        files_payload = {}
        file_content_to_send = content
        if file_content_to_send is None:
            file_content_to_send = self.get_gist_content(gist_id, current_file_name)
        
        if isinstance(file_content_to_send, (list, dict)):
            file_content_to_send = json.dumps(file_content_to_send)
        elif not isinstance(file_content_to_send, str):
            file_content_to_send = str(file_content_to_send)

        files_payload[current_file_name] = {
            'filename': name if name is not None else current_file_name,
            'content': file_content_to_send
        }

        payload = {
            'description': description if description is not None else current_gist_data['description'],
            'public': public if public is not None else current_gist_data['public'],
            'files': files_payload
        }

        resp = self.session.patch(f"{self.api}/gists/{gist_id}", json=payload)
        resp.raise_for_status()
        updated_gist = resp.json()
        file_name = self._get_gist_file_name(updated_gist)
        if not file_name:
            raise ValueError("Updated Gist has no files.")

        return {
            'id': updated_gist.get('id'),
            'url': f'https://gist.githubusercontent.com/{updated_gist.get("owner", {}).get("login")}/{updated_gist.get("id")}/raw',
            'name': file_name,
            'public': updated_gist.get('public'),
            'created': updated_gist.get('created_at'),
            'updated': updated_gist.get('updated_at'),
            'description': updated_gist.get('description')
        }
    
    def create_license(self, gist_id: str, user: str, plan: str, machine: str, expired_days: int) -> Dict[str, Any]:
        """Creates a new license entry in a Gist."""
        gist_data = self.get_gist_data(gist_id)
        content = self.get_gist_content(gist_id, gist_data['name'])

        if not isinstance(content, list):
            content = []
        
        valid_plans = ['free', 'trial', 'premium']
        chosen_plan = plan if plan in valid_plans else valid_plans[0]

        created_at = datetime.now()
        expired_at = created_at + timedelta(days=expired_days)
        
        license_key = None
        attempts = 0
        while attempts < 100: 
            temp_license_key = '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4))
            is_duplicate = any(isinstance(item, dict) and item.get('license') == temp_license_key for item in content)
            if not is_duplicate:
                license_key = temp_license_key
                break
            attempts += 1
        
        if not license_key:
            raise Exception("Failed to generate a unique license key after multiple attempts.")

        new_license = {
            'user': user,
            'plan': chosen_plan,
            'license': license_key,
            'machine': machine,
            'created': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'expired': expired_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        content.append(new_license)
        self.update_gist(gist_id=gist_id, content=content)
        return new_license
    
    def update_license(self, gist_id: str, license_key_to_update: str, user: str, plan: str, machine: str, created: str, expired: str) -> Dict[str, Any]:
        """Updates an existing license entry in a Gist."""
        gist_data = self.get_gist_data(gist_id)
        current_content = self.get_gist_content(gist_id, gist_data['name'])

        if not isinstance(current_content, list):
            raise ValueError("Gist content is not a list. Cannot update license.")

        updated_license = None
        found = False
        for i, item in enumerate(current_content):
            if isinstance(item, dict) and item.get('license') == license_key_to_update:
                current_content[i] = {
                    'user': user,
                    'plan': plan,
                    'license': license_key_to_update,
                    'machine': machine,
                    'created': created,
                    'expired': expired
                }
                updated_license = current_content[i]
                found = True
                break
        
        if not found:
            raise ValueError(f"License with key '{license_key_to_update}' not found in Gist '{gist_id}'.")

        self.update_gist(gist_id=gist_id, content=current_content)
        return updated_license

    def delete_license(self, gist_id: str, license_key: str) -> Dict[str, str]:
        """Deletes a license entry from a Gist."""
        gist_data = self.get_gist_data(gist_id)
        current_content = self.get_gist_content(gist_id, gist_data['name'])

        if not isinstance(current_content, list):
            raise ValueError("Gist content is not a list. Cannot delete license.")

        initial_len = len(current_content)
        updated_content = [item for item in current_content if isinstance(item, dict) and item.get('license') != license_key]
        
        if len(updated_content) == initial_len:
            raise ValueError(f"License with key '{license_key}' not found in Gist '{gist_id}'.")

        self.update_gist(gist_id=gist_id, content=updated_content)
        return {'message': f'License with key "{license_key}" has been deleted.'}

    def delete_expired_licenses(self, gist_id: str) -> Dict[str, Any]:
        """Deletes all expired licenses from a specific Gist."""
        gist_data = self.get_gist_data(gist_id)
        current_content = self.get_gist_content(gist_id, gist_data['name'])

        if not isinstance(current_content, list):
            raise ValueError("Gist content is not a list. Cannot delete expired licenses.")

        deleted_count = 0
        updated_licenses_list = []
        for lic in current_content:
            is_expired = False
            if isinstance(lic, dict) and 'expired' in lic:
                try:
                    expired_date = datetime.strptime(lic['expired'], '%Y-%m-%d %H:%M:%S')
                    if datetime.now() > expired_date:
                        is_expired = True
                except (ValueError, TypeError):
                    pass 

            if not is_expired:
                updated_licenses_list.append(lic)
            else:
                deleted_count += 1
        
        if deleted_count > 0:
            self.update_gist(gist_id=gist_id, content=updated_licenses_list)
        
        return {'message': f'{deleted_count} expired licenses deleted from Gist "{gist_data["name"]}".', 'deleted_count': deleted_count}


class GistLickey:
    """
    Client-side license verification.
    NOTE: Machine ID generation here might differ from Python's os.stat().st_ino
    due to OS limitations or containerization. It's recommended to test carefully.
    """
    def __init__(self, gist_url: str):
        self.gist_url = gist_url

    def get_machine_id(self) -> str:
        """
        Generates a machine ID using system information.
        This attempts to replicate the spirit of os.stat().st_ino for a unique identifier,
        but it's fundamentally different across OS and execution environments.
        For consistent machine ID, ensure target deployment environment allows access
        to these system files/info.
        """
        paths_to_check = ['/bin', '/etc', '/lib', '/sbin', '/usr', '/var']
        identifiers = []

        try:
            import stat as stat_module
            for p in paths_to_check:
                try:
                    s = os.stat(p)
                    identifiers.append(str(s.st_ino))
                except (FileNotFoundError, PermissionError):
                    pass 
        except ImportError:
            pass

        if not identifiers:
            hostname = os.uname().nodename if hasattr(os, 'uname') else os.getenv('HOSTNAME', 'unknown_host')
            identifiers.append(hostname)

            if hasattr(os, 'cpu_count') and os.cpu_count() > 0:
                identifiers.append(str(os.cpu_count()))
            
            identifiers.append(os.sys.platform)
            identifiers.append(os.name)
            identifiers.append(platform.machine())

        combined_identifier = "".join(identifiers)
        return hashlib.sha256(combined_identifier.encode()).hexdigest()

    def verify_license(self, license_key: str) -> Dict[str, Any]:
        """Verifies a license key against the Gist content."""
        try:
            resp = requests.get(self.gist_url + '?nocache=' + str(time.time()), headers={
                'Accept': 'application/json',
                'Cache-Control': 'max-age=0',
                'Pragma': 'no-cache',
                'User-Agent': 'Mozilla/5.0'
            }, allow_redirects=True)
            resp.raise_for_status()

            try:
                licenses_content = json.loads(resp.text)
            except json.JSONDecodeError:
                raise ValueError('Gist content is not valid JSON format.')

            if not isinstance(licenses_content, list):
                raise ValueError('Gist content is not an array of licenses.')

            machine_node = self.get_machine_id()
            now = datetime.now()

            for item in licenses_content:
                if isinstance(item, dict) and item.get('license') == license_key and item.get('machine') == machine_node:
                    try:
                        expired_date = datetime.strptime(item.get('expired'), '%Y-%m-%d %H:%M:%S')
                        is_valid = now < expired_date
                        return {
                            'status': is_valid,
                            'license': item,
                            'message': f'License key is valid until {item.get("expired")}.' if is_valid else f'License key has expired since {item.get("expired")}.'
                        }
                    except (ValueError, TypeError):
                        return {'status': False, 'license': item, 'message': 'Invalid expiration date format in license data.'}
            
            return {'status': False, 'license': license_key, 'message': 'License key is not registered or not for this machine.'}

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve Gist for license verification: {e}")
        except Exception as e:
            raise Exception(f"Failed to verify license: {e}")