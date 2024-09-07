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
        sys.exit()
        print("oh my god")


if __name__ == "__main__":
    path = r"E:\Storage\Appdata\tests"
    path2 = r"E:\Storage\Appdata\Exams"
    sep = "\\"
    dash = "-"
    duplist = []
    for file in os.listdir(path):
        filesplit = file.split("_")
        language = "Hebrew"
        year = filesplit[2]
        quarter = quarterlookup(filesplit[1])
        if os.path.isdir(path2 + sep + language + sep + year + sep):
            pass
        else:
            os.mkdir(path2 + sep + language + sep + year + sep)
        filepath = (
            path2
            + sep
            + language
            + sep
            + year
            + sep
            + language
            + dash
            + year
            + dash
            + quarter
            + ".pdf"
        )
        if filepath in duplist:
            print(path + sep + file, filepath)
            pass
        else:
            duplist.append(filepath)
            # print(path+sep+file,filepath)
            shutil.copy(path + sep + file, filepath)
