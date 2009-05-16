#!/usr/bin/python

import time


class MeasureTime:
  def __init__(self):
    self.startTime = 0

  def start(self):
    self.startTime = time.time()

  def finish(self):
    endtime = time.time()
    return endtime - self.startTime

