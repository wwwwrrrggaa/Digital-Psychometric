import os
import pickle
import sys

import pymupdf


def cropgradingkey(filename):
    rect = pymupdf.Rect(pymupdf.Point(100, 350), pymupdf.Point(500, 630))
    ogfile = pymupdf.open(filename)
    crop = ogfile[-7]
    crop.set_cropbox(rect)
    img = crop.get_pixmap()
    filename2 = filename.replace("tests", "tests2")
    ogfile.select([ogfile.page_count - 7])
    ogfile.save(filename2)


def verifynumeric(word):
    if len(word) == 0:
        return False
    if word.isnumeric():
        return True
    elif word[-1].isnumeric():
        return True
    elif word[0].isnumeric():
        return True
    return False


###2007 2012,2103,2107,2112,2204,2207,2209,2212,2307
def getgradingkey(filename):
    ogfile = pymupdf.open(filename)
    page = ogfile[0]
    gradingkey = {}
    text = [word for word in page.get_text().split("\n") if verifynumeric(word)]
    temp = []
    for index in range(len(text)):
        try:
            int(text[index])
        except ValueError:
            text[index] = text[index].replace("ו2", "122")
            text[index] = text[index].replace(" ", "")
            text[index] = text[index].replace("ו", "")
            text[index] = text[index].replace(".", "")

        currentword = text[index]
        if int(text[index]) < 50:
            # print(int(text[index]))
            gradingkey[text[index]] = temp
            temp = []
        else:
            temp.append(currentword)
    # print(gradingkey)
    print("\n")
    # listcompare=[str(i) for i in range(1,0)]
    count = 0
    for i in range(0, 47):
        if str(i) not in gradingkey:
            # print(filename)
            # print(gradingkey)
            # print(text)
            count += 1
        elif len(gradingkey[str(i)]) == 0:
            count += 1
            print(i)
        elif len(gradingkey[str(i)]) == 1:
            gradingkey[str(i)] = [0, 0, gradingkey[str(i)][0]]
        elif len(gradingkey[str(i)]) == 2:
            gradingkey[str(i)] = [gradingkey[str(i)][0], 0, gradingkey[str(i)][1]]

    if count != 0:
        if filename == r"C:\Users\Public\Appdata\hotfolder\\Sim_2109_ocred (2).pdf":
            gradingkey = {
                "0": ["50", "50", "50"],
                "1": ["52", "52", "51"],
                "2": ["54", "54", "52"],
                "3": ["56", "56", "53"],
                "4": ["58", "58", "54"],
                "5": ["60", "60", "55"],
                "6": ["62", "62", "57"],
                "7": ["64", "65", "59"],
                "8": ["66", "67", "61"],
                "9": ["68", "70", "63"],
                "10": ["70", "72", "65"],
                "11": ["72", "75", "67"],
                "12": ["75", "77", "69"],
                "13": ["77", "80", "72"],
                "14": ["80", "82", "74"],
                "15": ["82", "85", "76"],
                "16": ["84", "88", "78"],
                "17": ["87", "90", "81"],
                "18": ["89", "93", "83"],
                "19": ["92", "95", "86"],
                "20": ["94", "98", "88"],
                "21": ["96", "101", "90"],
                "22": ["98", "103", "93"],
                "23": ["101", "106", "95"],
                "24": ["103", "108", "98"],
                "25": ["105", "111", "100"],
                "26": ["107", "114", "102"],
                "27": ["110", "117", "104"],
                "28": ["112", "119", "107"],
                "29": ["115", "122", "109"],
                "30": ["117", "125", "111"],
                "31": ["119", "128", "114"],
                "32": ["122", "130", "116"],
                "33": ["124", "133", "119"],
                "34": ["127", "135", "121"],
                "35": ["129", "138", "124"],
                "36": ["132", "140", "126"],
                "37": ["134", "143", "128"],
                "38": ["137", "145", "131"],
                "39": ["139", "148", "133"],
                "40": ["142", "150", "135"],
                "41": ["144", 0, "138"],
                "42": ["146", 0, "140"],
                "43": ["148", 0, "143"],
                "44": ["150", 0, "145"],
                "45": [0, 0, "148"],
                "46": ["150"],
            }

    print(gradingkey)
    # newfilename=convertfilename(filename)
    # print(filename, newfilename)
    # os.remove(newfilename)
    # picklesave(gradingkey, newfilename)
    # return gradingkey


def abs2(stri):
    return abs(int(stri))


