@echo off
setlocal enabledelayedexpansion
for /R %%I in (*.TXT) do (
    set "source_file=%%~fI"
    if "!source_file!"=="!source_file:EXPORT=!" if "!source_file!"=="!source_file:INITIAL=!" if "!source_file!"=="!source_file:LAYER=!" if "!source_file!"=="!source_file:SUMMARY=!" (
        setlocal enabledelayedexpansion
        echo Converting: "!source_file!"
        subtitletool.exe -c "!source_file!"
        endlocal
        del "!source_file!"
    )
)
endlocal
