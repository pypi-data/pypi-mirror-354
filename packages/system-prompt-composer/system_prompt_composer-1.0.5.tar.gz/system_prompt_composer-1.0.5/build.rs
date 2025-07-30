fn main() {
    // Only build NAPI bindings when the nodejs feature is enabled
    #[cfg(feature = "nodejs")]
    {
        napi_build::setup();
    }
}
