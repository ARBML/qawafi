import random
import re

harakat = ["\u0650", "\u064E", "\u064F"]  # [kasra, fatha, damma, ]
sukun = ["\u0652"]  # [sukun]
mostly_saken = [
    "\u0627",
    "\u0648",
    "\u0649",
    "\u064A",
]  # [alef, waw, alef maqsurah, ya'a]
tnween_chars = [
    "\u064c",
    "\u064d",
    "\u064b",
]  # damm tanween, kasra tanween, fatha tanween, maddah
shadda_chars = ["\u0651"]
all_chars = list("إةابتثجحخدذرزسشصضطظعغفقكلمنهويىأءئؤ ")
prem_chars = harakat + sukun + mostly_saken + tnween_chars + shadda_chars + all_chars


def handle_space(plain_chars):
    if plain_chars[-1] == " ":
        return plain_chars[:-2]
    else:
        return plain_chars[:-1]

def remove_extra_harakat(pred):
    out = ""
    i = 0 
    while( i < len(pred)):
        if i < len(pred) - 1:
          if pred[i] in harakat and pred[i+1] in harakat:
            i += 1
            continue
        out += pred[i]
        i += 1
    return out

def extract_tf3eelav3(pred, verbose=False):
    pred = remove_extra_harakat(pred)
    chars = list(pred.replace("\u0622", "ءَا").strip())
    chars = [c for c in chars if c in prem_chars]
    chars = list(re.sub(" +", " ", "".join(chars).strip()))
    out = ""
    i = 0
    plain_chars = ""
    j = 0
    flag = True
    while i < len(chars) - 1 and flag:
        j += 1
        char = chars[i]
        if verbose:
            print(char)
        # plain_chars += char
        if char in all_chars:
            if char == " ":
                plain_chars += char
                i += 1
                continue
            # set up some vars
            next_char = chars[i + 1]
            if next_char == " ":
                next_char = chars[i + 2]
            if i < len(chars) - 2:
                next_next_char = chars[i + 2]
            if len(out) > 0:
                prev_char = out[-1]
            else:
                prev_char = ""
            # ----------------------
            if next_char in harakat:
                # print('next char is ',next_char,'prev char',prev_char)
                # print('-'*20)
                # print('char is',char)
                # print('next char is',next_char)
                # print('plain chars is',plain_chars)
                # print('out is',out)
                # print('-'*20)
                out += "1"
                plain_chars += char
            elif next_char in sukun:
                if prev_char != "0":
                    out += "0"
                    plain_chars += char
                elif (i + 1) == len(chars) - 1:
                    # print('next char is ',next_char,'prev char',prev_char)
                    # print('-'*20)
                    # print('char is',char)
                    # print('next char is',next_char)
                    # print('plain chars is',plain_chars)
                    # print('out is',out)
                    # print('-'*20)
                    out = out[:-1] + "10"
                    plain_chars += char
                else:
                    plain_chars = handle_space(plain_chars) + char
            elif next_char in tnween_chars:
                if char != "ا":
                    plain_chars += char
                plain_chars += "ن"
                out += "10"
            elif next_char in shadda_chars:
                """added characters"""
                # 1
                if prev_char != "0":
                    plain_chars += char
                    plain_chars += char
                    out += "01"
                else:
                    # print('next char is ',next_char,'prev char',prev_char)
                    # print('-'*20)
                    # print('char is',char)
                    # print('next char is',next_char)
                    # print('plain chars is',plain_chars)
                    # print('out is',out)
                    # print('-'*20)
                    plain_chars = handle_space(plain_chars) + char + char
                    out += "1"
                if i + 2 < len(chars):  # need to recheck this
                    if (
                        chars[i + 2] in harakat
                    ):  # in case shaddah not followed by harakah
                        i += 1
                    elif (
                        chars[i + 2] in tnween_chars
                    ):  # in case shaddah is followed by tanween
                        i += 1
                        # plain_chars += char
                        plain_chars += "ن"
                        # out += '10'
                        out += "0"
            elif next_char in all_chars:
                if prev_char != "0":
                    out += "0"
                    plain_chars += char
                elif prev_char == "0" and chars[i + 1] == " ":
                    out += "1"
                    plain_chars += char
                else:
                    plain_chars = handle_space(plain_chars) + char
                    # plain_chars += char
                i -= 1
            if next_next_char == " ":
                if char == "ه":
                    if next_char == harakat[0]:
                        plain_chars += "ي"
                        out += "0"
                    if next_char == harakat[2]:
                        plain_chars += "و"
                        out += "0"
            i += 2
        if j > 2 * len(chars):
            print("something might be wrong!")
            flag = False
            
    # if chars[-1] in all_chars:
    #   if out[-1] == '1':
    #     out += '0'
    #   else:
    #     out += '1'
    # print('next char is ',next_char,'prev char',prev_char)
    # print('-'*20)
    # print('char is',char)
    # print('next char is',next_char)
    # print('plain chars is',plain_chars)
    # print('out is',out)
    # print('-'*20)
    if out[-1] != "0":
        out += "0"  # always add sukun to the end of baits if mutaharek
    if chars[-1] == harakat[0]:
        plain_chars += "ي"
    elif chars[-1] == tnween_chars[1]:
        plain_chars = plain_chars[:-1] + "ي"
    elif chars[-1] == harakat[1]:
        plain_chars += "ا"
    elif chars[-1] == harakat[2]:
        plain_chars += "و"
    elif chars[-1] == tnween_chars[0]:
        plain_chars = plain_chars[:-1] + "و"
    elif chars[-1] in "ىاوي" and chars[-2] not in tnween_chars:
        plain_chars += chars[-1]
    # if out[-1] != '0': #always add sukun to the end of baits if mutaharek
    #   out += '0'
    plain_chars_no_space = plain_chars.replace(" ", "")
    # assert len(plain_chars_no_space) == len(
    #     out
    # ), f"{len(plain_chars_no_space)},{len(out)},\n{plain_chars}\n{out}"
    return plain_chars, out


