[Setup]
AppName=Sombra Cacau
AppVersion=1.0
AppPublisher=Jamile Castro
DefaultDirName={autopf}\SombraCacau
DefaultGroupName=Sombra Cacau
OutputDir=instalador
OutputBaseFilename=SombraCacau_Instalador
SetupIconFile=icone_sombra_cacau.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "dist\SombraCacau\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos adicionais:"

[Icons]
Name: "{group}\Sombra Cacau"; Filename: "{app}\SombraCacau.exe"
Name: "{group}\Desinstalar Sombra Cacau"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Sombra Cacau"; Filename: "{app}\SombraCacau.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\SombraCacau.exe"; Description: "Abrir Sombra Cacau"; Flags: nowait postinstall skipifsilent