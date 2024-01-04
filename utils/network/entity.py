import pygame

from types import SimpleNamespace
from uuid import uuid4

EntityNetworkAttrs = SimpleNamespace

class ServerEntity:

    def __init__(self):
        self.id = uuid4()
        self.type = ''

        self.network_attrs = EntityNetworkAttrs()
    
    def compile_network_attrs(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class ClientEntity:

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        self.attrs = attrs
        self.type = ''

    def set_attrs(self, attrs: EntityNetworkAttrs):
        self.attrs = attrs

    def update(self, screen: pygame.Surface):
        raise NotImplementedError

_entity_types = {}

def add_entity_type(entity_type: str, classes: tuple[ServerEntity, ClientEntity]):
    _entity_types[entity_type] = classes

def create_server_entity(entity_type: str, *args) -> ServerEntity:
    return _entity_types[entity_type][0](*args)

def create_client_entity(entity_type: str, *args) -> ClientEntity:
    return _entity_types[entity_type][1](*args)
