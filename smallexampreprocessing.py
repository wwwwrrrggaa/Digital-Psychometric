import os
import pickle
import re
import shutil
import sys

from pymupdf import open as pdfopen

gradingkey = []
saveslot = ""


def getgradingkey():
    global gradingkey
    return gradingkey


def givefinalscores(rawscores):
    gradingkey = getgradingkey()
    finalgradingkey = {
        "50": "200",
        "51": "221",
        "52": "228",
        "53": "234",
        "54": "241",
        "55": "248",
        "56": "249",
        "57": "256",
        "58": "262",
        "59": "269",
        "60": "276",
        "61": "277",
        "62": "284",
        "63": "290",
        "64": "297",
        "65": "304",
        "66": "305",
        "67": "312",
        "68": "319",
        "69": "326",
        "70": "333",
        "71": "334",
        "72": "341",
        "73": "348",
        "74": "354",
        "75": "361",
        "76": "362",
        "77": "369",
        "78": "376",
        "79": "382",
        "80": "389",
        "81": "390",
        "82": "397",
        "83": "404",
        "84": "411",
        "85": "418",
        "86": "419",
        "87": "426",
        "88": "432",
        "89": "439",
        "90": "446",
        "91": "447",
        "92": "454",
        "93": "460",
        "94": "467",
        "95": "474",
        "96": "475",
        "97": "482",
        "98": "489",
        "99": "496",
        "100": "503",
        "101": "504",
        "102": "511",
        "103": "518",
        "104": "524",
        "105": "531",
        "106": "532",
        "107": "539",
        "108": "546",
        "109": "552",
        "110": "559",
        "111": "560",
        "112": "567",
        "113": "574",
        "114": "580",
        "115": "587",
        "116": "588",
        "117": "595",
        "118": "602",
        "119": "609",
        "120": "616",
        "121": "617",
        "122": "624",
        "123": "630",
        "124": "637",
        "125": "644",
        "126": "645",
        "127": "652",
        "128": "658",
        "129": "665",
        "130": "672",
        "131": "673",
        "132": "680",
        "133": "687",
        "134": "694",
        "135": "701",
        "136": "702",
        "137": "709",
        "138": "716",
        "139": "722",
        "140": "729",
        "141": "730",
        "142": "738",
        "143": "746",
        "144": "753",
        "145": "761",
        "146": "762",
        "147": "773",
        "148": "784",
        "149": "795",
        "150": "800",
    }
    hebscore, mathscore, engscore = rawscores
    hebscore = int(gradingkey[hebscore][0])
    mathscore = int(gradingkey[mathscore][0])
    engscore = int(gradingkey[engscore][0])
    totalscore = finalgradingkey[
        str(int((2 * hebscore + 2 * mathscore + engscore) / 5.0))
    ]
    totalhebscore = finalgradingkey[
        str(int((3 * hebscore + 1 * mathscore + engscore) / 5.0))
    ]
    totalmathscore = finalgradingkey[
        str(int((1 * hebscore + 3 * mathscore + engscore) / 5.0))
    ]
    return totalscore, totalmathscore, totalhebscore


def saveanswers(answerlist, counter):
    appdata = getsaveslot() + r"\Answers\\" + str(counter) + ".txt"
    with open(appdata, "wb") as fp:
        pickle.dump(answerlist, fp)
    return appdata


def classifychapters(answerlist):
    list2 = []
    for item in answerlist:
        if "p" in item:
            list2.append(3)
        elif len(item) == 20:
            list2.append(1)
        elif len(item) == 22:
            list2.append(2)
        else:
            list2.append(0)
    return list2


def getsaveslot():
    global saveslot
    return saveslot


def fillrange(seplist):
    chapterlist = {str(i + 1): [] for i in range(6)}
    count = 1
    for j in range(len(seplist) - 1):
        i = seplist[j]
        chapterlist[str(count)].append(seplist[count - 1])
        chapterlist[str(count)].append(seplist[count] - 1)
        count += 1
    return chapterlist


def createchapterfiles(filename, pagelist):
    appdata = getsaveslot() + "\Chapters"
    filenames = []
    for i in pagelist.keys():
        ogfile = pdfopen(filename)
        pagezone = pagelist[i]
        chapterfile = appdata + "\\" + "chapter-" + i + ".pdf"
        filenames.append(chapterfile)
        ogfile.select(range(pagezone[0], pagezone[1]))
        ogfile.save(chapterfile)
        ogfile.close()
    return filenames


def wipesaveslot(saveslot):
    for folder in os.listdir(saveslot):
        for file in os.listdir(saveslot + r"\\" + folder):
            os.remove(saveslot + r"\\" + folder + r"\\" + file)


