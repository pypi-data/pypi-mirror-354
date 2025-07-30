"""
Tests for CBOR decoding functionality.
"""

import math

from pycddl import Schema
from hypothesis import given, strategies as st, settings
import cbor2

ANY_SCHEMA = Schema("main = any")

PRIMITIVES = (
    st.none()
    | st.booleans()
    | st.floats(allow_nan=False)
    | st.text()
    | st.integers(max_value=2**63, min_value=-(2**63))
    | st.binary()
)


@given(
    structure=st.recursive(
        PRIMITIVES,
        lambda values: st.lists(values) | st.dictionaries(PRIMITIVES, values),
        max_leaves=10,
    )
)
@settings(max_examples=2_000)
def test_roundtrip_basic_decoding(structure):
    """
    Basic serialized structures can be deserialized by pycddl.
    """
    serialized = cbor2.dumps(structure)
    deserialized = ANY_SCHEMA.validate_cbor(serialized, True)
    assert structure == deserialized


def test_decoding_is_optional():
    """
    If ``validate_cbor`` isn't told to, it doesn't deserialize the CBOR.
    """
    serialized = cbor2.dumps({1: 2})
    assert ANY_SCHEMA.validate_cbor(serialized, False) is None
    assert ANY_SCHEMA.validate_cbor(serialized) is None


def test_nan():
    """
    Floating point nan is decoded correctly.
    """
    serialized = cbor2.dumps(math.nan)
    result = ANY_SCHEMA.validate_cbor(serialized, True)
    assert math.isnan(result)


def test_sets():
    """
    Sets can be decoded.
    """
    structure = {1, b"abc", "def", 2.3}
    serialized = cbor2.dumps(structure)
    result = ANY_SCHEMA.validate_cbor(serialized, True)
    assert result == structure


@given(data=st.binary(max_size=10_000_000))
def test_large_bytes(data):
    """
    Deserialization of large bytes.
    """
    serialized = cbor2.dumps(data)
    assert ANY_SCHEMA.validate_cbor(serialized, True) == data
