"""
Create customed logger

customed logger, write jsonfield of task compute.
"""

import logging


class ModelLogHandler(logging.Handler):
  """suitble for model has log attr.
  logger will save log to model.log, and save it after emit (when calling logger.info)."""

  def __init__(self, record):
    super().__init__()
    self.record = record

  def emit(self, record):
    log_entry = self.format(record)
    if self.record.log is None:
      self.record.log = ""
    self.record.log += log_entry + "\n"
    self.record.save(update_fields=["log"])


class ComputeTaskHandler(logging.Handler):
  """A file logger, support multiple threading, and set file path"""

  def __init__(self, level=logging.NOTSET):
    super().__init__(level)
    self.compute_id = None
    self.file = None

  def set_compute_id(self, compute_id: str) -> "ComputeTaskHandler":
    """Set compute id, and set file path."""
    self.compute_id = compute_id
    self.file = self.get_file_path()
    return self

  def get_file_name(self):
    return f"{self.compute_id}.log"

  def get_file_path(self):
    """Edit this function to change the file path."""
    return "tmp/" + self.get_file_name()

  def emit(self, record):
    with open(self.file, "a") as f:
      f.write(self.format(record) + "\n")
