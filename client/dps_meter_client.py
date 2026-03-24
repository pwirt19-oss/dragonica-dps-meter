import json

class DPSMeterClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_data(self):
        response = self._send_request()
        return json.loads(response)

    def _send_request(self):
        # This function would handle the actual sending of a request to the server.
        # Simulated response for this example:
        return '{"data": "some_data"}'

    def format_data(self, data):
        return f'Formatted Data: {data}'