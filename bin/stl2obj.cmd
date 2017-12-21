@ECHO OFF

SET ScriptDir=%~dp0
SET ScriptDir=%ScriptDir:~0,-1%

PYTHON "%ScriptDir%\stl2obj.py" %*
