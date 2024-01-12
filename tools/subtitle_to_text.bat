@echo off
setlocal enabledelayedexpansion
for /R %%I in (*.BIN) do (
    set "source_file=%%~fI"
    if "!source_file!"=="!source_file:CLUTTER=!" (
        setlocal enabledelayedexpansion
        echo Converting: "!source_file!"
        subtitletool.exe -d "!source_file!"
        endlocal
        del "!source_file!"
    )
)
endlocal
