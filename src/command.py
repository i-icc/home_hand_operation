import queue

class Cmd:
    def __init__(self):
        self.cmd = queue.Queue(3)


if __name__ == "__main__":
    cmd = Cmd()
