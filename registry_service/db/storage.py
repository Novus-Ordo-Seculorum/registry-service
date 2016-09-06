from ujson import loads, dumps

from threading import RLock

from redis import StrictRedis


META = 'service.meta'
ROUTES = 'service.routes'
SCHEMAS = 'service.schemas'
PROTO = 'service.proto'

ALL_KEYS = [
    META, ROUTES, SCHEMAS, PROTO,
    ]


class ServiceStorage(object):

    _instance = None
    _instance_lock = RLock()

    @classmethod
    def get_instance(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = ServiceStorage()
        return cls._instance

    def __init__(self):
        # This assumes Redis is running on localhost on the default port.
        self.redis = StrictRedis()

    def delete_service(self, service_name:str):
        for k in ALL_KEYS:
            self.redis.hdel(k, service_name)

    def save_service(self, service:dict):
        meta = service.copy()
        self.redis.hset(ROUTES, meta['name'], dumps(meta.pop('routes')))
        self.redis.hset(SCHEMAS, meta['name'], dumps(meta.pop('schemas')))
        self.redis.hset(PROTO, meta['name'], meta.pop('proto'))
        self.redis.hset(META, meta['name'], dumps(meta))

    def get_service(self, service_name):
        if self.redis.hexists(META, service_name):
            service = loads(self.redis.hget(META, service_name))
            service['routes'] = self.get_routes_by_service(service_name)
            service['schemas'] = self.get_schemas_by_service(service_name)
            service['proto'] = self.get_proto_by_service(service_name)
            return service
        return None

    def get_services(self):
        return [
            self.get_service(name) for name in self.get_service_names()
            ]

    def get_service_names(self):
        return [k.decode() for k in self.redis.hkeys(META)]

    def get_routes_by_service(self, service_name):
        if self.redis.hexists(ROUTES, service_name):
            return loads(self.redis.hget(ROUTES, service_name))
        return None

    def get_schemas_by_service(self, service_name:str):
        if self.redis.hexists(SCHEMAS, service_name):
            return loads(self.redis.hget(SCHEMAS, service_name))
        return None

    def get_proto_by_service(self, service_name:str):
        if self.redis.hexists(PROTO, service_name):
            return self.redis.hget(PROTO, service_name).decode()
        return None
