class Cmd:
    def __init__(self):
        self.cmd = []

    def put_pose(self,pose):
        if pose == -1: 
            self.cmd = []
        else:
            if len(self.cmd) == 0:
                self.cmd.append(pose)
                return
            if self.cmd[-1] != pose:
                self.cmd.append(pose)
            if len(self.cmd) > 3:
                self.cmd.pop(0)
                
    def get_cmd(self):
        return self.cmd


if __name__ == "__main__":
    cmd = Cmd()
    cmd.put_pose(-1)
    print(cmd.cmd)
    cmd.put_pose(1)
    print(cmd.cmd)
    cmd.put_pose(2)
    print(cmd.cmd)
    cmd.put_pose(2)
    print(cmd.cmd)
    cmd.put_pose(3)
    print(cmd.cmd)
    cmd.put_pose(1)
    print(cmd.cmd)
