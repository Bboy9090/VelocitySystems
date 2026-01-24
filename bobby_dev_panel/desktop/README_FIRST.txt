╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         BOBBY DEV PANEL - DESKTOP APPLICATION               ║
║                    Pandora Codex                             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📍 WHERE AM I?

   You are in: bobby_dev_panel/desktop/
   
   Full path:
   C:\Users\Bobby\Documents\Velocity_Systems_FULL_Masterclass_Repo\
   bobby_dev_panel\desktop\

═══════════════════════════════════════════════════════════════

🚀 TO OPEN THE APP:

   WINDOWS (EASIEST):
   
   → Double-click: LAUNCH_APP.bat
   
   That's it! The app will open automatically.

═══════════════════════════════════════════════════════════════

📋 WHAT THE LAUNCHER DOES:

   1. Checks if Node.js is installed
   2. Checks if Rust is installed
   3. Installs dependencies (first time only)
   4. Starts the desktop app
   5. Opens the app window

═══════════════════════════════════════════════════════════════

⚠️ FIRST TIME REQUIREMENTS:

   Before the app can run, you need:
   
   ✓ Node.js v18+     → https://nodejs.org/
   ✓ Rust (cargo)     → https://rustup.rs/
   ✓ Python 3.8+      → Usually already installed
   ✓ ADB              → For Android devices
   
   The launcher will tell you what's missing!

═══════════════════════════════════════════════════════════════

⏱️ FIRST RUN TIMES:

   - npm install:        2-5 minutes
   - Rust compilation:    5-10 minutes (first time only)
   - App startup:        < 30 seconds
   
   Subsequent runs are much faster!

═══════════════════════════════════════════════════════════════

💻 MANUAL START (If launcher doesn't work):

   1. Open Command Prompt or PowerShell
   
   2. Navigate here:
      cd "C:\Users\Bobby\Documents\Velocity_Systems_FULL_Masterclass_Repo\bobby_dev_panel\desktop"
   
   3. Install dependencies:
      npm install
   
   4. Run the app:
      npm run tauri dev

═══════════════════════════════════════════════════════════════

📦 BUILD INSTALLABLE APP:

   After first run, create installer:
   
   npm run tauri build
   
   Installer location:
   src-tauri/target/release/bundle/msi/
   Bobby Dev Panel_1.0.0_x64_en-US.msi

═══════════════════════════════════════════════════════════════

🎯 WHAT YOU'LL SEE:

   When the app opens:
   
   • Sidebar on left (navigation)
   • Status bar at top (connection status)
   • Main area (dashboard or device list)
   • Dark theme with neon green accents
   • Professional enterprise UI

═══════════════════════════════════════════════════════════════

❓ NEED HELP?

   See: START_HERE.md for detailed instructions
   See: README.md for full documentation
   See: BUILD_INSTRUCTIONS.md for build details

═══════════════════════════════════════════════════════════════
