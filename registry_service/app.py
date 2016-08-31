import axial.service

from axial.service.middleware.processors import (
    ProtobufProcessor, JsonProcessor,
    )
from axial.service.middleware import (
    EncoderDecoder, SqlalchemyConnector
    )

from .db.session import Postgres
from . import routes


class Application(axial.service.Application):

    @property
    def middleware(self):
        return [
            EncoderDecoder(processors=[
                ProtobufProcessor(self.name),
                JsonProcessor(),
                ]),
            SqlalchemyConnector(Postgres),
            ]

    @property
    def routes(self):
        return [
            routes.StatusCheck(),
        ]
