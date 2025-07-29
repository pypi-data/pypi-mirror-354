import spback.funcs as f


def test_id_gen():
  id1 = f.id_gen()
  id2 = f.id_gen()
  assert id1 != id2
