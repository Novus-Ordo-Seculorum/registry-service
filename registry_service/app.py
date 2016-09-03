import axial.service

from axial.service.middleware import EncoderDecoder
from axial.service.middleware.processors import (
    ProtobufProcessor, JsonProcessor,
    )

from . import routes


class Application(axial.service.Application):

    @property
    def middleware(self):
        return [
            EncoderDecoder(processors=[
                ProtobufProcessor(self.name),
                JsonProcessor(),
                ]),
            ]

    @property
    def routes(self):
        return [
            routes.ServicesRoute(),
            routes.ServiceNamesRoute(),
            routes.ServiceRoute(),
        ]
