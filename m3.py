import time
import pymongo

from DRV8825_3 import DRV8825_3


class Motor3(DRV8825_3):
    steps = 25
    delay = 0.1
    client = pymongo.MongoClient(
        "mongodb://crepusculum.xyz:27017/",
        username="cube",
        password="123"
    )
    cubeDB = client["cube"]
    mini_cmd_collection = cubeDB["mini_cmd"]

    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        DRV8825_3.__init__(self, dir_pin, step_pin, enable_pin, mode_pins)
        self.SetMicroStep('softward', '1/32step')

    def motor3_clockwise(self, steps, stepdelay):  # motor3顺时针转动旋转槽
        self.motor3_anti_clockwise(steps, stepdelay)
        self.motor3_anti_clockwise(steps, stepdelay)
        self.motor3_anti_clockwise(steps, stepdelay)

    def motor3_anti_clockwise(self, steps, stepdelay):  # motor3顺时针转动旋转槽
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
            if cmd == "m3_clockwise":
                self.motor3_clockwise(self.steps, self.delay)
                self.update()
            elif cmd == "m3_anti":
                self.motor3_anti_clockwise(self.steps, self.delay)
                self.update()
            else:
                time.sleep(1)


if __name__ == "__main__":
    m3 = Motor3(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    m3.run()
