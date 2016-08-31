import pytz

from datetime import datetime

from axial.service.route import Route, handler_config

from .schemas import StatusCheckSchema


class StatusCheck(Route):
    path = '/status'

    @handler_config(
        response=StatusCheckSchema,
        )
    def on_get_v1(self, request, response):
        return {
            'name': 'registry',
            'datetime': str(datetime.now(pytz.utc)),
            }
