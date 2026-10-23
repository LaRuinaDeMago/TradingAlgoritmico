# Crea (o reemplaza) una tarea programada de Windows del usuario actual que ejecuta un comando con cmd /c.
# Uso: tarea_b22.ps1 -Nombre X -Comando "..." -Carpeta C:\... [-AlIniciarSesion]
param([string]$Nombre, [string]$Comando, [string]$Carpeta, [switch]$AlIniciarSesion)
$accion = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$Comando`"" -WorkingDirectory $Carpeta
$ajustes = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Days 3) -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -Priority 6 -StartWhenAvailable
$quien = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
$args = @{TaskName=$Nombre; Action=$accion; Settings=$ajustes; Principal=$quien; Force=$true;
          Description='Laboratorio B22 (transcripcion del curso). Se borra al terminar la tanda.'}
if ($AlIniciarSesion) { $args.Trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME" }
Register-ScheduledTask @args | Out-Null
Start-ScheduledTask -TaskName $Nombre
Get-ScheduledTask -TaskName $Nombre | Select-Object TaskName, State
