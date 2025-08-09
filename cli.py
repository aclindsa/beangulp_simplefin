#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
import json
from math import ceil, floor
import os
import requests

from simplefin_downloader import SimpleFinDownloader


def list_accounts(args):
    access_url = args.access_url

    scheme, rest = access_url.split('//', 1)
    auth, rest = rest.split('@', 1)
    request_url = scheme + '//' + rest + '/accounts'
    simplefin_username, simplefin_password = auth.split(':', 1)

    response = requests.get(request_url,
                            auth=(simplefin_username,
                                  simplefin_password))
    response.raise_for_status()
    data = response.json()

    print(json.dumps(data, indent=2))


def list_account_transactions(args):
    access_url = args.access_url
    account_id = args.account_id

    scheme, rest = access_url.split('//', 1)
    auth, rest = rest.split('@', 1)
    request_url = scheme + '//' + rest + '/accounts'
    simplefin_username, simplefin_password = auth.split(':', 1)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=args.days)
    params = {
        'account': account_id,
        'start-date': floor(start_time.timestamp()),
        'end-date': ceil(end_time.timestamp())
    }
    try:
        response = requests.get(request_url,
                                params=params,
                                auth=(simplefin_username,
                                      simplefin_password))
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
    except requests.exceptions.RequestException as e:
        print("An error occurred making the SimpleFin accounts request:", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access-url', default=os.environ.get('ACCESS_URL'),
                        required=True)
    subparsers = parser.add_subparsers(help='subcommand help')

    list_accts = subparsers.add_parser("list-accounts")
    list_accts.set_defaults(func=list_accounts)

    list_acct_txns = subparsers.add_parser("list-account-transactions")
    list_acct_txns.add_argument('--account-id', required=True)
    list_acct_txns.add_argument('--days', default=7, type=int)
    list_acct_txns.set_defaults(func=list_account_transactions)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
