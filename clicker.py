#!/usr/bin/env python3

import pyautogui
import yaml
import sys
import os.path
import time
import signal


class Clicker:
    def __init__(self):
        self.x = None
        self.y = None
        self.once = True
        self.interval = None
        self.file = './clicker.yaml'

    @staticmethod
    def exit(sig, frame):
        print("signal", sig, frame)
        return

    def catch_signal(self):
        for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM, signal.SIGKILL]:
            signal.signal(sig, self.exit)

    def get_config(self):
        if not os.path.exists(self.file):
            raise Exception('无法找到配置文件')

        with open('./clicker.yaml', 'r') as f:
            try:
                config = yaml.safe_load(f)
                x = config.get('x')
                y = config.get('y')
                interval = config.get('interval')
                once = config.get('once', True)
                if not x or not y or not interval:
                    raise Exception('坐标配置缺失')
                if interval < 10:
                    raise Exception('鼠标点击时间间隔太短')
                self.x = x
                self.y = y
                self.interval = interval
                self.once = once
            except yaml.YAMLError as error:
                print('读取配置异常: {}'.format(str(error)))
                sys.exit(1)

    def run(self):
        print('程序运行中...')
        while True:
            pyautogui.moveTo(self.x, self.y)
            if self.once:
                print('测试完毕，退出')
                sys.exit(0)
            pyautogui.click()
            time.sleep(self.interval)


def signal_handler(signum, frame):
    print('程序退出')


if __name__ == '__main__':
    try:
        for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
            signal.signal(sig, signal_handler)
        clicker = Clicker()
        clicker.get_config()
        clicker.run()
    except Exception as e:
        print('程序运行错误: {}'.format(str(e)))
