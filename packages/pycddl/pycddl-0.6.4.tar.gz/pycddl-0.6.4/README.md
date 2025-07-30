# PyCDDL: Deserialize CBOR and/or do CDDL schema validation

[CDDL](https://www.rfc-editor.org/rfc/rfc8610.html) is a schema language for the CBOR serialization format.
`pycddl` allows you to:

* Validate CBOR documents match a particular CDDL schema, based on the Rust [`cddl`](https://github.com/anweiss/cddl) library.
* Optionally, decode CBOR documents.

## Usage

### Validation

Here we use the [`cbor2`](https://pypi.org/project/cbor2/) library to serialize a dictionary to CBOR, and then validate it:

```python
from pycddl import Schema
import cbor2

uint_schema = Schema("""
    object = {
        xint: uint
    }
"""
)
uint_schema.validate_cbor(cbor2.dumps({"xint", -2}))
```

If validation fails, a `pycddl.ValidationError` is raised.

### Validation + deserialization

You can deserialize CBOR to Python objects using `cbor.loads()`.
However:

* `cbor2` uses C code by default, and the C programming language is prone to memory safety issues.
  If you are reading untrusted CBOR, better to use a Rust library to decode the data.
* You will need to parse the CBOR twice, once for validation and once for decoding, adding performance overhead.

By deserializing with `pycddl`, you solve the first problem, and a future version of `pycddl` will solve the second problem (see https://gitlab.com/tahoe-lafs/pycddl/-/issues/37).

```python
from pycddl import Schema
import cbor2

uint_schema = Schema("""
    object = {
        xint: uint
    }
"""
)
deserialized = uint_schema.validate_cbor(cbor2.dumps({"xint", -2}), True)
assert deserialized == {"xint": -2}
```

### Deserializing without schema validation

If you don't care about schemas, you can just deserialize the CBOR like so:

```python
from pycddl import Schema

ACCEPT_ANYTHING = Schema("main = any")

def loads(encoded_cbor_bytes):
    return ACCEPT_ANYTHING.validate_cbor(encoded_cbor_bytes, True)
```

In a future release this will become a standalone, more efficient API, see https://gitlab.com/tahoe-lafs/pycddl/-/issues/36

### Reducing memory usage and safety constraints

In order to reduce memory usage, you can pass in any Python object that implements the buffer API and stores bytes, e.g. a `memoryview()` or a `mmap` object.

**The passed-in object must be read-only, and the data must not change during validation!**
If you mutate the data while validation is happening the result can be memory corruption or other [undefined behavior](https://stackoverflow.com/questions/18506029/can-undefined-behavior-erase-the-hard-drive#comment27209771_18506029).

## Supported CBOR types for deserialization

If you are deserializing a CBOR document into Python objects, you can deserialize:

* Null/None.
* Booleans.
* Floats.
* Integers up to 64-bit size.
  Larger integers aren't supported yet.
* Bytes.
* Strings.
* Lists.
* Maps/dictionaries.
* Sets.

Other types will be added in the future if there is user demand.

Schema validation is not restricted to this list, but rather is limited by the functionality of the [`cddl` Rust crate](https://github.com/anweiss/cddl).

## Release notes

### 0.6.4

Features:

* Update Rust [CDDL](https://crates.io/crates/cddl/) dependency to update transitive dependency [lexical-core](https://crates.io/crates/lexical-core) which had been revised (i.a.) because of soundness/safety issues.

### 0.6.3

Features:

* Support final 3.13.

### 0.6.2

Features:

* Added support for Python 3.13.

### 0.6.1

Bug fixes:

* Allow PyPy to deserialize CBOR too.

### 0.6.0

Features:

* `validate_cbor(serialized_cbor, True)` will deserialize the CBOR document into Python objects, so you don't need to use e.g. `cbor2.loads(serialized_cbor)` separately.

Bug fixes:

* Release the GIL in a much more useful way.

Misc:

* Upgrade to newer `cddl` crate (0.9.4).

### 0.5.3

* Upgrade to newer `cddl` crate (0.9.3).
* Add Python 3.12 support.

### 0.5.2

* Upgrade to newer `cddl` crate (0.9.2), improving validation functionality.

### 0.5.1

* Upgrade to newer `cddl` crate, fixing some validation bugs.

### 0.5.0

* Support for ARM macOS.
* Dropped Python 3.7 support.

### 0.4.1

* Test fixes, with no user-relevant changes.

### 0.4.0

* `validate_cbor()` now accepts read-only buffers, not just `bytes`. This is useful if you want to e.g. validate a large file, since you can `mmap()` it.
* The GIL is released when parsing documents larger than 10KiB.

### 0.3.0

* Fixed major bug where if the document was valid UTF-8, the library would attempt to parse it as JSON!
* Added support for ARM macOS.

### 0.2.2

* Updated to `cddl` 0.9.1.

### 0.2.1

* Added PyPy wheels.

### 0.2.0

* Schemas are now only parsed once (when the `Schema()` object is created), instead of every time validation happens, which should improve validation performance.
* Updated to a newer version of [underlying CDDL library](https://github.com/anweiss/cddl), which should make CDDL parsing more compliant.
* Added a `repr()` implementation to `Schema` for easier debugging.

### 0.1.11

* Initial release.
