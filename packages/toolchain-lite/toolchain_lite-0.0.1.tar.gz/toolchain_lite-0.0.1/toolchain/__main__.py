import os

current_file_path = os.path.abspath(__file__)

parent_directory = os.path.dirname(current_file_path)

os.chdir(parent_directory)

os.system("gradlew :composeApp:wasmJsBrowserDevelopmentRun")
