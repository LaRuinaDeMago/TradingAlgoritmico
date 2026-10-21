@echo off
rem Prueba del lanzador en su sitio (A10): con una clave FALSA, claude_lab.cmd debe quitarla y arrancar Claude.
set "ANTHROPIC_API_KEY=CLAVE_FALSA_DE_PRUEBA"
call "%~dp0..\..\claude_lab.cmd" --version
