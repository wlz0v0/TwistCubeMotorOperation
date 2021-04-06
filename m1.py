import time, _thread

import pymongo

from DRV8825_12 import DRV8825_12


class Motor1(DRV8825_12):
    only_steps = 6500
    both_steps = 8700
    only_delay = 0.001
    both_delay = 0.001
    client = pymongo.MongoClient(
        "mongodb://crepusculum.xyz:27017/",
        username="cube",
        password="123"
    )
    cubeDB = client["cube"]
    mini_cmd_collection = cubeDB["mini_cmd"]

    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        DRV8825_12.__init__(self, dir_pin, step_pin, enable_pin, mode_pins)

    def motor1_up_to_3_only(self, steps, stepdelay):  # motor1顶起魔方至第三层并且只被旋转槽固定
        self.TurnStep('forward', steps, stepdelay)
        # self.Stop()

    def motor1_up_to_3_both(self, steps, stepdelay):  # motor1顶起魔方至第三层并且同时被固定槽和旋转槽固定
        self.TurnStep('forward', steps, stepdelay)  # steps的值根据实际情况需要再调
        # self.Stop()

    def motor1_down_to_2_from_only(self, steps, stepdelay):  # motor1让魔方从1的状态下降到第二层
        self.TurnStep('backward', steps, stepdelay)  # steps的值根据实际情况需要再调
        # self.Stop()

    def motor1_down_to_2_from_both(self, steps, stepdelay):  # motor1让魔方从1的状态下降到第二层
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
            if cmd == "m1_up_only":
                self.motor1_up_to_3_only(self.only_steps, self.only_delay)
                self.update()
            elif cmd == "m1_up_both":
                self.motor1_up_to_3_both(self.both_steps, self.both_delay)
                self.update()
            elif cmd == "m1_down_only":
                self.motor1_down_to_2_from_only(self.only_steps, self.only_delay)
                self.update()
            elif cmd == "m1_down_both":
                self.motor1_down_to_2_from_both(self.both_steps, self.both_delay)
                self.update()
            else:
                time.sleep(1)


if __name__ == "__main__":
    m1 = Motor1(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    m1.run()