def savetrueanswers(answerlist, chapternames):
    counter = 0
    trueanswerlist = []
    for i in range(len(answerlist)):
        appdata = (
            getsaveslot()
            + "\Trueanswers\\"
            + str(i)
            + "-"
            + str(chapternames[i])
            + ".txt"
        )
        trueanswerlist.append(appdata)
        with open(appdata, "wb") as fp:
            pickle.dump(answerlist[i], fp)
    return trueanswerlist


def mainfullexam(filename, saveslotnew):
    global gradingkey, saveslot
    saveslot = saveslotnew
    wipesaveslot(saveslot)
    foldername = filename + "\\"
    answers = pickle.load(open(foldername + "answers.txt", "rb"))
    gradingkey = pickle.load(open(foldername + "gradingkey.txt", "rb"))
    pagelist = pickle.load(open(foldername + "pagelist.txt", "rb"))
    file = pdfopen(foldername + "exam.pdf")
    examnames = createchapterfiles(foldername + "exam.pdf", pagelist)
    answers = [list(item) for item in answers]
    return (
        examnames,
        answers,
        classifychapters(answers),
        savetrueanswers(answers, classifychapters(answers)),
    )


def splitchapters(reader):
    seplist = []
    pages = [reader.pages[i] for i in range(reader.get_num_pages())]
    count = 0
    for page in pages:
        count += 1
        search = "עמוד ריק"
        search2 = "ריק"
        search3 = "עמוד"
        Text = page.extract_text()
        research = re.search(search, Text)
        if research:
            seplist.append(count)
        elif re.match(search2, Text) and re.match(search3, Text):
            seplist.append(count)

    return fillrange(seplist)


def swap(text_blocks):
    for i in range(len(text_blocks)):
        if text_blocks[i].endswith("חשיבה מילולית"):
            text_blocks[i] = 0
        elif text_blocks[i].endswith("חשיבה כמותית"):
            text_blocks[i] = 1
        else:
            text_blocks[i] = 2
    if text_blocks[0] != text_blocks[1] != text_blocks[2]:
        print("incorrect reading")
        sys.exit(0)


def verify(text_blocks, tabs, pagelist):
    if len(text_blocks) != len(tabs) != len(pagelist):
        print("incorrect reading!!!")
        sys.exit(0)


def getanswers(answerpage):
    text_blocks = [i for i in answerpage.get_text().splitlines() if "-" in i][1:]
    swap(text_blocks)
    tabs = answerpage.find_tables()
    answerslist = []
    # print(f"{len(tabs.tables)} table(s) on {'answerpage'}")
    for table in tabs:
        ans = table.extract()[1][:-1]
        answerslist.append(ans)
    return answerslist, text_blocks


def saveanswers(answerlist, counter):
    appdata = getsaveslot() + r"\Answers\\" + str(counter) + ".txt"
    with open(appdata, "wb") as fp:
        pickle.dump(answerlist, fp)
    return appdata


def savetrueanswers(answerlist, chapternames):
    counter = 0
    trueanswerlist = []
    for i in range(len(answerlist)):
        appdata = (
            getsaveslot()
            + "\Trueanswers\\"
            + str(i)
            + "-"
            + str(chapternames[i])
            + ".txt"
        )
        trueanswerlist.append(appdata)
        with open(appdata, "wb") as fp:
            pickle.dump(answerlist[i], fp)
    return trueanswerlist


def createchapterfiles(filename, pagelist):
    appdata = getsaveslot() + "\Chapters"
    filenames = []
    for i in pagelist.keys():
        ogfile = pdfopen(filename)
        pagezone = pagelist[i]
        chapterfile = appdata + "\\" + "chapter-" + i + ".pdf"
        filenames.append(chapterfile)
        ogfile.select(range(pagezone[0], pagezone[1]))
        ogfile.save(chapterfile)
        ogfile.close()
    return filenames


def checkperentry(containlist, checkstring):
    for letterr in containlist:
        if letterr in checkstring:
            return True
        else:
            return False


def checklist(list):
    hebrewletters = "ראטוןםםפשדגכעייחלךףזסבהנמצתץ"
    hebrewletters = [i for i in hebrewletters]
    counter = 0
    for item in list:
        if item.isnumeric():
            counter += 1
    if counter > len(list) / 2:
        return True
    else:
        return False


def extractgradingkey(gradepage):
    tables = gradepage.find_tables()
    gradingkey = {str(i): [] for i in range(47)}
    for tab in tables:
        for gradekey in tab.extract():
            if len(gradekey) == 4 and None not in gradekey:
                gradingkey[gradekey[-1]] = gradekey[:-1]
    if gradingkey["4"] == []:
        return extractgradingkey2(gradepage)
    else:
        return gradingkey


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def extractgradingkey2(gradepage):
    tables = gradepage.find_tables()
    gradingkey = {str(i): [] for i in range(47)}
    for tab in tables:
        for gradekey in tab.extract():
            if len(gradekey) == 14:
                gradekey = remove_values_from_list(gradekey, None)
                if checklist(gradekey):
                    if len(gradekey) == 13:
                        gradekey.remove("")
                    chunks = [gradekey[x : x + 4] for x in range(0, len(gradekey), 4)]
                    for chunk in chunks:
                        gradingkey[chunk[-1]] = chunk[:-1]
    return gradingkey


