@echo off
setlocal enabledelayedexpansion

for /R %%I in (*.audioscript) do (
    set "file=%%~fI"
    del !file!
)

endlocal