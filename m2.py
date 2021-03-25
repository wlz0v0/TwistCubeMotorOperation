import time

from DRV8825_12 import DRV8825_12


class Motor2(DRV8825_12):
    steps = 66
    delay = 0.005

    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        DRV8825_12.__init__(self, dir_pin, step_pin, enable_pin, mode_pins)

    def motor2_clockwise(self, steps, stepdelay):  # motor2让L型支架顺时针翻转（让上面向下翻转作为正面 从右边看是正L形）
        self.TurnStep('forward', steps, stepdelay)  # steps的值根据实际情况需要再调
        # self.Stop()

    def motor2_anti_clockwise(self, steps, stepdelay):  # motor2让L型支架顺时针翻转（让上面向下翻转作为正面 从右边看是正L形）
        self.TurnStep('backward', steps, stepdelay)  # steps的值根据实际情况需要再调
        # self.Stop()

    def get_cmd(self):
        temp_cmd = input()
        return temp_cmd

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
    m2 = Motor2(dir_pin=2, step_pin=3, enable_pin=4, mode_pins=(14, 15, 18))
    m2.run()
