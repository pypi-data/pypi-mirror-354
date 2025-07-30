use password_auth;
use pyo3::prelude::*;

#[derive(FromPyObject)]
enum StrOrBytes {
    Str(String),
    Bytes(Vec<u8>),
}

#[pyfunction]
fn generate_hash(password: StrOrBytes) -> String {
    match password {
        StrOrBytes::Str(s) => password_auth::generate_hash(&s),
        StrOrBytes::Bytes(b) => password_auth::generate_hash(&b),
    }
}

#[pyfunction]
fn verify_password(password: StrOrBytes, hash: String) -> bool {
    let result = match password {
        StrOrBytes::Str(s) => password_auth::verify_password(&s, &hash),
        StrOrBytes::Bytes(b) => password_auth::verify_password(&b, &hash),
    };
    result.is_ok()
}

fn get_version() -> PyResult<String> {
    Python::with_gil(|py| {
        let metadata = PyModule::import(py, "importlib.metadata")?;
        let version = metadata.getattr("version")?.call1(("passuth",))?;
        Ok(version.extract()?)
    })
}

#[pymodule(gil_used = false)]
fn passuth(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let version = get_version().unwrap_or_else(|_| "unknown".to_string());
    m.add("__version__", version)?;
    m.add_function(wrap_pyfunction!(generate_hash, m)?)?;
    m.add_function(wrap_pyfunction!(verify_password, m)?)?;
    Ok(())
}
