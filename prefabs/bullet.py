from pygame import Surface
from utils.network.entity import *
from utils.network.entity import EntityNetworkAttrs

class ServerBullet(ServerEntity):

    def __init__(self):
        super().__init__()

    def compile_network_attrs(self):
        return super().compile_network_attrs()
    
    def update(self):
        return super().update()
    
class ClientBullet(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        super().__init__(attrs)

    def update(self, screen: Surface):
        return super().update(screen)

add_entity_type('bullet', (ServerBullet, ClientBullet))
