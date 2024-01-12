@echo off
setlocal enabledelayedexpansion
for /R %%I in (*.xbmp) do (
    set "source_file=%%~fI"
    set "result_file=%%~dpnI.dds"
    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    xbmpconverter.exe "!source_file!" "!result_file!"
    endlocal
    del "!source_file!"
)
endlocal
