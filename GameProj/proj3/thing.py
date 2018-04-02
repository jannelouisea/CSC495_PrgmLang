def kv(d):
    return '\n' + '\n '.join(['%s: %s' % (k, d[k])
                          for k in sorted(d.keys()) if k[0] != "_"]) + '\n'


class Thing(object):
    def __repr__(self):
        return self.__class__.__name__ + kv(self.__dict__)
