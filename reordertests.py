"""Utility to reorder and copy test PDF files into the Exams structure.

Cosmetic cleanup only: use os.path.join and add a docstring. Logic is unchanged.
"""

import os
import shutil
import sys


def quarterlookup(name):
    list1 = ["winter", "feb"]
    list2 = ["april", "spring", "srping"]
    list3 = ["summer", "july"]
    list4 = ["autumn", "dec", "sep", "sept"]
    if name in list1:
        return "1"
    elif name in list2:
        return "2"
    elif name in list3:
        return "3"
    elif name in list4:
        return "4"
    else:
        # keep original behavior: exit on unknown quarter
        sys.exit()


if __name__ == "__main__":
    # Paths in this script are environment-specific; keep logic but prefer os.path.join
    path = r"E:\Storage\Appdata\tests"
    path2 = r"E:\Storage\Appdata\Exams"
    duplist = []

    for file in os.listdir(path):
        filesplit = file.split("_")
        language = "Hebrew"
        year = filesplit[2]
        quarter = quarterlookup(filesplit[1])
        target_dir = os.path.join(path2, language, year)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        filename = f"{language}-{year}-{quarter}.pdf"
        filepath = os.path.join(target_dir, filename)

        if filepath in duplist:
            print(os.path.join(path, file), filepath)
        else:
            duplist.append(filepath)
            shutil.copy(os.path.join(path, file), filepath)
