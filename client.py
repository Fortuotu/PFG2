import pygame, sys

from utils.network.game_socket import ClientSocket

class Game:
    
    def __init__(self):
        self.sock = ClientSocket()
        self.sock.set_socket_recv_buffer_size(1024)

        self.screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10

        self.entities = {}

    def recv_packets_and_keep_connection(self):
        while self.running:
            packet = self.sock.recv_packet()
            if packet:
                pass

    def run(self):
        self.sock.connect_to_server('localhost', 9999)
        self.sock.send_packet('CONNECT')

        while self.running:
            packet = self.sock.recv_packet()
            if packet:
                print(packet)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()
            self.clock.tick(self.fps)
            self.screen.fill((255, 255, 255))

            self.sock.ping_server()
        pygame.quit()
        sys.exit()

Game().run()
