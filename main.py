from ApplicationChecker import RegistryChecker
import winreg

def start_program():
    reg_check = RegistryChecker(hkey=winreg.HKEY_LOCAL_MACHINE,
                            keypath=r"SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
    app_version = reg_check.get_applications_version()
    for key, value in sorted(app_version.items()):
        print(key, '~', value)

if __name__ == "__main__":
    start_program()