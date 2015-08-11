import unittest
import mock
from savory_pie.resources import _ParamsImpl, EmptyParams, BasicResource, Resource


class EmptyParamsTestCase(unittest.TestCase):

    def test_get(self):
        params = EmptyParams()
        self.assertEqual(params.get('key', default='value'), 'value')

    def test_get_as(self):
        params = EmptyParams()
        self.assertEqual(params.get_as('key', str, default='value'), 'value')

    def test_get_list(self):
        params = EmptyParams()
        self.assertEqual(params.get_list('key'), [])

    def test_get_list_of(self):
        params = EmptyParams()
        self.assertEqual(params.get_list_of('key', str), [])


class ParamsImplTestCase(unittest.TestCase):
    def test_init(self):
        params = _ParamsImpl('some var')
        self.assertEqual(params._GET, 'some var')

    def test_keys(self):
        params = _ParamsImpl({'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(sorted(params.keys()), ['key1', 'key2'])

    def test_contains(self):
        params = _ParamsImpl({'key1': 'value1', 'key2': 'value2'})
        self.assertTrue('key1' in params)
        self.assertFalse('key3' in params)

    def test_get_item(self):
        params = _ParamsImpl({'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(params['key1'], 'value1')

    def test_parameters_get(self):
        params = _ParamsImpl({'key1': 'value1'})
        self.assertEqual(params.get('key1', 'other'), 'value1')

    def test_parameters_get_default(self):
        params = _ParamsImpl({'key1': 'value1'})
        self.assertEqual(params.get('some', 'other'), 'other')

    def test_parameters_get_as(self):
        params = _ParamsImpl({'key1': 'value1'})
        self.assertEqual(params.get_as('key1', str, 'other'), 'value1')

    def test_parameters_get_as_wrong_type(self):
        params = _ParamsImpl({'key1': 1})
        self.assertEqual(params.get_as('key1', str, 'other'), '1')

    def test_parameters_get_as_default(self):
        params = _ParamsImpl({'key1': 1})
        self.assertEqual(params.get_as('key2', str, 'other'), 'other')

    def test_parameters_get_list(self):
        get = mock.Mock()
        get.getlist.return_value = ['value1']
        params = _ParamsImpl(get)
        self.assertEqual(params.get_list('key1'), ['value1'])

    def test_get_list_of(self):
        params = _ParamsImpl({'key1': [1]})
        self.assertEqual(params.get_list_of('key1', str), ['1'])

    def test_get_list_of_not_found(self):
        params = _ParamsImpl({'key1': [1]})
        self.assertEqual(params.get_list_of('key2', str), [])


class TestBasicResource(BasicResource):
    path = 'test'

    def get(self):
        pass

    def extra_method(self):
        pass


class BasicResourceTestCase(unittest.TestCase):

    def test_init_empty(self):
        resource = TestBasicResource()

        self.assertEqual(resource.key, '')
        self.assertEqual(resource.resource_path, 'test')
        self.assertEqual(resource.allowed_methods, set(['GET']))
        self.assertIsNone(resource.get_child_resource({}, False))

    def test_init_with_dict(self):
        data = {
            'stringKey': 'stringValue',
            'numberKey': 1,
            'arrayKey': ['value1', 'value2', 'value3'],
            'objectKey': {
                'key': 'value'
            }
        }
        resource = TestBasicResource(data)

        self.assertDictEqual(data, resource)
        self.assertEqual(resource.key, '')
        self.assertEqual(resource.resource_path, 'test')

    def test_init_with_dict_and_id(self):
        data = {
            'id': '12335'
        }

        resource = TestBasicResource(data)

        self.assertEqual(resource.key, data['id'])
        self.assertEqual(resource.resource_path, 'test/' + data['id'])

    def test_update(self):
        resource = TestBasicResource()

        resource.field = 'string'

        self.assertEqual(resource.field, 'string')
        self.assertEqual(resource['field'], 'string')

    def test_delete(self):
        resource = TestBasicResource({
            'field': 123
        })

        del resource.field

        self.assertNotIn('field', resource)

    def test_access_invalid_attribute(self):
        resource = TestBasicResource()

        with self.assertRaises(AttributeError):
            resource.field

    def test_delete_invalid_attribute(self):
        resource = TestBasicResource()

        with self.assertRaises(AttributeError):
            del resource.path


class TestResource(Resource):
    resource_path = 'resource_path'

    def get(self):
        pass

    def extra_method(self):
        pass


class ResourceTestCase(unittest.TestCase):

    def test_init(self):
        resource = TestResource()

        self.assertEqual(resource.resource_path, 'resource_path')
        self.assertEqual(resource.allowed_methods, set(['GET']))
        self.assertIsNone(resource.get_child_resource({}, False))
