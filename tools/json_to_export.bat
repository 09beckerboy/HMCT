@echo off
setlocal enabledelayedexpansion
for /R %%I in (*.EXPORT.json) do (
    set "source_file=%%~fI"
    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    exporttool.exe -json -c "!source_file!"
    endlocal
    del "!source_file!"
)
endlocal
