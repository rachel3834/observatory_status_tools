import requests
from sys import argv
from datetime import datetime
import pytz

XXX Need to load config XXX

def concat_urls(base_url,extn_url, trailing_slash=False):
    """Function to concatenate URL components without unnecessary duplication
    of /"""

    if base_url[-1:] == '/':
        base_url = base_url[:-1]
    if extn_url[0:1] == '/':
        extn_url = extn_url[1:]

    url = base_url+'/'+extn_url

    if trailing_slash:
        if url[:-1] != '/':
            url += '/'

    return url

def set_status(payload, login):
    """
    Function to set the status of a facility.  Payload is a dictionary:
    {
    'instrument': OSS primary key of instrument (may be None),
    'telescope': OSS primary key of telescope (may be None, but instrument OR telescope must be set,
    'status': string, one of: ['Open', 'Closed-weather', 'Closed-unsafe-to-observe',
                               'Closed-daytime', 'Offline', 'Unknown'],
    'status_start': datetime of time when status comes into effect, with TZINFO set to UTC
    'status_end': datetime of time when status comes to an end, with TZINFO set to UTC, may be None
    'comment': string up to 300 characters,
    'last_updated': datetime of time of submission, with TZINFO set to UTC
    }
    """

    url = concat_urls(OSS_URL,status_endpoint, trailing_slash=True)
    response = requests.post(url, data=payload, auth=login)

    #print(response.text)

def get_args():

    allowed_states = ['Open', 'Closed-weather', 'Closed-unsafe-to-observe',
                               'Closed-daytime', 'Offline', 'Unknown']
    help = """
            Set the status of a telescope or instrument
            E.g.
            > python set_facility_status.py telescope=1 instrument=None status=Open status_start=2020-09-01 status_end=2020-09-05 comment="Offline for realuminization" user=me password=my_password

            Note:
            Telescope and instrument parameters refer to the primary keys of the facility in question in the Observatory Status System
            One or the other of these parameters must be set

            Status may be one of: """+','.join(allowed_states)+"""

            Date strings must be of the format YYYY-MM-DD

            Comment strings are optional, and should be enclosed in double quotes

            User ID and password are required
            """

    today = datetime.utcnow()
    today = today.replace(tzinfo=pytz.UTC)

    payload = {
            'telescope': None,
            'instrument': None,
            'status': None,
            'status_start': None,
            'status_end': None,
            'comment': '',
            'last_updated': today.strftime("%Y-%m-%dT%H:%M:%S")
    }
    login = [None, None]

    if len(argv) == 1:
        print(help)
        return login, payload

    else:
        for arg in argv[1:]:
            (key, value) = arg.split('=')

            if key == 'user':
                login[0] = value
            elif key == 'password':
                login[1] = value
            elif key in ['telescope', 'instrument']:
                if value:
                    payload[key] = int(value)
                else:
                    payload[key] = None
            elif key == 'status':
                if value not in allowed_states:
                    raise IOError('Facility state must be one of '+','.join(allowed_states))
                else:
                    payload[key] = value
            elif key in ['status_start', 'status_end']:
                #value = datetime.strptime(value, "%Y-%m-%d")
                #value = value.replace(tzinfo=pytz.UTC)
                payload[key] = value
            elif key == 'comment':
                if 'script' not in value:
                    payload[key] = value
                else:
                    raise IOError('Invalid comment')

        login = tuple(login)

        print(payload)
        return login, payload


if __name__ == '__main__':

    (login, payload) = get_args()
    if login[0] and login[1]:
        set_status(payload, login)
