# DeliciousBytes

The `deliciousbytes` library provides a range of data types that can be encoded into and
decoded from their binary forms which is useful when working with data that is stored in
certain file formats or transmitted over networks with certain encodings.

The data types provided by the library all subclass their corresponding native Python
types so can be used interchangeably with those types, while offering additional support
for decoding from and encoding into binary forms according to the specified byte order.

The library provides a range of signed and unsigned integer types of specific lengths,
chars, signed chars, signed and unsigned longs, signed and unsigned long longs, bytes
and string types.

The integer types automatically overflow if the specified value is out of range, for
example if the unsigned 8-bit integer type, `UInt8`, which can hold `255` as its largest
value, is instantiated with a value of `256` it will automatically overflow to `0`, and
if a signed 8-bit integer type, `Int8`, which can hold a minimum value of `-127` and a
maximum value of `128` is instantiated with a value of `129` it will overflow to `-127`.

While many of the built in types offer conversion operations to and from their binary
forms, the library provides a consistent interface across the data types and also offers
the ability to encode and decode bytes and string values with a defined endianness.

### Requirements

The DeliciousBytes library has been tested with Python 3.10, 3.11, 3.12 and 3.13. The
library has not been tested with and is likely incompatible with Python 3.9 and earlier.

### Installation

The DeliciousBytes library is available from PyPI, so may be added to a project's dependencies
via its `requirements.txt` file or similar by referencing the DeliciousBytes library's name,
`deliciousbytes`, or the library may be installed directly into your local runtime environment
using `pip` via the `pip install` command by entering the following into your shell:

	$ pip install deliciousbytes

### Example Usage

To use the DeliciousBytes library, import the library and the data type or data types
you need and use them just like their regular counterparts, and when needed the each
types' `encode()` and `decode()` methods provide support for decoding and encoding the
values to and from their binary representations:

```python
from deliciousbytes import (
    Int, Int8, ByteOrder,
)

value: Int8 = Int8(127)

assert isinstance(value, int)
assert isinstance(value, Int)
assert isinstance(value, Int8)

assert value == 127

encoded: bytes = value.encode(order=ByteOrder.BigEndian)
assert isinstance(encoded, bytes)
assert encoded == b"\x7f"

encoded: bytes = value.encode(order=ByteOrder.LittleEndian)
assert isinstance(encoded, bytes)
assert encoded == b"\x7f"
```

### Classes & Methods

The DeliciousBytes library provides the following data type classes:

| Class            | Description                         | Subclass Of |
|------------------|-------------------------------------|-------------|
| `Int`            | Signed unbounded integer            | `int`       |
| `Int8`           | Signed 8-bit integer                | `Int`       |
| `Int16`          | Signed 16-bit integer               | `Int`       |
| `Int32`          | Signed 32-bit integer               | `Int`       |
| `Int64`          | Signed 64-bit integer               | `Int`       |
| `UInt`           | Unsigned unbounded integer          | `Int`       |
| `UInt8`          | Unsigned 8-bit integer              | `UInt`      |
| `UInt16`         | Unsigned 16-bit integer             | `UInt`      |
| `UInt32`         | Unsigned 32-bit integer             | `UInt`      |
| `UInt64`         | Unsigned 64-bit integer             | `UInt`      |
| `Char`           | Unsigned 8-bit integer              | `UInt8`     |
| `SignedChar`     | Signed 8-bit integer                | `Int8`      |
| `Long`           | Unsigned long (16-bit) integer      | `UInt16`    |
| `SignedLong`     | Signed long (16-bit) integer        | `Int16`     |
| `LongLong`       | Unsigned long long (32-bit) integer | `UInt32`    |
| `SignedLongLong` | Signed long long (32-bit) integer   | `Int32`     |
| `Bytes`          | Unbounded bytes type                | `bytes`     |
| `Bytes8`         | 8-bit bytes type                    | `Bytes`     |
| `Bytes16`        | 16-bit bytes type                   | `Bytes`     |
| `Bytes32`        | 32-bit bytes type                   | `Bytes`     |
| `Bytes64`        | 64-bit bytes type                   | `Bytes`     |
| `Bytes128`       | 128-bit bytes type                  | `Bytes`     |
| `Bytes256`       | 256-bit bytes type                  | `Bytes`     |
| `String`         | Unbounded string type               | `str`       |

The unbounded types have no length/size restrictions on the values that they can hold
beyond those imposed by the Python interpreter in use. The bounded types do impose a
limit on the length/size of the values that they can hold, for example the `UInt8` type
can hold a minimum value of `0` and a maximum value of `255` being an 8-bit unsigned int
value.

As each of the type classes ultimately subclass from one of the native Python data types
the class instances can be used interchangeably with their native Python counterparts.

Each of the data type classes provide the following methods:

 * `encode(order: ByteOrder = ByteOrder.MSB)` (`bytes`) – The `encode()` method provides
support for encoding the value held by the type into its binary representation according
to the byte order defined during the call to the method. The byte order defaults to most
significant bit first, and is represented by the `ByteOrder` enumeration class which
provides enumeration options to specify the endianness that is needed for the use case.
 
 * `decode(value: bytes, order: ByteOrder = ByteOrder.MSB)` (`object`) – The `decode()`
methods on each of the data type classes are class rather than instance methods, so must
be called on the class type rather than on an instance of the class. The method takes a
binary encoded value provided via a `bytes` data type value, and decodes the value into
its native data type value. The byte order defaults to most-significant bit first, and
is represented by the `ByteOrder` enumeration class which provides enumeration options
to specify the endianness that is needed for the use case.

### Byte Order

The byte order for each of the data type classes defaults to most-significant bit first,
MSB, but may be changed to LSB if needed. The `ByteOrder` enumeration class value offers
enumeration options to specify the endianness that is needed for the use case, and for
convenience provides the enumerations in a few flavours depending on how one prefers to
refer to endianness:

| Enumeration Option             | Byte Order |
|--------------------------------|------------|
| `ByteOrder.MSB`                | MSB        |
| `ByteOrder.LSB`                | LSB        |
| `ByteOrder.Motorolla`          | MSB        |
| `ByteOrder.Intel`              | LSB        |
| `ByteOrder.BigEndian`          | MSB        |
| `ByteOrder.LittleEndian`       | LSB        |

### Unit Tests

The DeliciousBytes library includes a suite of comprehensive unit tests which ensure that
the library functionality operates as expected. The unit tests were developed with and are
run via `pytest`.

To ensure that the unit tests are run within a predictable runtime environment where all of the necessary dependencies are available, a [Docker](https://www.docker.com) image is created within which the tests are run. To run the unit tests, ensure Docker and Docker Compose is [installed](https://docs.docker.com/engine/install/), and perform the following commands, which will build the Docker image via `docker compose build` and then run the tests via `docker compose run` – the output of running the tests will be displayed:

```shell
$ docker compose build
$ docker compose run tests
```

To run the unit tests with optional command line arguments being passed to `pytest`, append the relevant arguments to the `docker compose run tests` command, as follows, for example passing `-vv` to enable verbose output:

```shell
$ docker compose run tests -vv
```

See the documentation for [PyTest](https://docs.pytest.org/en/latest/) regarding available optional command line arguments.

### Copyright & License Information

Copyright © 2025 Daniel Sissman; licensed under the MIT License.