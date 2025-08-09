#!/usr/bin/env python

import argparse
import json
import os
import requests


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access-url', default=os.environ.get('ACCESS_URL'),
                        required=True)
    subparsers = parser.add_subparsers(help='subcommand help')

    list_accts = subparsers.add_parser("list-accounts")
    list_accts.set_defaults(func=list_accounts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
