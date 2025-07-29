from .fn import count, get_count
from .handler import ModelLogHandler


def test_handler():
  old = ModelLogHandler.__init__

  def new_init(self, *args, **kwargs):
    old(self, *args, **kwargs)
    count()

  ModelLogHandler.__init__ = new_init

  import logging

  logger = logging.getLogger(__name__)

  db_log = ""

  class FakeRecord:
    """read data from db_log"""

    log: str = ""

    def __init__(self, *args, **kwargs):
      self.log = db_log

    def save(self, update_fields=None):
      nonlocal db_log
      db_log = self.log

  logger.addHandler(ModelLogHandler(FakeRecord()))

  logger.info("test")
  logger.info("test")
  logger.info("test")
  logger.info("test")
  logger.info("test")
  logger.info("test")
  logger.info("test")

  assert get_count() == 1, "The handler only init once"
  assert db_log == "test\ntest\ntest\ntest\ntest\ntest\ntest\n", "The log is not correct"
