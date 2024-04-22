rem \---- Repo location
set REPO_PATH=%~dp0

REM \---- Env Type
set CURRENT_ENV=dev

rem \---- Virtual env site-packages
set SITE_PACKAGES=%REPO_PATH%sitepackages

rem \---- Python Tools Root
set PYTHONROOT=%REPO_PATH%src\tools

rem \---- MEL root
set MAYA_SCRIPT_PATH=%REPO_PATH%src\mel

rem \---- Repository path
set CORE_REPO=%PYTHONROOT%\Core

rem \---- Icon Path
set XBMLANGPATH=%CORE_REPO%\icons

rem \---- Plugin path
rem \---- set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%VRAY_PLUGINS%

set MAYA_RENDER_SETUP_INCLUDE_ALL_LIGHTS=0

rem \---- Python paths
set PYTHONPATH=%REPO_PATH%;%PYTHONROOT%;%SITE_PACKAGES%

rem \---- Disable Autodesk Telemetry
set MAYA_DISABLE_ADP=1

set DCC_FOLDER="%~dp0"
set MAYA_PROJECT="%DCC_FOLDER%CG"

for %%I in ("%~dp0..") do (
    set "parent_dir=%%~fI"
    set "MAYA_PROJECT=%%~fI\CG"
)

rem \---- Start Maya - Leaves a cmd prompt window open. Feel free to close.
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\Maya\2025\Setup\InstallPath" /v MAYA_INSTALL_LOCATION') do set "MAYA_LOCATION=%%~b"
"%MAYA_LOCATION%\bin\maya.exe" %*

exit 0