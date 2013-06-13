def init(**kwargs):
    return M(**kwargs)

__all__ = ['init']

class M(object):
    def __init__(self, path=None, env_prefix=None):
        self._cache = {}
        self._resolvers = []
        self._add_cache_resolver()
        self._add_env_resolver(env_prefix)
        if path:
            self._add_file_resolver(path)

    def __call__(self, namespace):
        return Namespace(self, namespace)

    def __getattr__(self, key):
        return self._resolve(key)

    def _add_cache_resolver(self):
        self._add_resolver(source=self._cache)

    def _add_env_resolver(self, prefix):
        import os
        if prefix is not None:
            keygen = lambda k: prefix + "_" + k
        else:
            keygen = None
        self._add_resolver(source=os.environ, keygen=keygen)

    def _add_file_resolver(self, path):
        import json
        contents = PathedDict(json.load(open(path, mode="r")))
        self._add_resolver(source=contents)

    def _add_resolver(self, source, keygen=None):
        if keygen is None:
            keygen = lambda k: k
        self._resolvers.append( (source, keygen) )

    def _into_cache(self, key, val):
        self._cache[key] = val
        return val

    def _resolve(self, key):
        if key.startswith("_"): raise KeyError
        for source, keygen in self._resolvers:
            try:
                return self._into_cache(key, source[keygen(key)])
            except KeyError:
                continue

class Namespace(object):
    def __init__(self, milieu, namespace):
        self.namespace = namespace
        self.milieu = milieu

    def __getattr__(self, key):
        return self.milieu._resolve(self.namespace+"."+key)

class PathedDict(dict):
    def __getitem__(self, key):
        print "Getting", key
        val = self
        for k in key.split("."):
            val = dict.__getitem__(val, k)
        return val