def convertonscale(OldMin, OldMax, NewMin, NewMax, OldValue):
    OldRange = OldMax - OldMin
    if OldRange == 0:
        NewValue = NewMin
    else:
        NewRange = NewMax - NewMin
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue


def extractmyrange(page):
    rangea = [
        (50, 50),
        (51, 55),
        (56, 60),
        (61, 65),
        (66, 70),
        (71, 75),
        (76, 80),
        (81, 85),
        (86, 90),
        (91, 95),
        (96, 100),
        (101, 105),
        (106, 110),
        (111, 115),
        (116, 120),
        (121, 125),
        (126, 130),
        (131, 135),
        (136, 140),
        (141, 145),
        (146, 149),
        (150, 150),
    ]
    rangeb = [
        (200, 200),
        (221, 248),
        (249, 276),
        (277, 304),
        (305, 333),
        (334, 361),
        (362, 389),
        (390, 418),
        (419, 446),
        (447, 474),
        (475, 503),
        (504, 531),
        (532, 559),
        (560, 587),
        (588, 616),
        (617, 644),
        (645, 672),
        (673, 701),
        (702, 729),
        (730, 761),
        (762, 795),
        (800, 800),
    ]
    finalgradingkey = {}
    for gradeclassindex in range(len(rangea)):
        gradeclass = rangea[gradeclassindex]
        for grade in range(gradeclass[0], gradeclass[1] + 1):
            newgrade = convertonscale(
                *rangea[gradeclassindex], *rangeb[gradeclassindex], grade
            )
            finalgradingkey[str(grade)] = str(round(newgrade))

    return finalgradingkey


def givefinalscores(rawscores):
    gradingkey = getgradingkey()
    finalgradingkey = {
        "50": "200",
        "51": "221",
        "52": "228",
        "53": "234",
        "54": "241",
        "55": "248",
        "56": "249",
        "57": "256",
        "58": "262",
        "59": "269",
        "60": "276",
        "61": "277",
        "62": "284",
        "63": "290",
        "64": "297",
        "65": "304",
        "66": "305",
        "67": "312",
        "68": "319",
        "69": "326",
        "70": "333",
        "71": "334",
        "72": "341",
        "73": "348",
        "74": "354",
        "75": "361",
        "76": "362",
        "77": "369",
        "78": "376",
        "79": "382",
        "80": "389",
        "81": "390",
        "82": "397",
        "83": "404",
        "84": "411",
        "85": "418",
        "86": "419",
        "87": "426",
        "88": "432",
        "89": "439",
        "90": "446",
        "91": "447",
        "92": "454",
        "93": "460",
        "94": "467",
        "95": "474",
        "96": "475",
        "97": "482",
        "98": "489",
        "99": "496",
        "100": "503",
        "101": "504",
        "102": "511",
        "103": "518",
        "104": "524",
        "105": "531",
        "106": "532",
        "107": "539",
        "108": "546",
        "109": "552",
        "110": "559",
        "111": "560",
        "112": "567",
        "113": "574",
        "114": "580",
        "115": "587",
        "116": "588",
        "117": "595",
        "118": "602",
        "119": "609",
        "120": "616",
        "121": "617",
        "122": "624",
        "123": "630",
        "124": "637",
        "125": "644",
        "126": "645",
        "127": "652",
        "128": "658",
        "129": "665",
        "130": "672",
        "131": "673",
        "132": "680",
        "133": "687",
        "134": "694",
        "135": "701",
        "136": "702",
        "137": "709",
        "138": "716",
        "139": "722",
        "140": "729",
        "141": "730",
        "142": "738",
        "143": "746",
        "144": "753",
        "145": "761",
        "146": "762",
        "147": "773",
        "148": "784",
        "149": "795",
        "150": "800",
    }
    hebscore, mathscore, engscore = rawscores
    hebscore = int(gradingkey[hebscore][0])
    mathscore = int(gradingkey[mathscore][0])
    engscore = int(gradingkey[engscore][0])
    totalscore = finalgradingkey[
        str(int((2 * hebscore + 2 * mathscore + engscore) / 5.0))
    ]
    totalhebscore = finalgradingkey[
        str(int((3 * hebscore + 1 * mathscore + engscore) / 5.0))
    ]
    totalmathscore = finalgradingkey[
        str(int((1 * hebscore + 3 * mathscore + engscore) / 5.0))
    ]
    return totalscore, totalmathscore, totalhebscore


