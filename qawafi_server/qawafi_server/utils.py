from diacritization_evaluation.util import extract_haraqat, combine_txt_and_haraqat
import difflib
from termcolor import colored
from pyarabic.araby import strip_tatweel
import re
from pprint import pprint
import pandas as pd

vocab = list("إةابتثجحخدذرزسشصضطظعغفقكلمنهويىأءئؤ#آ ")
vocab += list("ًٌٍَُِّ") + ["ْ"] + ["ٓ"]

BOHOUR_NAMES = [
    "saree",
    "kamel",
    "mutakareb",
    "mutadarak",
    "munsareh",
    "madeed",
    "mujtath",
    "ramal",
    "baseet",
    "khafeef",
    "taweel",
    "wafer",
    "hazaj",
    "rajaz",
    "mudhare",
    "muqtadheb",
    "nathr",
]
BOHOUR_NAMES_AR = [
    "السريع",
    "الكامل",
    "المتقارب",
    "المتدارك",
    "المنسرح",
    "المديد",
    "المجتث",
    "الرمل",
    "البسيط",
    "الخفيف",
    "الطويل",
    "الوافر",
    "الهزج",
    "الرجز",
    "المضارع",
    "المقتضب",
    "نثر",
]

char2idx = {u: i + 1 for i, u in enumerate(vocab)}

label2name = BOHOUR_NAMES_AR


def process_and_write(input):
    lines = input.split("\n")[1:-1]
    baits = []
    for i in range(len(lines) // 2):
        bait = " # ".join(lines[i * 2 : (i + 1) * 2])
        baits.append(bait)
    open("/content/qawafi/demo/baits_input.txt", "w").write("\n".join(baits))


def clean(text):
    return re.sub(" +", " ", strip_tatweel(text)).strip()


def override_auto_tashkeel(auto_diacritized_bait, user_diacritized_bait):
    _, user_undiacritized_bait, user_tashkeelat = extract_haraqat(user_diacritized_bait)
    _, auto_undiacritized_bait, auto_tashkeelat = extract_haraqat(auto_diacritized_bait)
    try:
        assert len(user_tashkeelat) == len(auto_tashkeelat)
    except Exception as e:
        print(len(user_tashkeelat), len(auto_tashkeelat))
        raise e
    for index in range(len(user_tashkeelat)):
        if len(user_tashkeelat[index]) > 0:
            auto_tashkeelat[index] = user_tashkeelat[index]
    final_bait = combine_txt_and_haraqat(auto_undiacritized_bait, auto_tashkeelat)
    return final_bait


def override_auto_baits_tashkeel(auto_diacritized_baits, user_diacritized_baits):
    overridden = list()
    for auto_diacritized_bait, user_diacritized_bait in zip(
        auto_diacritized_baits, user_diacritized_baits
    ):
        overridden.append(
            override_auto_tashkeel(
                auto_diacritized_bait,
                user_diacritized_bait,
            )
        )
    return overridden


###--- sequence matching ---###


def highlight_difference(colored_string):
    highlighted = ""
    for i in range(0, len(colored_string), 2):
        if colored_string[i] == "R":
            highlighted += colored(colored_string[i + 1], "red")
        elif colored_string[i] == "B":
            highlighted += colored(colored_string[i + 1], "blue")
        elif colored_string[i] == "Y":
            highlighted += colored(colored_string[i + 1], "yellow")
        elif colored_string[i] == "G":
            highlighted += colored(colored_string[i + 1], "green")
    return highlighted


def find_mismatch(a, b, highlight_output=True):
    # print("Y:flipped, R:Removed, B:Added, G:Correct")
    # print("origina: ", a)
    # print("Predict: ", b)
    out = ""
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] != b[i]:
                out += "Y" + str(b[i])
            else:
                out += "G" + str(b[i])
    else:
        s = difflib.SequenceMatcher(None, a, b)

        b_block = []
        a_block = []

        for block in s.get_matching_blocks():
            a_block += list(range(block.a, block.a + block.size))
            b_block += list(range(block.b, block.b + block.size))

        added_indices = set(list(range(len(b)))).difference(set(b_block))
        removed_indices = set(list(range(len(a)))).difference(set(a_block))

        i = 0
        while i < len(b):
            if i in removed_indices:
                out += "B" + str(a[i])
                removed_indices.remove(i)
                continue
            elif i in added_indices:
                out += "R" + str(b[i])
            else:
                out += "G" + str(b[i])
            i += 1
        if len(removed_indices) > 0:
            for i in removed_indices:
                out += "B" + str(a[i])
    if highlight_output:
        return highlight_difference(out)
    return out


