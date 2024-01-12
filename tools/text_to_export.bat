@echo off
setlocal enabledelayedexpansion
for /R %%I in (*.EXPORT.TXT) do (
    set "source_file=%%~fI"
    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    exporttool.exe -c "!source_file!"
    endlocal
    del "!source_file!"
)
endlocal
