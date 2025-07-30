# pyavro-gen

Standard Avro implementation for Python is typeless and operates on `dict`s.
While this is convenient for small projects, larger ones, often with hundreds of schemas, 
certainly benefit from the ability to enforce schemas during record construction.   

This library allows Python Avro users to employ Specific Records.

## Usage:

```bash
pip install pyavro-gen
```

```bash
pyavrogen.py -v \
    -i my_schemas_dir \
    -o jaumoavro \
    -ie 'avsc' \
    -b com.jaumo.schema \
    -r com.jaumo.schema.rpc \
    -t com.jaumo.schema.type
```

Now you can import your classes like

```python
from jaumoavro.com.jaumo.schema.domain.user import Updated

u = Updated(...)
```

## Generation and test programmatically

```python
from avro_preprocessor.avro_paths import AvroPaths
from pyavro_gen.generator import AvroGenerator

generator = AvroGenerator(
    AvroPaths(
        input_path='myschemas/',
        output_path='avroclasses/',
        input_schema_file_extension='avsc',
        base_namespace='com.jaumo.schema',
        rpc_namespace='com.jaumo.schema.rpc',
        types_namespace='com.jaumo.schema.type',
    )
)
generator.process()
```

### Generation using custom classes:

```python
from pyavro_gen.generation_classes import GENERATION_CLASSES, GenerationClassesType
from pyavro_gen.codewriters.base import Decorator, ClassWriter, Extension
from typing import Optional

# First define two custom ClassWriters

class RpcWriter(ClassWriter):
    def __init__(self,
                 fully_qualified_name: str,
                 doc: Optional[str] = None,
                 prefix: Optional[str] = None):
        super().__init__(fully_qualified_name, doc, prefix)

        self.extensions = [
            Extension('abc.ABC')
        ]


class UndictifiableClassWriter(ClassWriter):
    def __init__(self,
                 fully_qualified_name: str,
                 doc: Optional[str] = None,
                 prefix: Optional[str] = None):
        super().__init__(fully_qualified_name, doc, prefix)

        self.decorators = [
            Decorator('@type_checked_constructor()',
                      ClassWriter('undictify.type_checked_constructor')),
            Decorator('@dataclass', ClassWriter('dataclasses.dataclass'))
        ]


# Then, register them in the GENERATION_CLASSES variable

GENERATION_CLASSES[GenerationClassesType.RECORD_CLASS] = UndictifiableClassWriter
GENERATION_CLASSES[GenerationClassesType.RPC_CLASS] = RpcWriter

# Then, generate classes in module `avroclasses` as shown above.
```
