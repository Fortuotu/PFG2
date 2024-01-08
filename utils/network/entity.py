import pygame

from types import SimpleNamespace
from uuid import uuid4
from itertools import count

EntityNetworkAttrs = SimpleNamespace

class ServerEntity:

    def __init__(self):
        self.network_attrs = EntityNetworkAttrs()
    
    def compile_network_attrs(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class ClientEntity:

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        self.attrs = attrs

    def set_attrs(self, attrs: EntityNetworkAttrs):
        self.attrs = attrs

    def update(self, screen: pygame.Surface):
        raise NotImplementedError

_entity_types = {}

_entity_counter = count()

_entities_organized_by_id = {}
_entities_organized_by_type_and_id = {}

def add_entity_type(entity_type: str, classes: tuple[ServerEntity, ClientEntity]):
    classes[0].entity_type = entity_type
    classes[1].entity_type = entity_type

    _entities_organized_by_type_and_id[entity_type] = {}

    _entity_types[entity_type] = classes

def create_server_entity(entity_type: str, *args) -> ServerEntity:
    entity = _entity_types[entity_type][0](*args)

    entity_id = next(_entity_counter)
    entity.id = entity_id

    _entities_organized_by_id[entity_id] = entity
    _entities_organized_by_type_and_id[entity_type][entity_id] = entity

    return entity

def remove_entity(entity_id: int):
    entity = _entities_organized_by_id[entity_id]
    entity_type = entity.type

    del _entities_organized_by_id[entity_id]

    del _entities_organized_by_type_and_id[entity_type][entity_id]

def get_entities_by_type(entity_type: str):
    return _entities_organized_by_type_and_id[entity_type]

def create_client_entity(entity_type: str, entity_id: int, *args) -> ClientEntity:
    entity = _entity_types[entity_type][1](*args)

    _entities_organized_by_id[entity_id] = entity
    _entities_organized_by_type_and_id[entity_type][entity_id] = entity

    return entity

def get_entities():
    return _entities_organized_by_id

def update_entities():
    for entity in _entities_organized_by_id:
        entity.update()