# Cem Arkohen
# https://www.facebook.com/groups/772946566154452
def getgradingkey():
    global gradingkey
    return gradingkey


def preprocessing(filename):
    global gradingkey
    pagelist = {
        "1": [4, 11],
        "2": [12, 19],
        "3": [20, 27],
        "4": [28, 35],
        "5": [36, 43],
        "6": [44, 51],
    }  # splitchapters(reader)
    file = pdfopen(filename)
    pages = [file[i] for i in range(file.page_count)]
    gradingkey = extractgradingkey(pages[-3])
    pages = pages[:-3]
    answers, chapternames = getanswers(pages[-1])
    verify(chapternames, answers, pagelist)
    return answers, pagelist, gradingkey


def main(filename, saveslotnew):
    global gradingkey, saveslot
    saveslot = saveslotnew
    wipesaveslot(saveslot)
    pagelist = {
        "1": [4, 11],
        "2": [12, 19],
        "3": [20, 27],
        "4": [28, 35],
        "5": [36, 43],
        "6": [44, 51],
    }  # splitchapters(reader)
    file = pdfopen(filename)
    pages = [file[i] for i in range(file.page_count)]
    gradingkey = extractgradingkey(pages[-3])
    pages = pages[:-3]
    examnames = createchapterfiles(filename, pagelist)
    answers, chapternames = getanswers(pages[-1])
    verify(chapternames, answers, pagelist)
    trueanswerlist = savetrueanswers(answers, chapternames)
    return examnames, answers, chapternames, trueanswerlist


def mainfullexam(filename, saveslotnew):
    global gradingkey, saveslot
    saveslot = saveslotnew
    wipesaveslot(saveslot)
    foldername = filename + "\\"
    answers = pickle.load(open(foldername + "answers.txt", "rb"))
    gradingkey = pickle.load(open(foldername + "gradingkey.txt", "rb"))
    pagelist = pickle.load(open(foldername + "pagelist.txt", "rb"))
    file = pdfopen(foldername + "exam.pdf")
    examnames = createchapterfiles(foldername + "exam.pdf", pagelist)
    answers = [list(item) for item in answers]
    return (
        examnames,
        answers,
        classifychapters(answers),
        savetrueanswers(answers, classifychapters(answers)),
    )


def wipesaveslot(saveslot):
    for folder in os.listdir(saveslot):
        for file in os.listdir(saveslot + r"\\" + folder):
            os.remove(saveslot + r"\\" + folder + r"\\" + file)


def classifychapters(answerlist):
    list2 = []
    for item in answerlist:
        if "p" in item:
            list2.append(3)
        elif len(item) == 20:
            list2.append(1)
        elif len(item) == 22:
            list2.append(2)
        else:
            list2.append(0)
    return list2


def opendir(filename):
    unpack = filename.split("-")
    year = unpack[1]
    quarter = unpack[2][0]
    if os.path.isdir(r"C:\Users\Public\Appdata\Exams2\\" + year):
        if os.path.isdir(r"C:\Users\Public\Appdata\Exams2\\" + year + "\\" + quarter):
            pass
        else:
            os.mkdir(r"C:\Users\Public\Appdata\Exams2\\" + year + "\\" + quarter)
    else:
        os.mkdir(r"C:\Users\Public\Appdata\Exams2\\" + year)
        os.mkdir(r"C:\Users\Public\Appdata\Exams2\\" + year + "\\" + quarter)

    return r"C:\Users\Public\Appdata\Exams2\\" + year + "\\" + quarter


def picklesave(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    for yearfolder in os.listdir(r"C:\Users\Public\Appdata\Exams\Hebrew"):
        for pdffile in os.listdir(
            r"C:\Users\Public\Appdata\Exams\Hebrew" + "\\" + yearfolder
        ):
            answer, pagelist, gradingkey = preprocessing(
                r"C:\Users\Public\Appdata\Exams\Hebrew"
                + "\\"
                + yearfolder
                + "\\"
                + pdffile
            )
            dirpath = opendir(
                r"C:\Users\Public\Appdata\Exams\Hebrew"
                + "\\"
                + yearfolder
                + "\\"
                + pdffile
            )
            picklesave(answer, dirpath + r"\\answers.txt")
            picklesave(pagelist, dirpath + r"\\pagelist.txt")
            picklesave(gradingkey, dirpath + r"\\gradingkey.txt")
            shutil.copy(
                r"C:\Users\Public\Appdata\Exams\Hebrew"
                + "\\"
                + yearfolder
                + "\\"
                + pdffile,
                dirpath + r"\\exam.pdf",
            )
