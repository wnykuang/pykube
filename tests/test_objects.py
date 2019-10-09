from unittest.mock import MagicMock

import pytest

import pykube
from pykube.objects import Pod, NamespacedAPIObject


def test_api_object():
    pod = Pod(None, {'metadata': {'name': 'myname'}})
    assert repr(pod) == '<Pod myname>'
    assert str(pod) == 'myname'
    assert pod.metadata == {'name': 'myname'}
    assert pod.labels == {}
    assert pod.annotations == {}


def test_object_factory_succeeds():
    api = MagicMock()
    api.resource_list.return_value = {'resources': [{'kind': 'ExampleObject', 'namespaced': True, 'name': 'exampleobjects'}]}
    ExampleObject = pykube.object_factory(api, 'example.org/v1', 'ExampleObject')
    assert ExampleObject.kind == 'ExampleObject'
    assert ExampleObject.endpoint == 'exampleobjects'
    assert ExampleObject.version == 'example.org/v1'
    assert NamespacedAPIObject in ExampleObject.mro()


def test_object_factory_raises_for_unknown_kind():
    api = MagicMock()
    api.resource_list.return_value = {'resources': [{'kind': 'ExampleObject', 'namespaced': True, 'name': 'exampleobjects'}]}
    with pytest.raises(ValueError):
        pykube.object_factory(api, 'example.org/v1', 'OtherObject')


def test_set_annotation():
    pod = Pod(None, {'metadata': {'name': 'myname'}})
    pod.annotations['foo'] = 'bar'
    assert pod.annotations['foo'] == 'bar'


def test_set_label():
    pod = Pod(None, {'metadata': {'name': 'myname'}})
    pod.labels['foo'] = 'bar'
    assert pod.labels['foo'] == 'bar'


def test_update():
    pod = Pod(None, {'metadata': {'name': 'myname'}})
    pod.api = MagicMock()
    pod.update(is_strategic=False)
    raise ValueError(pod.obj)
