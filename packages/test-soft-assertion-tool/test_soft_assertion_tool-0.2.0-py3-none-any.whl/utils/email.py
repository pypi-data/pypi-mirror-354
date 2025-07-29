import re
import time

import requests

from config.config import c_config


class EmailUtils:
    def __init__(self):
        pass

    def get_email_list(self,inbox_name,max_retries = 6,  retry_interval = 5):
        """
            get email list（have retry）
            Args:
                inbox_name: inbox name
                max_retries: maxium retry times
                retry_interval: interval for retry（s）
            Returns:
                when success, it will return email data dict，if fail, it will return null
            """
        url = f"{c_config.mailinator_base_url}/domains/{c_config.mailinator_domain}/inboxes/{inbox_name}"
        headers = {
            "Authorization": f"Bearer {c_config.mailinator_token}",
            "Content-Type": "application/json"
        }
        json_data = ""
        for i in range(max_retries):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data["msgs"]:
                    if json_data["msgs"][0]["seconds_ago"] < 15:
                        print("get the latest email")
                        break
                    else:
                        time.sleep(retry_interval)
        return json_data

    def get_email_id(self, json_data, subject: str):
        """
           get email id from with specific subject from email list
           Args:
             json_data: the dict include email list
             subject: the email subject to search for
          Raises:
             return empty if json_data wrong
        """
        email_id: str  # New authentication request
        if json_data["msgs"]:
            for email in json_data["msgs"]:
                print("email subject:", email["subject"])
                if email["subject"] == subject:
                    print("email id:", email["id"])
                    email_id = email["id"]
                    break
        return email_id

    def get_email_details(self, inbox_id):
        """
        get email details info from specific email
        Raises:
           return email datails info
        """
        url = f"{c_config.mailinator_base_url}/domains/{c_config.mailinator_domain}/messages/{inbox_id}"
        headers = {
            "Authorization": f"Bearer {c_config.mailinator_token}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_content_from_email_withpattern(self, json_data, pattern):
        """
          get specific pattern from email
          Raises:
              return email content if success, otherwise return None
        """
        for part in json_data.get("parts", []):
            body = part.get("body", "")
            match = re.search(pattern, body)
            if match:
                return match.group(1).strip()
        return None


mailinator_email = EmailUtils()
