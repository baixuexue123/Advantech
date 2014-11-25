#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'

import threading


class Worker(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args

    def getResult(self):
        return self.res

    def run(self):
        self.res = self.func(*self.args)

#用start()来启动线程
#用join()来等待线程结束
#用getResult()来获取函数结果
