import ApplicationChecker as ac
from Network import Client_Network
from CMDCommunicator import Commander
import winreg

def start_program():
    # Check existing program
    reg_check = ac.RegistryChecker(hkey=winreg.HKEY_LOCAL_MACHINE,
                            keypath=r"SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
    app_version = reg_check.get_applications_version()
    installed_apps = []
    for key, value in sorted(app_version.items()):
        installed_apps.append([key, value])
        # print(key, '~', value)
    # Existing program check end

    # Get Definitions from Server
    client_net = Client_Network('127.0.0.1', 7000)
    client_net.connect()
    client_net.download_latest_app_definition()
    # Get Definitions from Server end

    # Do comparison
    vc = ac.VersionComparator("ClientFiles/LatestVersion_on_server.csv")
    app_to_update = vc.compare_version(installed_apps)

    # Confirm Update
    cmd = Commander()
    if len(app_to_update) == 0:
        print("All application is up-to-date")
    else:
        for row in app_to_update:
            print()
            print("Latest version for program named", row[0], "found.")
            print("Do you want to install download the latest update? ("+row[1]+") -> ("+row[2]+")")
            print("(y/n)", end=' ')
            x = input()
            if str.lower('y') in str.lower(x):
                client_net = Client_Network('127.0.0.1', 7000)
                client_net.request_package(row[3])
                cmd.run_command(command="start ClientFiles/Executables/" + row[3], shell=True)
            else:
                continue
        print("Update Completed")

if __name__ == "__main__":
    start_program()
