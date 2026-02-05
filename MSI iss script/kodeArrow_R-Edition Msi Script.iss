; Inno Setup Script for KodeArrow R-Edition
[Setup]
; Basic installer settings
AppName=KodeArrow R-Edition
AppVersion=2.0
DefaultDirName={commonappdata}\KodeArrow R-Edition
DefaultGroupName=KodeArrow R-Edition
DisableProgramGroupPage=no
OutputDir=Output
OutputBaseFilename=KodeArrow_R-Edition_2.0_setup
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
Source: "P:\KodeArrow-Software\dist\KodeArrow R-Edition v2.0\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "P:\KodeArrow-Software\dist\KodeArrow R-Edition v2.0\KodeArrow R-Edition.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "P:\KodeArrow-Software\dist\KodeArrow R-Edition v2.0\Read Me.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create a shortcut for the executable on the desktop
Name: "{commondesktop}\KodeArrow R-Edition"; Filename: "{app}\KodeArrow R-Edition.exe"; IconFilename: "{app}\icon.ico"
; Create a shortcut for the Read Me file on the desktop
Name: "{commondesktop}\KodeArrow R-Edition_Read Me"; Filename: "{app}\Read Me.txt"

[Run]
; Optional: Run the application after installation
Filename: "{app}\KodeArrow R-Edition.exe"; Description: "Run KodeArrow R-Edition"; Flags: nowait postinstall skipifsilent
