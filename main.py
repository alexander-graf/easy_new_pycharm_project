import os
import tkinter as tk
import subprocess
from loguru import logger

# Configure Loguru logger
logger.add("app.log", rotation="500 MB", level="DEBUG")


def get_pycharm_executable():
    try:
        result = subprocess.run(
            ["where", "pycharm.bat"], capture_output=True, text=True, check=True
        )
        pycharm_executable = result.stdout.strip()
        logger.info(f"PyCharm executable path: {pycharm_executable}")
        return pycharm_executable
    except subprocess.CalledProcessError:
        logger.error("PyCharm executable not found")
        return None


def create_project():
    project_name = project_entry.get()
    logger.info(f"Creating new project: {project_name}")

    # Determine the path to PyCharm executable
    pycharm_executable = get_pycharm_executable()

    if pycharm_executable:
        # Create the new project folder
        user_profile = os.environ.get("USERPROFILE")
        project_folder = os.path.join(user_profile, "PycharmProjects", project_name)
        os.makedirs(project_folder, exist_ok=True)
        logger.info(f"New project folder created: {project_folder}")

        # Create the config and pics folders within the project folder using PowerShell commands
        powershell_commands = [
            f'New-Item -Path "{project_folder}\\config" -ItemType Directory',
            f'New-Item -Path "{project_folder}\\pics" -ItemType Directory',
        ]
        subprocess.run(
            ["powershell.exe", "-Command", ";".join(powershell_commands)], check=True
        )
        logger.info("Config and pics folders created")

        # Open the project folder in PyCharm
        subprocess.run([pycharm_executable, project_folder])
        logger.info("Project folder opened in PyCharm")
    else:
        logger.error("Failed to open project folder in PyCharm")


# Create the GUI window
window = tk.Tk()
window.title("New Project")
window.geometry("300x150")

# Create the project name label and entry
project_label = tk.Label(window, text="Project Name:")
project_label.pack()

project_entry = tk.Entry(window)
project_entry.pack()

# Create the create project button
create_button = tk.Button(window, text="Create Project", command=create_project)
create_button.pack()

window.mainloop()
