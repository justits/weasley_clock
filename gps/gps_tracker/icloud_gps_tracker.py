from pyicloud import PyiCloudService
import sys
import json
import time
import datetime

from gps.global_const import LOCAL_TZ, MINUTE
from gps.gps_tracker.gps_tracker import GPSTracker
from gps.location import GPSLocation, Location


def get_time(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp) / 1_000, LOCAL_TZ)


def get_gps_location(loc):
    if loc is None:
        return None
    location = Location(loc['latitude'], loc['longitude'])
    return GPSLocation(location, get_time(loc['timestamp']))


class iCloudGPSTracker(PyiCloudService, GPSTracker):
    def __init__(self, apple_id, password):
        super().__init__(apple_id, password)
        self._create_connection()

    def _create_connection(self):
        if self.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = self.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

            if not self.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = self.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif self.requires_2sa:
            import click
            print("Two-step authentication required. Your trusted devices are:")

            devices = self.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s" % (i, device.get('deviceName',
                                                "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not self.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not self.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)

    def select_query(self, query_method):
        # _ = {'family_locations': self._family_locations}[query_method]
        # time.sleep(MINUTE)
        return {'family_locations': self._family_locations}[query_method]

    @property
    def _family_locations(self):
        service_root = self._get_webservice_url("findme")
        fmf_endpoint = f"{service_root}/fmipservice/client/fmfWeb/initClient"
        data = json.dumps(
            {
                "clientContext": {
                    "appVersion": "1.0",
                    "contextApp": "com.icloud.web.fmf",
                    "mapkitAvailable": True,
                    "productType": "fmfWeb",
                    "tileServer": "Apple",
                    "userInactivityTimeInMS": 537,
                    "windowInFocus": False,
                    "windowVisible": True,
                },
                "dataContext": None,
                "serverContext": None,
            }
        )

        req = self.session.post(fmf_endpoint, data=data, params=self.params)
        response = req.json()
        return {user['id']: get_gps_location(user['location']) for user in response['locations']}
