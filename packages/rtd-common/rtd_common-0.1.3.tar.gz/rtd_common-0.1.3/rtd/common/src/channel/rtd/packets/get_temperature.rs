use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct GetTemperatureRequest {}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct GetTemperatureResponse {
    pub temperature: f32,
}

#[cfg(all(feature = "pyo3", not(feature = "std")))]
use alloc::vec::Vec;
#[cfg(all(feature = "pyo3", feature = "std"))]
use std::vec::Vec;

#[cfg(feature = "pyo3")]
#[pyfunction]
#[pyo3(name = "get_temperature_request")]
pub fn get_temperature_py(c_number: usize, id: u32) -> Vec<u8> {
    hal_common::packets::Request::with_id(
        crate::channel::packets::Request::Impl(
            crate::channel::rtd::packets::Request::GetTemperature(
                GetTemperatureRequest {},
            ),
        ),
        id,
    )
    .into(c_number as u8)
    .as_bytes()
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "get_temperature").map(|module| {
        Ok(module)
    })?
}