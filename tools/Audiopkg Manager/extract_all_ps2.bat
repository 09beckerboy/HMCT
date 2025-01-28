@echo off
setlocal enabledelayedexpansion

for /R %%I in (*.AUDIOPKG) do (
    set "file=%%~fI"
    set "file_path=%%~dpI"
    echo !file_path!
    set "folder=%%~dpnI"
    setlocal enabledelayedexpansion
    audiopkg.exe -t "!file!"
    mkdir "!folder!"
    endlocal
    for %%O in ("!file_path!\*.wav") do (
        echo "%%~dpnxO" "!folder!\%%~nxO"
        move "%%~dpnxO" "!folder!\%%~nxO"
    )
)

endlocal
