import pygame

from types import SimpleNamespace
from itertools import count

EntityNetworkAttrs = SimpleNamespace

class ServerEntity:

    def __init__(self):
        self.network_attrs = EntityNetworkAttrs()
        self.global_vars = global_vars
    
    def compile_network_attrs(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class ClientEntity:

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        self.attrs = attrs
        self.global_vars = global_vars

    def set_attrs(self, attrs: EntityNetworkAttrs):
        self.attrs = attrs

    def update(self, screen: pygame.Surface):
        raise NotImplementedError

class EntityManager:

    def __init__(self):
        self._entities_organized_by_id = {}
        self._entities_organized_by_type_and_id = {}

        self._removed_entities = []

        self._entity_counter = count()

        self._entity_types = {}

    def add_entity_type(self, entity_type: str, classes: tuple[ServerEntity, ClientEntity]):
        self._entities_organized_by_type_and_id[entity_type] = {}
        self._entity_types[entity_type] = classes

    def create_server_entity(self, entity_type: str, *args) -> ServerEntity:
        entity = self._entity_types[entity_type][0](*args)

        entity_id = next(self._entity_counter)
        entity.id = entity_id

        self._entities_organized_by_id[entity_id] = entity
        self._entities_organized_by_type_and_id[entity_type][entity_id] = entity

        return entity

    def create_client_entity(self, entity_type: str, entity_id: int, *args) -> ClientEntity:
        entity = self._entity_types[entity_type][1](*args)

        self._entities_organized_by_id[entity_id] = entity
        self._entities_organized_by_type_and_id[entity_type][entity_id] = entity

        return entity
    
    def get_entities_by_type(self, entity_type: str):
        return self._entities_organized_by_type_and_id[entity_type]

    def get_all_entities(self):
        return self._entities_organized_by_id
    
    def add_entity_to_removed_entities(self, entity_id: int):
        self._removed_entities.append(entity_id)

    def update_entities(self):
        for entity_id, entity in self._entities_organized_by_id.items():
            entity.update()

    def flush_removed_entities(self):
        for entity_id in self._removed_entities:
            from pprint import pprint
            print()
            pprint(self._entities_organized_by_id)
            print()
            entity = self._entities_organized_by_id[entity_id]
            entity_type = entity.type

            del self._entities_organized_by_id[entity_id]

            del self._entities_organized_by_type_and_id[entity_type][entity_id]
        self._removed_entities.clear()

global_vars = object()

def set_entity_global_vars(gloabal_vars_obj):
    global global_vars
    global_vars = gloabal_vars_obj

entity_manager = EntityManager()