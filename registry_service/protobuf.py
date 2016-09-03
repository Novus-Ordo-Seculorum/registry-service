import re


class CodeGenerator(object):
    FIELD_TYPENAMES = {
        'Str': 'string',
        'Int': 'int64',
        'Float': 'float',
        'Bool': 'bool',
        'Email': 'string',
        'Url': 'string',
        }

    def __init__(self, schemas:dict=None):
        self.schemas = schemas or {}

    def emit(self):
        visited = set()
        results = []
        messages = []
        for schema in self.schemas.values():
            messages.append(self._to_protobuf_message(schema))
        source = '\n'.join(messages)
        return source

    def _emit(self, schema:dict, visited:set, results:list):
        for field in schema['fields']:
            if field['type'] == 'Nested':
                nested_schema = self.schemas[field['nested']]
                _emit(nested_schema, visited, results)
        results.append(self._to_protobuf_message(schema))
        visited.add(schema['name'])

    def _to_protobuf_message(self, schema:dict):
        label = re.sub(r'Schema$', '', schema['name'])
        fields = [self._to_protobuf_field(f) for f in schema['fields']]
        return '''message {label} {{\n{fields}\n}}'''.format(
                label=label,
                fields='\n'.join(fields)).strip()

    def _to_protobuf_field(self, field:dict):
        attrs = field['attrs']
        return '  {required} {typename} {name} = {field_number};'.format(
            required='required' if attrs['required'] else 'optional',
            typename=self._get_typename(field),
            name=field['name'],
            field_number=attrs['field_number'],
            )

    def _get_typename(self, field):
        if field['type'] != 'Nested':
            return self.FIELD_TYPENAMES[field['type']]
        else:
            return field['attrs']['nested']