def process_specials_before(bait):
    if bait[0] == "ا":
        bait = random.choice(["أَ", "إِ"]) + bait[1:]
    bait = bait.replace("وا ", "و ")
    if bait.find("وا") == len(bait) - 2:
        bait = bait[:-1]
    bait = bait.replace("وْا", "و")
    if bait.find("وْا") == len(bait) - 2:
        bait = bait[:-2] + "و"
    bait = bait.replace("الله", "اللاه")
    bait = bait.replace("اللّه", "الله")
    bait = bait.replace("إلَّا", "إِلّا")
    bait = bait.replace("نْ ال", "نَ ال")
    bait = bait.replace("لْ ال", "لِ ال")
    bait = bait.replace("إلَى", "إِلَى")
    bait = bait.replace("إذَا", "إِذَا")
    bait = bait.replace("ك ", "كَ ")
    bait = bait.replace(" ال ", " الْ ")
    bait = bait.replace("ْ ال", "ِ ال")
    for i in range(len(bait) - 2):
        if bait[i] in sukun:
            if bait[i + 2] in sukun:
                bait = bait[: i + 2] + random.choice(harakat) + bait[i + 3 :]
    # check tanween fath not being at last of the word
    if bait.find(tnween_chars[2]) != -1:
        tanween_index = bait.index(tnween_chars[2])
        if bait[tanween_index + 1] == "ا":
            bait = bait[:tanween_index] + tnween_chars[2] + bait[tanween_index + 2 :]
    return bait


def process_specials_after(bait):
    bait = bait.replace("ةن", "تن")
    # bait = bait.replace('ةي','تن')
    return bait


def get_arudi_style(baits):
    results = []
    for bait in baits:
        arudi_style, pattern = extract_tf3eelav3(process_specials_before(bait))
        results.append([process_specials_after(arudi_style), pattern])
    return results
