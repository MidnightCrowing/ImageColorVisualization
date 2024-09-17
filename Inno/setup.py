import os
import shutil

# 打包属性设置
NAME = 'ImageColorVisualization'
VERSION = '1.0.0'
PUBLISHER = 'MidnightCrowing'
APP_URL = 'https://www.support@imagecolorviz.com/'
OUTPUT_PATH = 'F:\\'

# region 获取当前脚本的绝对路径
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"当前脚本路径: {script_dir}")
except Exception as e:
    print(f"获取当前脚本路径时发生错误: {e}")
    raise
# endregion

# region 获取必要路径
root_dir = os.path.abspath(os.path.join(script_dir, '..'))  # 根目录路径
dist_path = os.path.abspath(os.path.join(root_dir, 'dist'))  # dist文件夹路径
output_path = os.path.join(dist_path, 'ImageColorVisualization')  # 输出文件夹路径
# endregion

# region 删除旧文件夹
try:
    if os.path.exists(output_path) and os.path.isdir(output_path):
        shutil.rmtree(output_path)
        print(f"旧文件夹 '{output_path}' 已删除。")
    else:
        print(f"旧文件夹 '{output_path}' 不存在。")
except Exception as e:
    print(f"删除旧文件夹时发生错误: {e}")
    raise
# endregion

# region 重命名文件夹
old_folder_path = os.path.join(dist_path, 'main.dist')
try:
    if os.path.exists(old_folder_path) and os.path.isdir(old_folder_path):
        new_folder_path = os.path.join(os.path.dirname(old_folder_path), 'ImageColorVisualization')
        os.rename(old_folder_path, new_folder_path)
        print(f"文件夹已从 '{old_folder_path}' 重命名为 '{new_folder_path}'。")
    else:
        print(f"文件夹 '{old_folder_path}' 不存在。")
except Exception as e:
    print(f"重命名文件夹时发生错误: {e}")
    raise
# endregion

# region 重命名文件
old_file_path = os.path.join(output_path, 'main.exe')
try:
    if os.path.exists(old_file_path) and os.path.isfile(old_file_path):
        new_file_path = os.path.join(os.path.dirname(old_file_path), 'ImageColorVisualization.exe')
        os.rename(old_file_path, new_file_path)
        print(f"文件已从 '{old_file_path}' 重命名为 '{new_file_path}'。")
    else:
        print(f"文件 '{old_file_path}' 不存在。")
except Exception as e:
    print(f"重命名文件时发生错误: {e}")
    raise
# endregion

# region 复制LICENSE
try:
    shutil.copyfile(os.path.join(root_dir, 'LICENSE'), os.path.join(output_path, 'LICENSE'))
    print("LICENSE 已复制。")
except Exception as e:
    print(f"复制LICENSE时发生错误: {e}")
    raise
# endregion

# region 复制图标
try:
    shutil.copyfile(os.path.join(root_dir, 'resource', 'image', 'ImageColorVisualization.ico'),
                    os.path.join(output_path, 'ImageColorVisualization.ico'))
    print("图标已复制。")
except Exception as e:
    print(f"复制图标时发生错误: {e}")
    raise
# endregion

# region 复制源代码
try:
    shutil.copytree(os.path.join(root_dir, 'src'), os.path.join(output_path, 'resource', 'src'))
    shutil.copyfile(os.path.join(root_dir, 'main.py'), os.path.join(output_path, 'resource', 'main.py'))
    print("源代码已复制。")
except Exception as e:
    print(f"复制源代码时发生错误: {e}")
    raise


# endregion

# region 删除 Python 编译文件
def delete_python_compiled_files(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path):
            # 删除 .pyc 文件
            for file in files:
                if file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")

            # 删除 __pycache__ 文件夹
            for dir in dirs:
                if dir == '__pycache__':
                    dir_path = os.path.join(root, dir)
                    shutil.rmtree(dir_path)
                    print(f"已删除文件夹: {dir_path}")
    except Exception as e:
        print(f"删除 Python 编译文件时发生错误: {e}")
        raise


delete_python_compiled_files(os.path.join(output_path, 'resource', 'src'))
print("已删除Python编译文件。")
# endregion

# region 写入inno_setup脚本
inno_template = f'''
; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "{NAME}"
#define MyAppVersion "{VERSION}"
#define MyAppPublisher "{PUBLISHER}"
#define MyAppURL "{APP_URL}"
#define MyAppExeName "ImageColorVisualization.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{{{B26D7B53-F8A5-4927-A660-D7924279050D}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
;AppVerName={{#MyAppName}} {{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName=ImageColorVisualization
; "ArchitecturesAllowed=x64compatible" specifies that Setup cannot run
; on anything but x64 and Windows 11 on Arm.
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" requests that the
; install be done in "64-bit mode" on x64 or Windows 11 on Arm,
; meaning it should use the native 64-bit Program Files directory and
; the 64-bit view of the registry.
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes
DisableDirPage=no
DisableProgramGroupPage=no
LicenseFile={output_path}\\LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir={OUTPUT_PATH}
OutputBaseFilename=ImageColorVisualization
SetupIconFile={output_path}\\ImageColorVisualization.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "armenian"; MessagesFile: "compiler:Languages\\Armenian.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"
Name: "bulgarian"; MessagesFile: "compiler:Languages\\Bulgarian.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\\Catalan.isl"
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\\ChineseSimplified.isl"
Name: "chinesetraditional"; MessagesFile: "compiler:Languages\\ChineseTraditional.isl"
Name: "corsican"; MessagesFile: "compiler:Languages\\Corsican.isl"
Name: "czech"; MessagesFile: "compiler:Languages\\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\\Dutch.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\\Finnish.isl"
Name: "french"; MessagesFile: "compiler:Languages\\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\\German.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\\Hebrew.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\\Hungarian.isl"
Name: "icelandic"; MessagesFile: "compiler:Languages\\Icelandic.isl"
Name: "italian"; MessagesFile: "compiler:Languages\\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\\Japanese.isl"
Name: "korean"; MessagesFile: "compiler:Languages\\Korean.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\\Russian.isl"
Name: "slovak"; MessagesFile: "compiler:Languages\\Slovak.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\\Slovenian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\\Turkish.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\\Ukrainian.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "{output_path}\\{{#MyAppExeName}}"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{output_path}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\\Classes\\{{#MyAppAssocExt}}\\OpenWithProgids"; ValueType: string; ValueName: "{{#MyAppAssocKey}}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\\Classes\\{{#MyAppAssocKey}}"; ValueType: string; ValueName: ""; ValueData: "{{#MyAppAssocName}}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\\Classes\\{{#MyAppAssocKey}}\\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{{app}}\\{{#MyAppExeName}},0"
Root: HKA; Subkey: "Software\\Classes\\{{#MyAppAssocKey}}\\shell\\open\\command"; ValueType: string; ValueName: ""; ValueData: """{{app}}\\{{#MyAppExeName}}"" ""%1"""
Root: HKA; Subkey: "Software\\Classes\\Applications\\{{#MyAppExeName}}\\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{{autoprograms}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

'''

with open('setup.iss', 'w', encoding='utf-8') as file:
    file.write(inno_template)

print("已将inno setup代码写入到 setup.iss 文件中。")
# endregion
