#!/usr/bin/python3
#----------------------------------------------------------------------------------
# Скрипт для получение данных о параметре из билда, его значении и ссылки на билд.
# Выполнение поиска по конкретному значению параметра
# Получение всех значений, кроме.
#----------------------------------------------------------------------------------
import requests
import xmltodict
from getpass import getpass

base_url = "Your url"
username = input("username: ")
password = getpass("password: ")
parameter_name = input("parameter name: ")

# Показывает только конкретное значение параметра.
user_input = input("Show specific parameter values? y/n? ").lower()
if user_input == 'y':
    specific_param = input("Enter a specific parameter value: ")

# Показывает все значения параметра, кроме конкретного
exclude_input = None
if user_input != 'y':
    exclude_input = input("Exclude a specific parameter value? (yes/no): ").lower()
    if exclude_input == 'y':
        exclude_specific_param = input("Enter a specific parameter value to exclude: ")
    else:
        exclude_specific_param = None


response = requests.get(base_url, auth=(username, password))

if response.status_code == 200:
    try:
        xml_dict = xmltodict.parse(response.text)
        build_types = xml_dict['buildTypes']['buildType']

        for build_type in build_types:
            build_id = build_type['@id']
            url = f"{base_url}/id:{build_id}/parameters/{parameter_name}"

            response_build = requests.get(url, auth=(username, password))

            if response_build.status_code == 200:
                xml_dict_build = xmltodict.parse(response_build.text)

                if 'property' in xml_dict_build and '@name' in xml_dict_build['property'] and xml_dict_build['property']['@name'] == parameter_name:
                    param_value = xml_dict_build['property']['@value']

                    # Выводим все значения param_value, если user_input = 'n'
                    if user_input == 'n' and exclude_input == 'n':
                        print(f"Build ID: {build_id}")
                        print(f"Parameter Name: {parameter_name}")
                        print(f"Parameter Value: {param_value}")
                        # Используем get для извлечения webUrl
                        web_url = build_type.get('@webUrl', 'N/A')
                        print(f"Web URL: {web_url}")

                        print("-" * 50)
                    # Выводим значения только при совпадении с specific_param, и если user_input = 'y'
                    elif user_input == 'y' and param_value == specific_param:
                        print(f"Build ID: {build_id}")
                        print(f"Parameter Name: {parameter_name}")
                        print(f"Parameter Value: {param_value}")
                        web_url = build_type.get('@webUrl', 'N/A')
                        print(f"Web URL: {web_url}")

                        print("-" * 50)
                    # Выводим все значения, кроме конкретного, если user_input = 'y' и exclude_specific_param = 'y'
                    elif exclude_input == 'y' and exclude_specific_param is not None and param_value != exclude_specific_param:
                        print(f"Build ID: {build_id}")
                        print(f"Parameter Name: {parameter_name}")
                        print(f"Parameter Value: {param_value}")
                        web_url = build_type.get('@webUrl', 'N/A')
                        print(f"Web URL: {web_url}")

                        print("-" * 50)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

