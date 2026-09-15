Set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get Desktop path
desktop = WshShell.SpecialFolders("Desktop")

' Create shortcut
Set shortcut = WshShell.CreateShortcut(desktop & "\LIGHT STREAM SWITCH.lnk")
shortcut.TargetPath = fso.GetParentFolderName(WScript.ScriptFullName) & "\StreamSwitch.exe"
shortcut.WorkingDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
shortcut.Description = "LIGHT STREAM SWITCH"
shortcut.WindowStyle = 1
shortcut.Save

WScript.Echo "Desktop shortcut created: " & desktop & "\LIGHT STREAM SWITCH.lnk"
