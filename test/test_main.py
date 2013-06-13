import pytest
import milieu


def prepare_env(data):
    import os
    os.environ.update(data)

    def fin():
        for k in data.iterkeys():
            del os.environ[k]

    return fin

def prepare_file(data):
    import json
    from tempfile import NamedTemporaryFile
    tmpfile = NamedTemporaryFile(suffix='json')
    json.dump(data, tmpfile)
    tmpfile.flush()
    return tmpfile

@pytest.fixture(params=[None, 'MILIEU'])
def prefix(request):
    prefix = request.param+"_" if request.param else ''
    data = {
        prefix+'FOO': 'envfoo',
        prefix+'BAR': 'envbar',
        prefix+'ENVONLY': 'env',
    }

    fin = prepare_env(data)
    request.addfinalizer(fin)
    
    return request.param

@pytest.fixture
def file():
    data = {
        'FOO': 'filefoo',
        'BAR': 'filebar',
        'FILEONLY': 'file'
    }
    return prepare_file(data)
    

@pytest.fixture(params=['file', 'env'])
def namespaced_milieu(request):
    if request.param == 'env':
        data = {
                "ns1.FOO": 'foo1',
                "ns1.BAR": 'bar1',
                "ns2.FOO": 'foo2',
                "ns2.BAR": 'bar2',
                "ns2.ns3.FOO": "foo3",
            }
        fin = prepare_env(data)
        request.addfinalizer(fin)
        return milieu.init()
    else:
        data = {
                'ns1': {
                    'FOO': 'foo1',
                    'BAR': 'bar1',
                },
                'ns2': {
                    'FOO': 'foo2',
                    'BAR': 'bar2',
                    "ns3" : {
                        "FOO": "foo3",
                    }
                },
            }
        f = prepare_file(data)
        def fin():
            f.delete()
        return milieu.init(path=f.name)

def test_from_env(prefix):
    M = milieu.init(env_prefix=prefix)
    assert M.FOO == 'envfoo'
    assert M.BAR == 'envbar'
    assert M.ENVONLY == 'env'

def test_from_file(file):
    M = milieu.init(path=file.name)
    assert M.FOO == 'filefoo'
    assert M.BAR == 'filebar'
    assert M.FILEONLY == 'file'

def test_env_precedence(prefix, file):
    M = milieu.init(env_prefix=prefix, path=file.name)
    assert M.FOO == 'envfoo'
    assert M.BAR == 'envbar'
    assert M.ENVONLY == 'env'
    assert M.FILEONLY == 'file'

def test_namespace(namespaced_milieu):
    M = namespaced_milieu
    assert M("ns1").FOO == 'foo1'
    assert M("ns1").BAR == 'bar1'
    assert M("ns2").FOO == 'foo2'
    assert M("ns2").BAR == 'bar2'
    assert M("ns2.ns3").FOO == 'foo3'
