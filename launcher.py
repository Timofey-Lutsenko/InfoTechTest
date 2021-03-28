import subprocess
import logging
import os


logger = logging.getLogger('mainapp.log')


def path_checker(path):
    if os.path.exists(path):
        return True
    else:
        return False


# Opening console on start
def launcher():
    print('Input get src_path dst_path - to download file from DropBox.\n'
          'Or put src_path dst_path - to upload file to DropBox.\n'
          'Input "exit" to exit. Input "help" to show README.')
    while True:
        action = input('>: ')
        if action.lower() == 'exit':
            break
        if action.lower() == 'help':
            with open('Manual', 'r') as file:
                for line in file:
                    print(line)
        else:
            subprocess.Popen(f'mainapp.exe {action}',
                             creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    launcher()
