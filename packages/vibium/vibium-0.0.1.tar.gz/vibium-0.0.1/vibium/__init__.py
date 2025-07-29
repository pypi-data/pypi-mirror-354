class Vibium:
    def __init__(self, device='default'):
        self.device = device

    def do(self, command):
        print(f"[{self.device}] Doing: {command}")

    def check(self, question):
        print(f"[{self.device}] Checking: {question}")
