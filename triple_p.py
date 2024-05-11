
import os
import threading
import time
from threading import Semaphore
import requests
from requests import Response
import json
from cryptography.fernet import Fernet
import concurrent.futures
import shlex


SECRET_KEY = b'IAjsTPAtdtJTaa8cY3dYROV2TtLwP4kFn0EB_NgL6RY='
base_url = "http://localhost:3000/"


class ConsoleColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    RESET = '\033[0m'

class Auth:
    name: str = None
    email: str = None
    token: str = None

    @staticmethod
    def signup(name, email, password):
        url = base_url + 'auth/register-with-email'
        response = requests.post(
            url,
            json={"name": name, "email": email, "password": password}
        )

        if response.status_code == 200:
            body = response.json()
            Auth.name = name
            Auth.email = email
            Auth.token = body["token"]

            with open("login-data.json", 'w') as login_data:
                login_data.write(json.dumps(body))
            # print(body)
            return True
        else:
            print("Failed to signup")
            return False

    @staticmethod
    def login(email, password):
        url = base_url + 'auth/login-with-email'
        response: Response = requests.post(
            url,
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            body = response.json()
            Auth.name = body["name"]
            Auth.email = email
            Auth.token = body["token"]

            with open("login-data.json", 'w') as login_data:
                login_data.write(json.dumps(body))

            return True
        else:
            print("Failed to login")
            return False

    @staticmethod
    def auto_login():
        if not os.path.exists("login-data.json"):
            return False

        with open("login-data.json", 'r') as login_data:
            login = json.loads(login_data.read())
            Auth.name = login["name"]
            Auth.email = login["email"]
            Auth.token = login["token"]
        return True

    @staticmethod
    def logout():
        os.remove("login-data.json")
        Auth.name = None
        Auth.email = None
        Auth.token = None


class FileUploader:
    @staticmethod
    def upload_file(file_path: str):
        print("\t\t - Uploading file: " + file_path)
        time.sleep(2)
        upload_url = base_url + 'backup/upload'

        with open(file_path, 'rb') as file:
            encrypted_data = Fernet(SECRET_KEY).encrypt(file.read())
            files = {'file': (file_path, encrypted_data)}
            response = requests.post(upload_url, files=files, headers={"Authorization": Auth.token})

            return response.status_code == 200


    @staticmethod
    def list_files(folder_path: str):
        files = os.listdir(folder_path)
        threads = []

        max_threads = 3
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            for file in files:
                full_path = os.path.join(folder_path, file)

                if os.path.isfile(full_path):
                    thread = executor.submit(FileUploader.upload_file, full_path)
                    threads.append(thread)

        for thread in threads:
            thread.result()

    @staticmethod
    def delete_file(file_name: str):
        url = base_url + 'backup/delete-file'
        response = requests.delete(url, json={"fileName": file_name}, headers={"Authorization": Auth.token})
        return response.status_code == 200

    @staticmethod
    def delete_all_files():
        url = base_url + 'backup/delete-all'
        response = requests.delete(url, headers={"Authorization": Auth.token})
        return response.status_code == 200

class Downloader:
    @staticmethod
    def list_backup_files():
        upload_url = base_url + 'backup/list-uploaded-files'
        response = requests.get(upload_url, headers={"Authorization": Auth.token})

        if response.status_code == 200:
            return response.json()
        else:
            print("\t Upload failed with status code: ", response.status_code)

    @staticmethod
    def download_file(file_name: str, target_dir: str, semaphore: Semaphore):
        upload_url = base_url + 'backup/download'
        response = requests.get(
            upload_url,
            json={"fileName": file_name},
            headers={"Authorization": Auth.token}
        )

        if response.status_code == 200:
            with open(target_dir + file_name, 'wb') as target_file:
                decrypted_data = Fernet(SECRET_KEY).decrypt(response.content)
                target_file.write(decrypted_data)
        else:
            print("\t Upload failed with status code:", response.status_code)

        semaphore.release()

    @staticmethod
    def download_list_of_files(file_names: list[str], target_dir: str):
        semaphore: Semaphore = threading.Semaphore(3)

        for file in file_names:
            semaphore.acquire()
            thread = threading.Thread(target=Downloader.download_file, args=(file, target_dir, semaphore))
            thread.start()


class UserInteraction:
    @staticmethod
    def welcome():
        print(ConsoleColors.BLUE)
        print("\n\t\t\t\t\t =========================================")
        print("\t\t\t\t\t|| Welcome to the most worst backup tool ||")
        print("\t\t\t\t\t =========================================")
        print(ConsoleColors.RESET)

        if Auth.auto_login():
            print(ConsoleColors.BLUE, end="")
            print("\t ========================= CURRENT USER: " + Auth.name + " =========================")
            print(ConsoleColors.RESET, end="")
        else:
            UserInteraction.ask_for_login()

    @staticmethod
    def ask_for_login():
        print(ConsoleColors.RESET)
        has_account = input("\t Do you have an account (y || n): ")
        if has_account == 'n':
            UserInteraction.create_new_account()
        elif has_account == 'y':
            UserInteraction.login()

    @staticmethod
    def create_new_account():
        print(ConsoleColors.CYAN, end="")
        print("\n\t Creating new account..")
        print(ConsoleColors.RESET, end="")
        name = input("\t\t * Name: ")
        email = input("\t\t * Email: ")
        password = input("\t\t * Password: ")

        res = Auth.signup(name, email, password)
        if res is None:
            print("Failed to Signup..")
        else:
            print("Welcome " + Auth.name)

    @staticmethod
    def login():
        print(ConsoleColors.CYAN, end="")
        print("\n\t Login..")
        print(ConsoleColors.RESET, end="")
        email = input("\t\t * Email: ")
        password = input("\t\t * Password: ")

        res = Auth.login(email, password)

        if res is None:
            print("Failed to Login..")
        else:
            print(ConsoleColors.BLUE, end="")
            print("\t ========================= CURRENT USER: " + Auth.name + " =========================")
            print(ConsoleColors.RESET, end="")

    @staticmethod
    def enter_command():
        print(ConsoleColors.PURPLE, "FileUploader>>", ConsoleColors.RESET, end="")
        command = input("")
        tokens = shlex.split(command)
        print(ConsoleColors.CYAN, end="")

        if tokens[0] == 'help':
            UserInteraction.help()
        elif tokens[0] == 'upload':
            UserInteraction.upload(tokens)
        elif tokens[0] == 'ls':
            UserInteraction.list_files()
        elif tokens[0] == 'download':
            UserInteraction.download(tokens)
        elif tokens[0] == 'delete':
            UserInteraction.delete(tokens)
        elif tokens[0] == 'delete-all':
            UserInteraction.delete_all()
        elif tokens[0] == 'clear':
            os.system("cls")
        elif tokens[0] == 'logout':
            UserInteraction.logout()
        elif tokens[0] == 'exit':
            exit(0)
        else:
            print(ConsoleColors.RED, end="")
            print("\t Unknown command.")


    @staticmethod
    def help():
        print("\t Commands:")
        print("\t\t help: list all commands.")
        print("\t\t upload <dir-path>: upload all files within the directory.")
        print("\t\t ls: list all uploaded files.")
        print("\t\t download <file-name> <target-path>: save file to specified path.")
        print("\t\t delete <file-name>: delete specific file.")
        print("\t\t delete-all: delete all files.")
        print("\t\t logout: logout from current account.")
        print("\t\t clear: clear the content of terminal.")
        print("\t\t exit: exit program.")

    @staticmethod
    def upload(command_tokens: list[str]):
        if len(command_tokens) < 2:
            print(ConsoleColors.RED, end="")
            print("\t Command uncompleted")
            return
        dir_path = command_tokens[1]
        print("\t Uploading files in directory: " + dir_path + "...")
        FileUploader.list_files(dir_path)
        print("\t Files uploaded successfully")

    @staticmethod
    def list_files():
        files = Downloader.list_backup_files()
        if files is not None:
            if len(files) == 0:
                print("\t No files uploaded")
            else:
                print("\t Uploaded files:")
                for file in files:
                    print("\t\t " + file)

    @staticmethod
    def download(command_tokens: list[str]):
        if len(command_tokens) < 2:
            print(ConsoleColors.RED, end="")
            print("\t Command uncompleted")
            return

        print(ConsoleColors.PURPLE, end="")
        download_dir = input("\t Download to: ")
        print(ConsoleColors.CYAN, end="")

        Downloader.download_list_of_files(command_tokens[1:], download_dir)
        print("\t File downloaded successfully")

    @staticmethod
    def delete(command_tokens: list[str]):
        if len(command_tokens) < 2:
            print(ConsoleColors.RED, end="")
            print("\t Command uncompleted")
            return
        file_name = command_tokens[1]

        FileUploader.delete_file(file_name)
        print("\t File deleted successfully")

    @staticmethod
    def delete_all():
        FileUploader.delete_all_files()
        print("\t All files deleted successfully")

    @staticmethod
    def logout():
        Auth.logout()
        print()
        UserInteraction.ask_for_login()


def main():
    os.system("cls")
    UserInteraction.welcome()

    if Auth.token is not None:
        while True:
            UserInteraction.enter_command()

    # upload D:/chess_game/src/chess_game/
    # munir235@gmail.com
    # john@gmail.com
    # 12345678
    # C:/Users/20114/FCAI/Desktop/


if __name__ == '__main__':
    main()
