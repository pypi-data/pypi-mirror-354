//! Deserialize CBOR to Python objects.

use ciborium::value::Value;
use pyo3::{prelude::*, types::{PyNone, PyList, PyDict, PyBytes, PySet}, exceptions::PyValueError};

/// Convert a CBOR value into an equivalent tree of Python objects.
pub fn deserialize(py: Python<'_>, value: &Value) -> PyResult<PyObject> {
    match value {
        Value::Integer(int) => Ok(i128::from(*int).to_object(py)),
        Value::Bytes(vec) => Ok(PyBytes::new_bound(py, vec).to_object(py)),
        Value::Float(float) => Ok(float.to_object(py)),
        Value::Text(string) => Ok(string.to_object(py)),
        Value::Bool(boolean) => Ok(boolean.to_object(py)),
        Value::Null => Ok(PyNone::get_bound(py).to_object(py)),
        Value::Array(array_values) => {
            let result = PyList::empty_bound(py);
            for array_value in array_values {
                result.append(deserialize(py, array_value)?)?;
            }
            Ok(result.to_object(py))
        },
        Value::Map(map_pairs) => {
            let result = PyDict::new_bound(py);
            for (key, value) in map_pairs {
                let key = deserialize(py, key)?;
                let value = deserialize(py, value)?;
                result.set_item(key, value)?;
            }
            Ok(result.to_object(py))
        },
        Value::Tag(tag, tagged_value) => deserialize_tagged(py, *tag, tagged_value),
        _ => Err(PyValueError::new_err("Unsupported CBOR type"))
    }
}

/// Decoded a tagged value that isn't built-in to ciborium.
fn deserialize_tagged(py: Python<'_>, tag: u64, value: &Value) -> PyResult<PyObject> {
    match (tag, value) {
        (258, Value::Array(array_values)) => {
            let result = PySet::empty_bound(py)?;
            for array_value in array_values {
                result.add(deserialize(py, array_value)?)?;
            }
            Ok(result.to_object(py))
        },
        _ =>  Err(PyValueError::new_err(format!("Tag {tag} not yet supported, please file an issue at https://gitlab.com/tahoe-lafs/pycddl"))),
    }
}
