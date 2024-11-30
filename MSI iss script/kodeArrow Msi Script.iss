; Inno Setup Script for KodeArrow R-Edition
[Setup]
; Basic installer settings
AppName=KodeArrow
AppVersion=2.0
DefaultDirName=C:\KodeArrow R-Edition
DefaultGroupName=KodeArrow
DisableProgramGroupPage=no
OutputDir=Output
OutputBaseFilename=KodeArrow_2.0_setup
Compression=lzma
SolidCompression=yes
SetupIconFile=P:\KodeArrow-Software\dist\Kodearrow_setup_icon.ico
CreateUninstallRegKey=true

; Publisher and Copyright information (for installer and uninstaller properties)
AppPublisher=Ahmad Hassan
AppPublisherURL=https://bted.wuaze.com/
AppSupportURL=https://bted.wuaze.com/contactMe.html
AppUpdatesURL=https://kodearrow.wuaze.com/
AppCopyright=Copyright © ByTed Technologies 2024

[Files]
; Include your files from the specified directory
Source: "P:\KodeArrow-Software\dist\KodeArrow v2.0\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "P:\KodeArrow-Software\dist\KodeArrow v2.0\KodeArrow.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "P:\KodeArrow-Software\dist\KodeArrow v2.0\Read Me.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create a shortcut for the executable on the desktop
Name: "{commondesktop}\KodeArrow"; Filename: "{app}\KodeArrow.exe"; IconFilename: "{app}\icon.ico"
; Create a shortcut for the Read Me file on the desktop
Name: "{commondesktop}\KodeArrow_Read Me"; Filename: "{app}\Read Me.txt"

[Run]
; Optional: Run the application after installation
Filename: "{app}\KodeArrow.exe"; Description: "Run KodeArrow"; Flags: nowait postinstall skipifsilent

[Code]