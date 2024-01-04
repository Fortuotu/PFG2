from types import SimpleNamespace

EntityNetworkAttrs = SimpleNamespace

class ServerEntity:

    def __init__(self):
        self.network_attrs = None
    
    def compile_network_attrs(self):
        pass

    def update(self):
        pass

class ClientEntity:

    def __init__(self) -> None:
        pass

_entity_types = {}

def add_entity_type(entity_type: str, classes: tuple[ServerEntity, ClientEntity]):
    _entity_types[entity_type] = classes

def create_server_entity(entity_type: str, *args) -> ServerEntity:
    return _entity_types[entity_type][0](*args)

def create_client_entity(entity_type: str, *args) -> ClientEntity:
    return _entity_types[entity_type][1](*args)
