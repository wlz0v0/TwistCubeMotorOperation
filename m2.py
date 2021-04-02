import time

import pymongo

from DRV8825_12 import DRV8825_12


class Motor2(DRV8825_12):
    steps = 66
    delay = 0.005
    client = pymongo.MongoClient(
        "mongodb://crepusculum.xyz:27017/",
        username="cube",
        password="123"
    )
    cubeDB = client["cube"]
    mini_cmd_collection = cubeDB["mini_cmd"]

    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        DRV8825_12.__init__(self, dir_pin, step_pin, enable_pin, mode_pins)

    def motor2_clockwise(self, steps, stepdelay):  # motor2让L型支架顺时针翻转（让上面向下翻转作为正面 从右边看是正L形）
        self.TurnStep('forward', steps, stepdelay)  # steps的值根据实际情况需要再调
        # self.Stop()

    def motor2_anti_clockwise(self, steps, stepdelay):  # motor2让L型支架顺时针翻转（让上面向下翻转作为正面 从右边看是正L形）
        self.TurnStep('backward', steps, stepdelay)  # steps的值根据实际情况需要再调
        # self.Stop()

    def get_cmd(self):
        mini_cmd = self.mini_cmd_collection.find_one()
        if mini_cmd is None:
            return
        if len(mini_cmd["mini_cmd"]) == 0:
            return "-1"  # 随便返回
        temp_cmd = mini_cmd["mini_cmd"][0]
        return temp_cmd

    def update(self):
        mini_cmd = self.mini_cmd_collection.find_one()
        if mini_cmd is None:
            return
        if len(mini_cmd["mini_cmd"]) == 0:
            return
        self.mini_cmd_collection.delete_many({})
        new_mini_cmd = mini_cmd["mini_cmd"]
        del (new_mini_cmd[0])
        self.mini_cmd_collection.insert_one({"mini_cmd": new_mini_cmd})
        return

    def run(self):
        while True:
            cmd = self.get_cmd()
            if cmd == "m2_clockwise":
                self.motor2_clockwise(self.steps, self.delay)
            elif cmd == "m2_anti":
                self.motor2_clockwise(self.steps, self.delay)
            else:
                time.sleep(1)


if __name__ == "__main__":
    m2 = Motor2(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    m2.run()
