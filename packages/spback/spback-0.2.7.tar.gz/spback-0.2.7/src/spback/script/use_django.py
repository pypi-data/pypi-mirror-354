import os


def use_django(conf_path="conf.settings"):
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", conf_path)
  import django

  django.setup()


class DjangoCommand(object):
  def use_django(self, conf_path="conf.settings"):
    use_django(conf_path)

  def append_sys_path(self, path="."):
    import sys

    sys.path.append(path)

  def before_run(self):
    pass

  def after_run(self):
    pass

  def main(self):
    self.use_django()
    self.before_run()
    self.run()
    self.after_run()

  def run(self):
    pass
