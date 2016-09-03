import pytz

from pprint import pprint
from datetime import datetime

from falcon import HTTPNotFound
from axial.service.route import Route, handler_config

from .protobuf import CodeGenerator
from .db import ServiceStorage
from .schemas import (
    SuccessSchema,
    ServiceSchema,
    ServicesSchema,
    )


class ServicesRoute(Route):
    path = '/services'

    @handler_config(
        request=ServiceSchema,
        response=SuccessSchema,
        )
    def on_post_v1(self, request, response):
        service = request.data

        schemas = {}
        for schema in service['schemas']:
            # TODO: consistently prefix both protobuf messages and schema names with service name
            schemas[schema['name']] = schema

        service['proto'] = CodeGenerator(schemas=schemas).emit()

        storage = ServiceStorage.get_instance()
        storage.save_service(service)

        return {
            'success': True
            }

    @handler_config(
        response=ServicesSchema,
        )
    def on_get_v1(self, request, response):
        storage = ServiceStorage.get_instance()
        return {
            'services': storage.get_services()
            }

class ServiceNamesRoute(Route):
    path = '/services/names'

    @handler_config()
    def on_get_v1(self, request, response):
        services_names = ServiceStorage.get_instance().get_service_names()
        return {
            'services': services_names
            }


class ServiceRoute(Route):
    path = '/services/{service_name}'

    @handler_config(
        response=ServiceSchema,
        )
    def on_get_v1(self, request, response, service_name):
        storage = ServiceStorage.get_instance()
        service = storage.get_service(service_name)
        if service is None:
            raise HTTPNotFound(
                title='Service Not Found',
                description="No service '{}'".format(service_name),
                )
        return service

    @handler_config(
        response=SuccessSchema
        )
    def on_delete_v1(self, request, response, service_name):
        storage = ServiceStorage.get_instance()
        storage.delete_service(service_name)
        return {
            'success': True
            }


if __name__ == '__main__':
    import ujson

    from pprint import pprint

    from axial.schema import Schema
    from axial.schema import fields
    from axial.service import (
        ServiceRegistry,
        AsyncHttpClient,
        AsyncServiceClient,
        )

    class CompanySchema(Schema):
        name = fields.Str(1, required=True)
        description = fields.Str(2, required=False)

    payload = {
        "name": "company",
        "routes": [
            {
                "name": "companies",
                "path": "/companies",
                "handlers": [
                    {
                        "method": "POST",
                        "version": "1",
                        "schemas": {
                            "request": "CompanySchema",
                            "response": "CompanySchema",
                            "params": None,
                        }
                    },
                ]
            }
        ],
        "schemas": [
            CompanySchema.to_dict()
        ]
    }

    client = AsyncHttpClient('0.0.0.0', 8000)

    # request = client.request(
    #         'POST',
    #         '/services',
    #         data=ujson.dumps(payload))
    # client.send(request)

    request = client.request('GET', '/services/registry', data=ujson.dumps(payload))
    service = client.send(request)[0].json
    pprint(service)

    # request = client.request('GET', '/services')
    # client.send(request)
