@echo off
setlocal enabledelayedexpansion

REM Convert files within the current directory and subfolders
for /R %%I in (*.dds) do (
    set "source_file=%%~fI"
    set "result_file=%%~dpnI.XBMP"
    
    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    xbmpconverter.exe "!source_file!" "!result_file!"
    endlocal

    del "!source_file!"
)

endlocal