def cropanswers(filename):
    rect = pymupdf.Rect(pymupdf.Point(100, 110), pymupdf.Point(490, 800))
    ogfile = pymupdf.open(filename)
    crop = ogfile[-8]
    crop.set_cropbox(rect)
    filename2 = filename.replace("tests", "tests3")
    ogfile.select([ogfile.page_count - 8])
    ogfile.save(filename2)


def textianswers(filename):
    filename = filename.replace("tests", "tests5")
    filename = filename.replace(".pdf", ".txt")
    f = open(filename, "r")
    lines = f.readlines()
    for index in range(len(lines)):
        lines[index] = lines[index].replace("\t", "")
        lines[index] = lines[index].replace(
            " ",
            "",
        )
        lines[index] = lines[index].replace(
            "\n",
            "",
        )
    # print([i for i in lines],filename)
    return lines


def verify(text):
    A = "עמוד"
    B = "ריק"
    if A in text and B in text:
        return True
    return False


globlist = {2019: [], 2020: [], 2021: [], 2022: [], 2023: []}


def convertfilename(filename):
    global globlist
    print(filename)
    firstsplit = filename[-18:-14]
    print(firstsplit)
    year = firstsplit[0:2]
    quarter = firstsplit[2:4]
    year = "20" + year
    if quarter == "01":
        quarter = "1"
    elif quarter == "02":
        quarter = "1"
    elif quarter == "03":
        quarter = "1"
    elif quarter == "04":
        quarter = "1"
    elif quarter == "05":
        quarter = "2"
    elif quarter == "06":
        quarter = "2"
    elif quarter == "07":
        quarter = "2"
    elif quarter == "08":
        quarter = "3"
    elif quarter == "09":
        quarter = "3"
    elif quarter == "10":
        quarter = "4"
    elif quarter == "11":
        quarter = "4"
    elif quarter == "12":
        quarter = "4"
    globlist[int(year)].append(quarter)
    filename = r"C:\Users\Public\Appdata\FullExams\Hebrew\2021\2\gradingkey.txt"
    filename = filename.replace("2021", year)
    filename = list(filename)
    filename[-16] = quarter
    filename = "".join(filename)
    return filename


def getpagelist(filename):
    file = pymupdf.open(filename)
    pages = list(file.pages(0, file.page_count))
    text = [index for index in range(len(pages)) if verify(pages[index].get_text())]
    texttrueform = {str(i + 1): [text[i] + 1, text[i + 1]] for i in range(8)}
    newfilename = convertfilename(filename)
    print(filename, newfilename)
    os.remove(newfilename)
    picklesave(texttrueform, newfilename)


def addimage(filename):
    rect = pymupdf.Rect(pymupdf.Point(90, 80), pymupdf.Point(560, 800))
    ogfile = pymupdf.open(filename)
    crop = ogfile[-8]
    crop.set_cropbox(rect)
    pixmap = crop.get_pixmap()
    imgsave = filename.replace("exam.pdf", "answer.png")
    pixmap.pil_save(imgsave)
    return crop


def preprocessing(filename, pdffile):
    # getpagelist(filename)
    # pagelist = {'1': [4, 11], '2': [12, 19], '3': [20, 27], '4': [28, 35], '5': [36, 43],
    # '6': [44, 51], '7': [53, 60], '8': [61, 70]}  # splitchapters(reader)
    # file = pymupdf.open(filename)
    # gradingkey = cropgradingkey(filename)
    # cropanswers(filename)
    # gradingkey = getgradingkey(filename.replace('tests', 'hotfolder').replace('.pdf', '_ocred (2).pdf'))
    # answers=testianswers(filename)
    # examname=pdffile.replace('.pdf','')
    # dir=r"C:\Users\Public\Appdata\FullExams\\"+examname+'\\'
    # os.mkdir(dir)
    # file.save(dir+'exam.pdf')
    # picklesave(pagelist,dir+"pagelist.txt")
    # picklesave(gradingkey,dir+"gradingkey.txt")
    # picklesave(answers,dir+"answers.txt")
    pass


def picklesave(data, filename):
    with open(filename, "wb") as fp:
        pickle.dump(data, fp)


if __name__ == "__main__":
    errorFormat = '<span style="color:red;">{}</span>'
    print("a" + errorFormat.format("b"))
    sys.exit(0)
    sep = r"\\"
    folder = r"C:\Users\Public\Appdata\FullExams\Hebrew"
    for yearfolder in os.listdir(folder):
        for quarter in os.listdir(folder + sep + yearfolder):
            filename = folder + sep + yearfolder + sep + quarter + sep + "exam.pdf"
            # addimage(filename)
