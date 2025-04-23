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

for /R %%I in (*.export) do (
    set "source_file=%%~fI"
    set "res_file=%%~dpnI.exportres"
    
    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    exporttool.exe -json -d "!source_file!"
    endlocal

    del "!res_file!"
)

for /R %%I in (*.rgeom) do (
    set "source_file=%%~fI"
    set "result_file=%%~dpnI.obj"    

    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    rgeom2obj.exe "!source_file!" "!result_file!"
    endlocal

    del "!source_file!"
)

for /R %%I in (*.npcgeom) do (
    set "source_file=%%~fI"
    set "result_file=%%~dpnI.dds"    

    setlocal enabledelayedexpansion
    echo Converting: "!source_file!"
    rgeom2obj.exe "!source_file!" "!result_file!"
    endlocal

    del "!source_file!"
)

endlocal
