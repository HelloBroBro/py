import py
import types
import sys

def checksubpackage(name):
    obj = getattr(py, name)
    if hasattr(obj, '__map__'): # isinstance(obj, Module):
        keys = dir(obj)
        assert len(keys) > 0
        print (obj.__map__)
        for name in obj.__map__:
            assert hasattr(obj, name), (obj, name)

def test_dir():
    for name in dir(py):
        if not name.startswith('_'):
            yield checksubpackage, name

def test_virtual_module_identity():
    from py import path as path1
    from py import path as path2
    assert path1 is path2
    from py.path import local as local1
    from py.path import local as local2
    assert local1 is local2

def test_importall():
    base = py._pydir.join("impl")
    nodirs = [
        base.join('test', 'testing', 'data'),
        base.join('path', 'gateway',),
        base.join('code', 'oldmagic.py'),
        base.join('compat', 'testing'),
    ]
    if sys.version_info >= (3,0):
        nodirs.append(base.join('code', '_assertionold.py'))
    else:
        nodirs.append(base.join('code', '_assertionnew.py'))

    def recurse(p):
        return p.check(dotfile=0) and p.basename != "attic"

    for p in base.visit('*.py', recurse):
        if p.basename == '__init__.py':
            continue
        relpath = p.new(ext='').relto(base)
        if base.sep in relpath: # not py/*.py itself
            for x in nodirs:
                if p == x or p.relto(x):
                    break
            else:
                relpath = relpath.replace(base.sep, '.')
                modpath = 'py.impl.%s' % relpath
                check_import(modpath)

def check_import(modpath):
    py.builtin.print_("checking import", modpath)
    assert __import__(modpath)

def test_all_resolves():
    seen = py.builtin.set([py])
    lastlength = None
    while len(seen) != lastlength:
        lastlength = len(seen)
        for item in py.builtin.frozenset(seen):
            for value in item.__dict__.values():
                if isinstance(value, type(py.test)):
                    seen.add(value)
