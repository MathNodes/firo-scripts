#!/bin/env python3
import subprocess
import shlex
import requests
import json

# Edit these
API_URL = "https://api.test.me/v1/firo/getsparkwalletbalance"
EXCLUDED_ADDRESS = ""
TO_ADDRESS = ""
CLI = '/home/firo/firo-e0c4238052d1/bin/firo-cli'
CONF = '/home/firo/firo-e0c4238052d1/bin/firo.conf'
SATOSHI = 100000000

def fetch_balances():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data['result']['availableBalance']
    except Exception as e:
        print(f"Failed to fetch balances: {e}")
        return []

def build_and_run_command(amount_to_send):
    recipient = {
        TO_ADDRESS: {
            "amount": round(amount_to_send, 8),
            "subtractFee": True
        }
    }
    
    json_str = json.dumps(recipient)
    escaped_json_str = f'"{json_str}"'
    
    command = (
        f'{CLI} -conf={CONF} '
        f'spendspark '
        f'"{{\\"{TO_ADDRESS}\\":{{\\"amount\\":{amount_to_send:.8f}, \\"subtractFee\\": true}}}}"'
    )

    print("\nRunning command:")
    print(command)

    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            check=True
        )
        print("\nCommand output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("\nError running command:")
        print(e.stderr)

def main():
    print("====== Firo Auto Send ======")
    balance = fetch_balances()

    if balance == 0:
        print("No balances found.")
        return
    
    amount_to_send = balance / SATOSHI
    print(f"\nPreparing to send to {TO_ADDRESS}\nwith balance {balance} (sending {amount_to_send:.8f})")
    build_and_run_command(amount_to_send)

if __name__ == "__main__":
    main()
