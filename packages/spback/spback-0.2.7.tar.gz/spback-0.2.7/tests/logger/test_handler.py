import logging
import os
import threading
import time

import pytest

from spback.logger.handler import ComputeTaskHandler


@pytest.fixture
def create_logger():
  def fn(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

  return fn


def test_file_logger(create_logger):
  logger = create_logger("test")
  if os.path.exists("tmp/123.log"):
    os.unlink("tmp/123.log")
  logger.addHandler(ComputeTaskHandler().set_compute_id("123"))
  logger.info("test")

  assert os.path.exists("tmp/123.log")
  with open("tmp/123.log", "r") as f:
    assert f.read() == "test\n"


def test_file_logger_multithreading(create_logger):
  logger = create_logger("test_mt")
  if os.path.exists("tmp/test_mt.log"):
    os.unlink("tmp/test_mt.log")

  handler = ComputeTaskHandler().set_compute_id("test_mt")
  logger.addHandler(handler)

  def worker(thread_id):
    for i in range(5):
      logger.info(f"Thread-{thread_id} message {i}")
      time.sleep(0.01)  # 添加小延迟以增加线程交错的可能性

  # 创建多个线程
  threads = []
  for i in range(3):  # 创建3个线程
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

  # 等待所有线程完成
  for t in threads:
    t.join()

  assert os.path.exists("tmp/test_mt.log")
  # os.unlink("tmp/test_mt.log")
