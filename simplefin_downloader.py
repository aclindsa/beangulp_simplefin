#!/usr/bin/env python

import json
import requests
from datetime import timedelta, datetime
from math import ceil, floor


class SimpleFinDownloader:
    def __init__(self,
                 name,
                 simplefin_acctid,
                 simplefin_username,
                 simplefin_password,
                 simplefin_url='https://beta-bridge.simplefin.org/simplefin',
                 download_days=timedelta(days=30)):
        self.account_name = name
        self.simplefin_acctid = simplefin_acctid
        self.simplefin_username = simplefin_username
        self.simplefin_password = simplefin_password
        self.simplefin_url = simplefin_url
        self.download_days = download_days

    def info(self):
        try:
            response = requests.get(f'{self.simplefin_url}/info')
            response.raise_for_status()
            return response.json()['versions']
        except requests.exceptions.RequestException as e:
            print("An error occurred making the SimpleFin info request:", e)
            return []

    def download(self, filename):
        request_url = f'{self.simplefin_url}/accounts'
        end_time = datetime.now() + timedelta(days=1)
        start_time = end_time - self.download_days
        params = {
            'account': self.simplefin_acctid,
            'start-date': floor(start_time.timestamp()),
            'end-date': ceil(end_time.timestamp())
        }
        info = self.info()
        data = {}
        try:
            response = requests.get(request_url,
                                    params=params,
                                    auth=(self.simplefin_username,
                                          self.simplefin_password))
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred making the SimpleFin accounts request:", e)
            return False

        def output_json(data):
            with open(filename, 'w') as out_file:
                j = {
                    'simplefin_versions': info,
                    'simplefin_request_url': request_url,
                    'simplefin_request_params': params,
                    'response': data
                }
                json.dump(j, out_file, indent=2)

        if 'accounts' not in data:
            # write out for debugging purposes
            output_json(data)
            return False

        for account in data['accounts']:
            if account['id'] == self.simplefin_acctid:
                output_json(account)
                return True

        # couldn't find account, write full output for debugging purposes
        output_json(data)
        return False

    def filename_suffix(self):
        return "simplefin.json"

    def name(self):
        return self.account_name
