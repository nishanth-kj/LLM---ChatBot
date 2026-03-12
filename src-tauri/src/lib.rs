#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .plugin(tauri_plugin_shell::init())
    .setup(|app| {
      use tauri_plugin_shell::ShellExt;

      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }

      // Spawn the backend API sidecar attached to this process
      let sidecar_command = app.shell().sidecar("backend-api")
          .expect("Failed to create sidecar command");
      let (_rx, mut _child) = sidecar_command
          .spawn()
          .expect("Failed to spawn sidecar");

      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
