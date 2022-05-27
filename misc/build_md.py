import os


def make_tree_file():
    """
    Make the tree file.
    """
    # make the tree file
    os.system("tree /a /f > tree_file.txt")


def make_lines_file():
    """
    Make the lines file.
    """
    # make the lines file
    os.system("py project_line_counter.py --write")


def format_tree_file():
    """
    Format the tree file.
    """
    # make the tree file
    with open("tree_file.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            turnicate_line = line.replace("\n", "")


def remove_pyc():
    """
    Remove the pyc files.
    """
    # open the tree file
    with open("tree_file.txt", "r") as f:
        # read the file
        lines = f.readlines()
    # open the tree file
    with open("tree_file.txt", "w") as w:
        # write the file
        for line in lines:
            # remove the pyc files
            if ".pyc" in line:
                continue
            # remove the pycache folders
            if "__pycache__" in line:
                continue
            if "Folder PATH listing for volume coding_drive" in line:
                pass
            # write the line
            w.write(line)


def rem_doubles():
    """
    Remove doubles.
    """
    # remove extra ```py and ``` from tree_file.txt
    with open("tree_file.txt", "r") as f:
        # read the file
        lines = f.read()
        # split the file into lines
        lines = lines.replace("```bat", "")
        # remove the extra ```py
        lines = lines.replace("```", "")
        # write the file
        with open("tree_file.txt", "w") as f:
            # write the file
            f.write(lines)


def highlighting_wrapper():
    """
    Highlighting wrapper.
    """
    # open the tree file
    with open("tree_file.txt", "r") as f:
        # split the file into lines
        lines = f.read()
        # add the highlight to the file
        lines = f"```bat\n{lines}\n```"
        # write the file
        with open("tree_file.txt", "w") as f:
            f.write(lines)
    # open the tree file
    with open("tree_file.txt", "r") as f:
        lines = f.read()
        for line in lines:
            if ".pyc" in line:
                lines.remove(line)


def write_lines_file():
    """
    Write the lines file.
    """
    make_lines_file()
    array_to_overwrite = list()
    # open the readme
    with open("../README.md", "r+") as f:
        lines = f.readlines()
    # open the tree file
    with open("project_lines.txt", "r") as f:
        tree_file = f.read()
    # iterate over the lines
    for line in lines:
        # if the line is the tree file
        array_to_overwrite.append(line)
        if "# Project Size" in line:
            # iterate over the tree file
            if "## lines of code" in line:
                ...
            if "## amount of files" in line:
                ...

            for tree_line in tree_file:
                # add the tree file to the array
                array_to_overwrite.append(tree_line)
            break
        else:
            continue
    # open the readme
    with open("../README.md", "w") as f:
        # write the array
        for lines in array_to_overwrite:

            f.write(lines)


def inject_into_readme():
    """
    Inject the tree file into the readme.
    """
    highlighting_wrapper()
    array_to_overwrite = list()
    # open the readme
    with open("../README.md", "r+") as f:
        lines = f.readlines()
    # open the tree file
    with open("tree_file.txt", "r") as f:
        tree_file = f.read()
    # iterate over the lines
    for line in lines:
        # if the line is the tree file
        array_to_overwrite.append(line)
        if "# File Structure" in line:
            # iterate over the tree file
            for tree_line in tree_file:
                # add the tree file to the array
                array_to_overwrite.append(tree_line)
            break
        else:
            continue
    # open the readme
    with open("../README.md", "w") as f:
        # write the array
        for lines in array_to_overwrite:

            f.write(lines)


def main():
    """
    Main function.
    """
    make_tree_file()
    remove_pyc()
    highlighting_wrapper()
    rem_doubles()
    inject_into_readme()
    # write_lines_file()


if __name__ == "__main__":
    main()
