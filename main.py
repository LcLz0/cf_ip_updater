#!/usr/bin/env
import requests
import dotenv
import os

def _get_ip():
    ip_api_url = "https://api.ipify.org"
    r = requests.get(ip_api_url)
    return r.text


def _get_current_zone(api_token, zone_id):
    cf_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    r = requests.get(cf_url, headers=headers)
    r.raise_for_status()
    return r.json()


def _patch_record(api_token, zone_id, record, current_ip):
    cf_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    data = {
        "name": record["name"],
        "content": current_ip,
        "type": record["type"],
        "proxied": record["proxied"],
    }
    r = requests.put(cf_url, headers=headers, json=data)
    r.raise_for_status()


def main():
    dotenv.load_dotenv()
    api_token = os.getenv("CF_API_TOKEN")
    zone_id = os.getenv("CF_ZONE_ID")

    current_ip = _get_ip()
    current_records = _get_current_zone(api_token, zone_id)
    # Only interested in A-records
    current_records = [ x for x in current_records["result"] if x["type"] == "A" ]

    for record in current_records:
        if record["content"] != current_ip:
            _patch_record(api_token, zone_id, record, current_ip)


if __name__ == "__main__":
    main()
