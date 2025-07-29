# basic logic of ~

import random
import string


def id_gen() -> str:
  # generate id without repeated
  import uuid

  return str(uuid.uuid4())


def hide_details(debug: bool, message: str) -> str:
  if debug:
    return "unknown error, please check the request_id: {} log."
  else:
    return message


def random_string(N: int) -> str:
  return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
