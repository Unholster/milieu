Milieu
======

Milieu allows easy parameter configuration using environment variables or
json files.

Usage Examples
==============

The following code creates a milieu instance that reads environment variables,
then reads the WORKON_HOME variable.

```
    >>> import milieu
    >>> M = milieu.init()
    >>> M.WORKON_HOME
    '/Users/andres/.virtualenvs'
```

The following code create a milieu instance from a json file, the reads the
several variables variable:

```
    >>> import milieu
    >>> M= milieu.init(path='/tmp/file.json')
    >>> M.foo
    u'fizz'
    >>> M.bar
    u'buzz'
    >>> M.baz
    [u'one', u'two', u'three']
```

The json associated to this example is:

```
    {
        "foo": "fizz",
        "bar": "buzz",
        "baz": ["one", "two", "three"]
    }
```
