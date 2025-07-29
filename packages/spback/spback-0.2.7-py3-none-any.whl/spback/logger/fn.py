def init_recorder():
  i = 0

  def count():
    nonlocal i
    i += 1

  def get_count():
    return i

  return count, get_count


count, get_count = init_recorder()
