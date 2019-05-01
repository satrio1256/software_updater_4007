import winreg
import csv
from packaging import version

class RegistryChecker:
    def __init__(self, hkey, keypath):
        self.keypath = keypath
        self.hkey = hkey

    def __get_subkeys(self, key):
        i = 0
        while True:
            try:
                subkey = winreg.EnumKey(key, i)
                yield subkey
                i += 1
            except OSError:
                break

    def __get_enumVal(self, subKey):
        i = 0
        while True:
            try:
                value = winreg.EnumValue(subKey, i)
                yield value
                i += 1
            except OSError:
                break

    def __get_val(self, key):
        i = 0
        values = dict ()
        for subkeyName in self.__get_subkeys(key):
            try:
                valueName = r'\\'.join([self.keypath, subkeyName])
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, valueName, 0, winreg.KEY_READ) as subkey:
                    for val in self.__get_enumVal(subkey):
                        values[val[0]] = val[1]
                    yield (valueName, values)
            except OSError:
                break

    def get_applications_version(self, tabs=0):
        print("Checking Installed App Version...")
        print()
        registry_dict = {}
        key = winreg.OpenKey(self.hkey, self.keypath, 0, winreg.KEY_READ)
        for value in self.__get_val(key):
            registry_dict[value[1]['DisplayName']] = value[1]['DisplayVersion']
        return registry_dict

class VersionComparator:
    def __init__(self, definitions_dir):
        self.definitions = []
        with open(definitions_dir, newline='\n') as csvfile:
            definitions = csv.reader(csvfile, delimiter=',', quotechar="'")
            for definition in definitions:
                self.definitions.append(definition)
        self.definitions.remove(self.definitions[0])

    def compare_version(self, apps_list):
        need_update = []
        for app in self.definitions:
            for installed_app in apps_list:
                if str.lower(app[0]) in str.lower(installed_app[0]):
                    if version.parse(app[1]) > version.parse(installed_app[1]):
                        need_update.append([installed_app[0], installed_app[1], app[1], app[2]])
        return need_update
