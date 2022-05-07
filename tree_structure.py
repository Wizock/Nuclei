import os

from sqlalchemy import true


def make_tree_file():
    os.system("tree /a /f > tree_file.txt")


def format_tree_file():
    with open("tree_file.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            turnicate_line = line.replace("\n", "")


def remove_pyc():
    with open("tree_file.txt", "r") as f:
        lines = f.readlines()
    with open("tree_file.txt", "w") as w:
        for line in lines:
            if ".pyc" in line:
                continue
            if "__pycache__" in line:
                continue
            if "Folder PATH listing for volume coding_drive" in line:
                pass
            w.write(line)


def rem_doubles():
    # remove extra ```py and ``` from tree_file.txt
    with open("tree_file.txt", "r") as f:
        lines = f.read()
        lines = lines.replace("```bat", "")
        lines = lines.replace("```", "")
        with open("tree_file.txt", "w") as f:
            f.write(lines)


def highlighting_wrapper():
    with open("tree_file.txt", "r") as f:
        lines = f.read()
        lines = f"```bat\n{lines}\n```"

        with open("tree_file.txt", "w") as f:
            f.write(lines)

    with open("tree_file.txt", "r") as f:
        lines = f.read()
        for line in lines:
            if ".pyc" in line:
                lines.remove(line)


def inject_into_readme():
    highlighting_wrapper()
    array_to_overwrite = list()
    with open("README.md", "r+") as f:
        lines = f.readlines()
    with open("tree_file.txt", "r") as f:
        tree_file = f.read()

    for line in lines:
        array_to_overwrite.append(line)
        if "# File Structure" in line:

            for tree_line in tree_file:
                array_to_overwrite.append(tree_line)
            break
        else:
            continue

    with open("README.md", "w") as f:
        for lines in array_to_overwrite:
            f.write(lines)


def main():
    make_tree_file()
    remove_pyc()
    highlighting_wrapper()
    rem_doubles()
    inject_into_readme()


if __name__ == "__main__":
    main()
