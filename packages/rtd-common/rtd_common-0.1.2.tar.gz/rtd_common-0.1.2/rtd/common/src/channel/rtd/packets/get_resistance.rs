use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct GetResistanceRequest {}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct GetResistanceResponse {
    pub resistance: f32,
}

#[cfg(all(feature = "pyo3", not(feature = "std")))]
use alloc::vec::Vec;
#[cfg(all(feature = "pyo3", feature = "std"))]
use std::vec::Vec;

#[cfg(feature = "pyo3")]
#[pyfunction]
#[pyo3(name = "get_resistance_request")]
pub fn get_resistance_py(c_number: usize, id: u32) -> Vec<u8> {
    hal_common::packets::Request::with_id(
        crate::channel::packets::Request::Impl(
            crate::channel::rtd::packets::Request::GetResistance(
                GetResistanceRequest {},
            ),
        ),
        id,
    )
    .into(c_number as u8)
    .as_bytes()
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "get_resistance").map(|module| {
        Ok(module)
    })?
}