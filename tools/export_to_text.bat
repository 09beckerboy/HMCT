@echo off
setlocal enabledelayedexpansion
for /R %%I in (*.EXPORT) do (
    set "source_file=%%~fI"
    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    exporttool.exe -d "!source_file!"
    endlocal
    del "!source_file!"
)
endlocal
