import pathlib
import sys

import click
import typer
from typer import *


class ProjectLineCounter:
    """
    Initializes the ProjectLineCounter class.

    Args:
        project_path (str): The path to the project.

    """

    def __init__(self, project_path):
        self.options = {
            "-h": False,
            "-l": False,
            "-f": False,
            "-p": False,
            "-a": False,
            "--write": False,
        }

        self.project_path = project_path
        self.project_files: int = self.get_project_files()
        self.project_lines: int = self.get_project_lines()
        self.lines: int = 0

    def parse_options(self, args: list):
        """
        Parses the options.

        Args:
            args (list): The arguments.
        """
        print(args)
        for arg in args:
            if arg in self.options:
                self.options[arg] = True
            else:
                typer.echo(f"Invalid option: {arg}", err=True)
                self.print_help()

    def execute_opts(self, flags):
        """
        Executes the options.

        Args:
            flags (dict): The flags to execute.
        """
        if flags["-h"]:
            self.print_help()
        if flags["-l"]:
            self.print_lines()
        if flags["-f"]:
            self.print_files()
        if flags["-p"]:
            self.print_path()
        if flags["-a"]:
            self.print_all()
        if flags["--write"]:
            self.write()
        else:
            self.print_help()

    def get_project_files(self):
        """
        Gets the project files.
        """
        # Get the project files
        files = 0
        # iterate over the project files
        for path in pathlib.Path(self.project_path).glob("**/*"):
            # if the path is a file
            if path.is_file():
                # increment the files
                files += 1
        # return the files
        return files

    def print_all(self):
        """
        Prints all.
        """
        typer.echo(f"Project lines: {self.project_lines}")
        typer.echo(f"Project files: {self.project_files}")
        typer.echo(f"Project path: {self.project_path}")

    def get_project_lines(self):
        """
        Gets the project lines.
        """
        # Get the project lines
        lines = 0
        # iterate over the project files
        import os

        directory = "."
        directory_depth = 100 # How deep you would like to go
        extensions_to_consider = [".py", ".css"]  # Change to ["all"] to include all extensions
        exclude_filenames = ["venv", ".idea", "__pycache__", "cache"]
        skip_file_error_list = True

        this_file_dir = os.path.realpath(__file__)

        print("Path to ignore:", this_file_dir)
        print("=====================================")
        def _walk(path, depth):
            """Recursively list files and directories up to a certain depth"""
            depth -= 1
            with os.scandir(path) as p:
                for entry in p:

                    skip_entry = False
                    for fName in exclude_filenames:
                        if entry.path.endswith(fName):
                            skip_entry = True
                            break

                    if skip_entry:
                        print("Skipping entry", entry.path)
                        continue

                    yield entry.path
                    if entry.is_dir() and depth > 0:
                        yield from _walk(entry.path, depth)

        print("Caching entries")
        files = list(_walk(directory, directory_depth))
        print("=====================================")

        print("Counting Lines")
        file_err_list = []
        line_count = 0
        len_files = len(files)
        for i, file_dir in enumerate(files):

            if file_dir == this_file_dir:
                print("=[Rejected file directory", file_dir, "]=")
                continue

            if not os.path.isfile(file_dir):
                continue

            skip_File = True
            for ending in extensions_to_consider:
                if file_dir.endswith(ending) or ending == "all":
                    skip_File = False

            if not skip_File:
                try:
                    file = open(file_dir, "r")
                    local_count = 0
                    for line in file:
                        if line != "\n":
                            local_count += 1
                    print("({:.1f}%)".format(100*i/len_files), file_dir, "|", local_count)
                    line_count += local_count
                    file.close()
                except:
                    file_err_list.append(file_dir)
                    continue
        print("=====================================")
        print("File Count Errors:", len(file_err_list))
        if not skip_file_error_list:
            for file in file_err_list:
                print(file_err_list)

        print("=====================================")
        print("Total lines |", line_count)

        # return the lines
        return line_count

    def write(self):
        """
        Writes the project lines to a text file.
        """
        # open the file
        with open("project_lines.txt", "w", encoding="utf-8") as file:
            # write the project lines
            file.write(f"{self.project_lines}")
            file.write("\n")
            file.write(f"{self.project_files}")
            file.close()

    def print_help(self):
        """
        Prints the help.
        """
        typer.echo(f"Usage: project_line_counter.py [options]")
        typer.echo(f"Options:")
        typer.echo(f"\t-h: Prints this help.")
        typer.echo(f"\t-l: Prints the project lines.")
        typer.echo(f"\t-f: Prints the project files.")
        typer.echo(f"\t-p: Prints the project path.")
        typer.echo(f"\t-a: Prints all.")
        typer.echo(f"\t-h: Prints this help.")

    def print_lines(self):
        """
        Prints the lines.
        """
        typer.echo(f"Project lines: {self.project_lines}")

    def about(self):
        """
        Prints the about.
        """
        typer.echo(f"ProjectLineCounter v1.0.0")
        typer.echo(f"Author: Rohaan Ahmed")
        typer.echo(f"License: MIT")
        typer.echo(f"\thttps://github.com/Wizock/project_line_counter")


if __name__ == "__main__":
    # create the project line counter
    project_line_counter = ProjectLineCounter(project_path=str(pathlib.Path.cwd()))
    # parse the options
    project_line_counter.parse_options(args=sys.argv[1:])
    # execute the options
    project_line_counter.execute_opts(flags=project_line_counter.options)
