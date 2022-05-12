import pathlib, typer, click
from typer import *
class ProjectLineCounter:
    '''
    Initializes the ProjectLineCounter class.

    Args:
        project_path (str): The path to the project.

    '''
    def __init__(self, project_path):
        self.options = {'-h': False, '-l': False, '-f': False, '-p': False, '-a': False}

        self.project_path = project_path
        self.project_files:int = self.get_project_files()
        self.project_lines:int = self.get_project_lines()
        self.lines:int = 0
    
    def parse_options(self, args=typer.Argument(('-h', '-l', '-f', '-p', '-a'))):
        '''
        Parses the options.

        Args:
            args (list): The arguments.
        '''
        # for arg in args:
        if args in self.options:
            self.options[args] = True
        else:
            typer.echo(f'Invalid option: {args}', err=True)
            self.print_help()

    def execute_opts(self, flags):
        '''
        Executes the options.

        Args:
            flags (dict): The flags to execute.
        '''
        if flags['-h']:
            self.print_help()
        elif flags['-l']:
            self.print_lines()
        elif flags['-f']:
            self.print_files()
        elif flags['-p']:
            self.print_path()
        elif flags['-a']:
            self.print_all()
        else:
            self.print_help()
    
    def get_project_files(self):
        '''
        Gets the project files.
        '''
        # Get the project files
        files = 0
        # iterate over the project files
        for path in pathlib.Path(self.project_path).glob('**/*'):
            # if the path is a file
            if path.is_file():
                # increment the files
                files += 1
        # return the files
        return files
    
    def get_project_lines(self):
        '''
        Gets the project lines.
        '''
        # Get the project lines
        lines = 0
        # iterate over the project files
        for path in pathlib.Path(self.project_path).glob('**/*'):
            # if the path is a file
            if path.is_file():
                # open the file
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    # increment the lines
                    lines += len(file.readlines())
        # return the lines
        return lines
    
    def print_help(self):
        '''
        Prints the help.
        '''
        typer.echo(f'Usage: project_line_counter.py [options]')
        typer.echo(f'Options:')
        typer.echo(f'\t-h: Prints this help.')
        typer.echo(f'\t-l: Prints the project lines.')
        typer.echo(f'\t-f: Prints the project files.')
        typer.echo(f'\t-p: Prints the project path.')
        typer.echo(f'\t-a: Prints all.')
        typer.echo(f'\t-h: Prints this help.')

    def print_lines(self):
        '''
        Prints the lines.
        '''
        typer.echo(f'Project lines: {self.project_lines}')

    def about(self):
        '''
        Prints the about.
        '''
        typer.echo(f'ProjectLineCounter v1.0.0')
        typer.echo(f'Author: Rohaan Ahmed')
        typer.echo(f'License: MIT')
        typer.echo(f'\thttps://github.com/Wizock/project_line_counter')

if __name__ == '__main__':
    # create the project line counter
    project_line_counter = ProjectLineCounter(project_path=str(pathlib.Path.cwd()))
    # parse the options
    project_line_counter.parse_options(args=typer.Argument)
    # execute the options
    project_line_counter.execute_opts(flags=project_line_counter.options)
