import os
import pickle

from pymupdf import open as pdfopen

saveslot = ""

def givefinalscores(rawscores,gradingkey):
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
    mathscore = int(gradingkey[mathscore][1])
    engscore = int(gradingkey[engscore][2])
    totalscore = finalgradingkey[str(int((2 * hebscore + 2 * mathscore + engscore) / 5.0))]
    totalhebscore = finalgradingkey[str(int((3 * hebscore + 1 * mathscore + engscore) / 5.0))]
    totalmathscore = finalgradingkey[str(int((1 * hebscore + 3 * mathscore + engscore) / 5.0))]
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
        if folder != "images":
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

'''
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
'''

def main(filename, saveslotnew):
    global gradingkey, saveslot
    saveslot = saveslotnew
    wipesaveslot(saveslot)
    foldername = filename + "\\"
    answers = pickle.load(open(foldername + "answers.txt", "rb"))
    pagelist = pickle.load(open(foldername + "pagelist.txt", "rb"))
    examnames = createchapterfiles(foldername + "exam.pdf", pagelist)
    grading_key=pickle.load(open(foldername + "gradingkey.txt", "rb"))
    grading_key_save_location=saveslot + "\\Grade\gradingkey.txt"
    grading_key_save_file=open(grading_key_save_location,"wb")
    pickle.dump(grading_key,grading_key_save_file)
    answers = [list(item) for item in answers]
    true_answers_dir=savetrueanswers(answers, classifychapters(answers))
    print(true_answers_dir)
    true_answers=[pickle.load(open(filename,"rb")) for filename in true_answers_dir]
    return (
        examnames,
        answers,
        true_answers_dir,
        true_answers

    )


def mainresume(saveslotnew):
    global gradingkey,saveslot
    saveslot=saveslotnew
    #parent_dir=os.path.dirname(os.path.abspath(__file__))+"\\Data\\"
    save_folder = saveslot + "\\"
    answers_dir = save_folder + "Answers\\"
    chapters_dir = save_folder + "Chapters\\"
    trueanswers_dir = save_folder + "Trueanswers\\"
    len_answers = len(os.listdir(answers_dir))
    combined_answers = [pickle.load(open(answers_dir + str(i) + ".txt", "rb")) for i in range(len_answers)]
    combined_trueanswers = [pickle.load(open(trueanswers_dir + file_name, "rb")) for file_name in os.listdir(trueanswers_dir)]
    chapter_file_names=[chapters_dir+file_name for file_name in os.listdir(chapters_dir) ]
    return (chapter_file_names,
            combined_answers,
            combined_trueanswers,
            len_answers-1

    )
if __name__ == "__main__":
    main("C:\Temp\simtrue.pdf", "a")
