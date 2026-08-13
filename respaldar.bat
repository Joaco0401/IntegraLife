@echo off
set PGBIN=C:\Program Files\PostgreSQL\18\bin
set CARPETA=C:\Users\joaqu\proyectopapa\respaldos
set BD=proyectopapa
set USUARIO=postgres
set PGPASSWORD=Pepe11

if not exist "%CARPETA%" mkdir "%CARPETA%"

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set FECHA=%%a
set STAMP=%FECHA:~0,4%-%FECHA:~4,2%-%FECHA:~6,2%_%FECHA:~8,2%%FECHA:~10,2%
set ARCHIVO=%CARPETA%\respaldo_%STAMP%.sql

echo Respaldando la base de datos...
"%PGBIN%\pg_dump.exe" -U %USUARIO% -d %BD% -f "%ARCHIVO%"

if %errorlevel%==0 (
    echo Respaldo creado: %ARCHIVO%
) else (
    echo ERROR: no se pudo crear el respaldo.
)

forfiles /p "%CARPETA%" /m respaldo_*.sql /d -30 /c "cmd /c del @path" 2>nul

echo.
dir /b "%CARPETA%\*.sql"