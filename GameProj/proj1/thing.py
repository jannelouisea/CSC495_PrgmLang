def kv(d):
  return '\n' + '\n '.join(['%s: %s' % (k, d[k])
                          for k in sorted(d.keys()) if k[0] != "_"]) + '\n'

class Thing(object):
  def __repr__(i) : return i.__class__.__name__ + kv(i.__dict__)
