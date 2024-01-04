import pygame

class PingPacket: pass


class EntityUpdatePacket:

    def __init__(self, entity_type, entity_id: int, entity_attrs):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.entity_attrs = entity_attrs

class EntitiesUpdatePacket:

    def __init__(self, entity_packets):
        self.entity_packets = entity_packets

class KeyInputPacket:
    
    def __init__(self, key, key_down=False, key_up=False):
        self.key = key
        self.key_down = key_down
        self.key_up = key_up
