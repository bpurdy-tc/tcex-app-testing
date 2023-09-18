"""TcEx Framework Module"""
import json
# standard library
import logging
from functools import partial
from pathlib import Path

import requests
# third-party
from requests import PreparedRequest

# first-party
import responses
from responses import matchers

# get logger
_logger = logging.getLogger(__name__.split('.', maxsplit=1)[0])

base_path = Path(
    '/Users/bpurdy-ad/projects/intergrations/playbooks/attributes/tcpb_-_threatconnect_attributes/'
)


def response_callback(request, output_file: str):
    responses.stop()
    response = requests.request(request.method, request.url, headers=request.headers, data=request.body)
    responses.start()

    with open(base_path / Path(output_file), 'w') as f:
        f.write(json.dumps(response.json(), indent=4))

    return response.status_code, response.headers, response.text


class StagerRequest:
    """Stages the Redis Data"""

    def __init__(self):
        """Initialize class properties."""
        self.log = _logger

    def stage(self, request_data) -> dict:
        """Stage redis data from dict"""
        for key, requests in request_data.items():
            for request in requests:
                kwargs = {
                    'url': request.get('url'),
                    'status': request.get('status', 200),
                    'match': [],
                }
                if request.get('params'):
                    kwargs['match'] = [matchers.query_param_matcher(request.get('params', {}))]
                path_ = self.staged_responses.get(request.get('output_file'))
                if path_ and path_.exists():
                    with open(path_, 'r') as f:
                        data = f.read()
                    kwargs['json'] = json.loads(data)
                else:
                    responses.add_callback(
                        key.upper(), url=request.get('url'),callback=partial(response_callback, output_file=request.get('output_file'))
                    )

                resp = getattr(responses, key.lower())(**kwargs)

    @property
    def staged_responses(self):
        """Get a list of all of the files already staged."""
        temp = ['groups_associations.json', 'groups_attr.json', 'indicators.json']
        return {file: base_path / Path(file) for file in temp}
        # return os.listdir('/path/to/folder/to/list')
