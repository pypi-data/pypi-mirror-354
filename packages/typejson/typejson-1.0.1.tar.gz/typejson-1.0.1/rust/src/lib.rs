use pyo3::prelude::*;
use pyo3::types::{PyAny, PyBool, PyDict, PyFloat, PyInt, PyList, PyString};
use pyo3::exceptions::PyRecursionError;


fn _is_int_or_float(obj: &Bound<'_, PyAny>) -> bool {
    obj.is_instance_of::<PyInt>() || obj.is_instance_of::<PyFloat>()
}

fn _is_str(obj: &Bound<'_, PyAny>) -> bool {
    obj.is_instance_of::<PyString>()
}

fn _is_bool(obj: &Bound<'_, PyAny>) -> bool {
    obj.is_instance_of::<PyBool>()
}

fn _is_number(obj: &Bound<'_, PyAny>) -> bool {
    _is_int_or_float(obj) && !_is_bool(obj)
}

fn _is_scalar(obj: &Bound<'_, PyAny>) -> bool {
    _is_int_or_float(obj) || _is_str(obj) || obj.is_none()
}

fn _is_array(obj: &Bound<'_, PyAny>) -> bool {
    obj.is_instance_of::<PyList>()
}

fn _is_object(obj: &Bound<'_, PyAny>) -> bool {
    obj.is_instance_of::<PyDict>()
}

fn _is_document(obj: &Bound<'_, PyAny>) -> bool {
    _is_array(obj) || _is_object(obj)
}

fn _is_json(obj: &Bound<'_, PyAny>) -> bool {
    _is_scalar(obj) || _is_array(obj) || _is_object(obj)
}

fn _is_array_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_array(obj) && _is_json_deep(py, obj)?)
}

fn _is_object_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_object(obj) && _is_json_deep(py, obj)?)
}

fn _is_document_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_document(obj) && _is_json_deep(py, obj)?)
}

fn _is_json_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    if _is_scalar(obj) {
        return Ok(true);
    }
    let sys = py.import("sys")?;
    let limit: usize = sys.getattr("getrecursionlimit")?.call0()?.extract()?;
    _is_json_deep_rec(py, obj, 0, limit)
}

fn _is_json_deep_rec(py: Python<'_>, obj: &Bound<'_, PyAny>, depth: usize, limit: usize) -> PyResult<bool> {
    if _is_scalar(obj) {
        return Ok(true);
    }

    if depth > limit {
        return Err(PyRecursionError::new_err("maximum recursion depth exceeded"));
    }

    if let Ok(list) = obj.downcast::<PyList>() {
        for element in list.iter() {
            if !_is_json_deep_rec(py, &element, depth + 1, limit)? {
                return Ok(false);
            }
        }
        return Ok(true);
    }

    if let Ok(dict) = obj.downcast::<PyDict>() {
        for (key, val) in dict.iter() {
            if !key.is_instance_of::<PyString>() || !_is_json_deep_rec(py, &val, depth + 1, limit)? {
                return Ok(false);
            }
        }
        return Ok(true);
    }

    Ok(false)
}


// Is (not deep)

#[pyfunction]
fn is_json_number(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_number(obj))
}

#[pyfunction]
fn is_json_scalar(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_scalar(obj))
}

#[pyfunction]
fn is_json_array(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_array(obj))
}

#[pyfunction]
fn is_json_object(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_object(obj))
}

#[pyfunction]
fn is_json_document(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_document(obj))
}

#[pyfunction]
fn is_json(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_json(obj))
}

// Guard (not deep)

#[pyfunction]
fn guard_json_number(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_number(obj))
}

#[pyfunction]
fn guard_json_scalar(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_scalar(obj))
}

#[pyfunction]
fn guard_json_array(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_array(obj))
}

#[pyfunction]
fn guard_json_object(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_object(obj))
}

#[pyfunction]
fn guard_json_document(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_document(obj))
}

#[pyfunction]
fn guard_json(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    Ok(_is_json(obj))
}

// Is (deep)

#[pyfunction]
fn is_json_array_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_array_deep(py, obj)
}

#[pyfunction]
fn is_json_object_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_object_deep(py, obj)
}

#[pyfunction]
fn is_json_document_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_document_deep(py, obj)
}

#[pyfunction]
fn is_json_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_json_deep(py, obj)
}

// Guard (deep)

#[pyfunction]
fn guard_json_array_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_array_deep(py, obj)
}

#[pyfunction]
fn guard_json_object_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_object_deep(py, obj)
}

#[pyfunction]
fn guard_json_document_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_document_deep(py, obj)
}

#[pyfunction]
fn guard_json_deep(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    _is_json_deep(py, obj)
}

#[pymodule]
fn _rust(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_json_number, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_array, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_object, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_document, m)?)?;
    m.add_function(wrap_pyfunction!(is_json, m)?)?;

    m.add_function(wrap_pyfunction!(guard_json_number, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_array, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_object, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_document, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json, m)?)?;

    m.add_function(wrap_pyfunction!(is_json_array_deep, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_object_deep, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_document_deep, m)?)?;
    m.add_function(wrap_pyfunction!(is_json_deep, m)?)?;

    m.add_function(wrap_pyfunction!(guard_json_array_deep, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_object_deep, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_document_deep, m)?)?;
    m.add_function(wrap_pyfunction!(guard_json_deep, m)?)?;
    Ok(())
}