def find_baits_mismatch(gold_patterns, predicted_patterns, highlight_output=True):
    baits_mismatch = list()
    for gold_pattern, predicted_pattern in zip(gold_patterns, predicted_patterns):
        if len(gold_pattern) * len(predicted_patterns) == 0:
            baits_mismatch.append("")
        else:
            baits_mismatch.append(
                find_mismatch(
                    gold_pattern,
                    predicted_pattern,
                    highlight_output,
                )
            )
    return baits_mismatch


def beautiful_print(output):
    for key in output:
        print(key)
        if key == "patterns_mismatches":
            for mismatch in output[key]:
                print(mismatch)
        elif key == "diacritized":
            for diac_bait in output[key]:
                print(diac_bait)
        elif key == "closest_baits":
            for mismatch in output[key]:
                print(mismatch[-1])
        else:
            pprint(output[key])


def get_output_df(output):
    baits_df = {"المشكل": [], "الكتابة العروضية": [], "التفعيله": [], "النمط": []}
    poems_df = {"البحر": [], "الحقبة الزمنية": [], "العاطفة": [], "القافية": []}
    full_df = {**baits_df, **poems_df}
    for key in ["diacritized", "arudi_style", "meter", "era", "theme", "qafiyah"]:
        if key == "arudi_style":
            for style, mismatch, pattern in zip(
                output[key], output["patterns_mismatches"], output["closest_patterns"]
            ):
                full_df["الكتابة العروضية"].append(style[0])
                full_df["التفعيله"].append(pattern[-1])
                full_df["النمط"].append(mismatch)

        elif key == "diacritized":
            for diac_bait in output[key]:
                for shatr in diac_bait.split("#"):
                    full_df["المشكل"].append(shatr.strip())
        elif key == "closest_baits":
            for bait in output[key]:
                for shatr in bait[0][0].split("#"):
                    full_df["أقرب بيت"].append(shatr.strip())
        elif key == "meter":
            for i in range(len(output["arudi_style"])):
                if i == 0:
                    full_df["البحر"].append(output[key])
                else:
                    full_df["البحر"].append("")
        elif key == "era":
            for i in range(len(output["arudi_style"])):
                if i == 0:
                    full_df["الحقبة الزمنية"].append(output[key][0])
                else:
                    full_df["الحقبة الزمنية"].append("")
        elif key == "theme":
            for i in range(len(output["arudi_style"])):
                if i == 0:
                    full_df["العاطفة"].append(output[key][0])
                else:
                    full_df["العاطفة"].append("")
        elif key == "qafiyah":
            for i in range(len(output["arudi_style"])):
                if i == 0:
                    full_df["القافية"].append(" ".join(output[key]))
                else:
                    full_df["القافية"].append("")
    return pd.DataFrame(full_df)


def process_and_write(input, output_file_path="/content/baits_input.txt"):
    lines = input.split("\n")[1:-1]
    baits = []
    for i in range(len(lines) // 2):
        bait = " # ".join(lines[i * 2 : (i + 1) * 2])
        baits.append(bait)
    open(output_file_path, "w").write("\n".join(baits))


import re
from IPython.display import HTML


def process_colors(pattern):
    out = ""
    map_colors = {"R": "#EB5353", "G": "#36AE7C", "B": "#187498", "Y": "#F9D923"}
    for i in range(len(pattern) // 2):
        color = pattern[2 * i]
        bit = pattern[2 * i + 1]
        out += f'<span style="color: {map_colors[color]}">{bit}</span>'
    return out


def display_highlighted_patterns(df):
    head = (
        """
    <html>
    <head>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #555555;
    }
    </style>
    </head>

    <table>
        <thead>
            """
        + "".join(["<th> %s </th>" % c for c in df.columns])
        + """
        </thead>
    <tbody>"""
    )
    for i, r in df.iterrows():
        row = "<tr>"
        for c in list(df.columns):
            if c == "النمط":
                row += "<td> %s </td>" % process_colors(r[c])
            else:
                row += "<td> %s </td>" % r[c]
        row += "</tr>"
        head += row

    head += "</tbody></table></html>"
    display(HTML(head))
