# Fixed: "Input watch path is neither a file nor a directory"

## Issue
Tauri was trying to watch a path that doesn't exist, causing the error.

## Fixes Applied

1. ✅ Created `dist` directory in parent folder
2. ✅ Removed invalid `withGlobalTauri` option from config
3. ✅ Changed `devPath` to `devUrl` (correct for Tauri 1.5)
4. ✅ Added config file in `src-tauri/` directory (Tauri looks there first)
5. ✅ Updated Vite config to output to correct dist directory

## Try Again

```bash
npm run tauri dev
```

The app should now start correctly!
