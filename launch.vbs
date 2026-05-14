Set sh = CreateObject("WScript.Shell")
sh.Run "pythonw.exe """ & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\src\main.py""", 0, False
