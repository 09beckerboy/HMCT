@echo off
setlocal enabledelayedexpansion

for /R %%I in (*.AUDIOPKG) do (
    set "file=%%~fI"
    del !file!
)

endlocal