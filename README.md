Checks your current public IP and loops through any A-records in the specified Cloudflare zone,
changing them if different.
Note: It will change any A-record found in Cloudflare

Supply the following env vars:
```bash
CF_API_TOKEN
CF_ZONE_ID
```
