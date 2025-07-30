use cddl::{
    ast::CDDL,
    validator::{cbor::CBORValidator, Validator},
};
use pyo3::{
    buffer::{PyBuffer, ReadOnlyCell},
    create_exception,
    exceptions::{PyException, PyTypeError, PyValueError},
    prelude::*,
};
use self_cell::self_cell;
use std::mem::size_of;

mod deserialize;

/// A CDDL schema that can be used to validate CBOR documents.
#[pyclass]
struct Schema {
    // We need to do a song-and-dance with an inner struct so we don't have to
    // worry about how the self_cell! macro and PyO3 macros interact.
    inner: SchemaImpl,
}

self_cell! {
    struct SchemaImpl {
        // Keep around the underlying data.
        owner: String,

        // The parsed schema:
        #[covariant]
        dependent: CDDL,
    }
}

#[pymethods]
impl Schema {
    /// Create a new ``Schema`` given a string with the CDDL specification.
    #[new]
    fn new(schema_string: String) -> PyResult<Self> {
        let inner = SchemaImpl::try_new(schema_string, |s: &String| CDDL::from_slice(s.as_bytes()))
            .map_err(PyValueError::new_err)?;
        Ok(Schema { inner })
    }

    fn __repr__(&self) -> String {
        format!(r#"Schema("""{}""")"#, self.inner.borrow_owner())
    }

    /// Validate a CBOR document in string format, throwing a ``ValidateError``
    /// if validation failed. If the ``deserialize`` argument is true, the CBOR
    /// will be deserialized to Python objects and returned.
    #[pyo3(signature = (cbor, deserialize=false))]
    fn validate_cbor(&self, py: Python<'_>, cbor: &Bound<'_, PyAny>, deserialize: bool) -> PyResult<PyObject> {
        let buffer = PyBuffer::<u8>::get_bound(cbor)?;
        // PyPy has weird issues with this flag.
        if !cfg!(PyPy) && !buffer.readonly() {
            return Err(PyValueError::new_err("Must be a read-only byte buffer (and you should never mutate it during validation)"));
        }
        let slice = buffer
            .as_slice(py)
            .ok_or_else(|| PyTypeError::new_err("Must be a contiguous sequence of bytes"))?;

        // The slice is &[ReadOnlyCell<u8>]. A ReadOnlyCell has the same memory
        // representation as the underlying data; it's #[repr(transparent)]
        // newtype around UnsafeCell. And per Rust docs "UnsafeCell<T> has the
        // same in-memory representation as its inner type T". Here's a
        // compile-time assertion that demonstrates that:
        const _: () = assert!(
            size_of::<ReadOnlyCell<u8>>() == size_of::<u8>(),
            "ReadOnlyCell<u8> is different size than u8?!"
        );
        // Safety: Given the two types are the same size, the main safety issue
        // with the transmute is whether the data is _really_ read-only. We do
        // the read-only check above, and we document that the data shouldn't be
        // mutated during validation.
        let (before, cbor, after) = unsafe { slice.align_to::<u8>() };
        assert_eq!(before.len(), 0);
        assert_eq!(after.len(), 0);

        let parse = || ciborium::de::from_reader::<ciborium::value::Value, _>(cbor);

        let parse_and_validate = || {
            let parsed_cbor = parse().map_err(|e| ValidationError::new_err(format!("{}", e)))?;
            let schema = self.inner.borrow_dependent();
            let mut cv = CBORValidator::new(schema, parsed_cbor, None);
            cv.validate()
                .map_err(|e| ValidationError::new_err(format!("{}", e)))
        };

        let document_size = cbor.len();
        if document_size > 10 * 1024 {
            // For larger documents, parsing can get expensive, so release
            // the GIL to enable parallelism.
            Python::allow_threads(py, parse_and_validate)?;
        } else {
            parse_and_validate()?;
        }

        if deserialize {
            // Unfortunately CBORValidator takes ownership of the Value, so we
            // need to parse twice (https://github.com/anweiss/cddl/issues/216).
            // Cloning would use lots more memory, so better to use CPU.
            let parsed_cbor = if document_size > 10 * 1024 {
                Python::allow_threads(py, parse)
            } else {
                parse()
            }
            .expect("This should never error since this is the second time we're parsing...");
            crate::deserialize::deserialize(py, &parsed_cbor)
        } else {
            Ok(None::<()>.to_object(py))
        }
    }
}

create_exception!(pycddl, ValidationError, PyException);

#[pymodule]
fn pycddl(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("ValidationError", py.get_type_bound::<ValidationError>())?;
    m.add_class::<Schema>()?;
    Ok(())
}
