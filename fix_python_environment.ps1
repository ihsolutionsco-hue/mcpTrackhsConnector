# Script para solucionar el error "Could not find platform independent libraries <prefix>"
# Este script configura las variables de entorno de Python correctamente

Write-Host "Configurando variables de entorno de Python..." -ForegroundColor Green

# Configurar PYTHONHOME
$pythonHome = "C:\Users\EQUIPO\AppData\Local\Programs\Python\Python313"
[Environment]::SetEnvironmentVariable("PYTHONHOME", $pythonHome, "User")

# Configurar PYTHONPATH
$pythonPath = "C:\Users\EQUIPO\AppData\Local\Programs\Python\Python313\Lib;C:\Users\EQUIPO\AppData\Local\Programs\Python\Python313\Lib\site-packages"
[Environment]::SetEnvironmentVariable("PYTHONPATH", $pythonPath, "User")

# Configurar variables para la sesión actual
$env:PYTHONHOME = $pythonHome
$env:PYTHONPATH = $pythonPath

Write-Host "Variables de entorno configuradas:" -ForegroundColor Yellow
Write-Host "PYTHONHOME: $pythonHome" -ForegroundColor Cyan
Write-Host "PYTHONPATH: $pythonPath" -ForegroundColor Cyan

Write-Host "`nProbando Python..." -ForegroundColor Green
python -c "import sys; print('Python funciona correctamente!'); print('Python executable:', sys.executable)"

Write-Host "`n¡Problema solucionado! Las variables de entorno se han configurado permanentemente." -ForegroundColor Green
Write-Host "Reinicia tu terminal o PowerShell para que los cambios surtan efecto." -ForegroundColor Yellow
