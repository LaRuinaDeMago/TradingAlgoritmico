# B22: cambia la tarea LAB_B22_transcripcion para que transcriba el curso entero (BONUS 2025 y después el resto) y se
# relance cada hora (una sola instancia: si ya corre, la repetición se ignora). No toca la ejecución en curso
# (ensayado el 2026-10-23: Set-ScheduledTask sobre una tarea en marcha no la para). Uso: powershell -File este.ps1
$d = 'C:\Users\SERVILAB\Documents\LAB_PRIVADO_CURSO'
$py = (Get-Command python).Source
$cmd = "`"$py`" -I herramientas\b22_tanda_bonus.py 1>> b22_salida_6.txt 2>> b22_errores_6.txt & " +
       "`"$py`" -I herramientas\b22_tanda_resto.py 1>> b22_salida_6.txt 2>> b22_errores_6.txt"
$accion = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$cmd`"" -WorkingDirectory $d
$cadaHora = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(60) -RepetitionInterval (New-TimeSpan -Hours 1) `
  -RepetitionDuration (New-TimeSpan -Days 30)
$alEntrar = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
Set-ScheduledTask -TaskName 'LAB_B22_transcripcion' -Action $accion -Trigger @($alEntrar, $cadaHora) | Out-Null
$t = Get-ScheduledTask -TaskName 'LAB_B22_transcripcion'
$t | Select-Object TaskName, State
$t.Actions | Select-Object Arguments
$t.Triggers | Select-Object @{n = 'tipo'; e = { $_.CimClass.CimClassName } }, StartBoundary, @{n = 'cada'; e = { $_.Repetition.Interval } }
$t.Settings | Select-Object MultipleInstances, ExecutionTimeLimit
