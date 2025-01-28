@echo off
setlocal enabledelayedexpansion

for /R %%I in (*.audioscript) do (
    set "file=%%~fI"
    echo !file!
    SoundPackager -pc -v -clean !file!
)

endlocal
