import pyarabic.araby as araby

remove_tashkeel = lambda text: araby.strip_tashkeel(text)
remove_tatweel = lambda text: araby.strip_tatweel(text)
accepted_chars = list("إةابتثجحخدذرزسشصضطظعغفقكلمنهويىأءئؤ#آ َِْ ")
remove_unaccepted_chars = lambda text: "".join(c for c in text if c in accepted_chars)
normalize = lambda text: remove_tashkeel(
    remove_tatweel(remove_unaccepted_chars(text))
).strip()

FATHA = "َ"
SUKUN = "ْ"


def get_rawwy_char(bait, with_index=False):
    """
    This method returns the last char in the bait
    """
    clean_bait = normalize(bait)
    i = -1
    while True:
        last_char = clean_bait[i]
        second_last_char = clean_bait[i - 1]
        if second_last_char == "آ":
            second_last_char = "ا"
        last_two_chars = "".join(clean_bait[i - 1 :])
        i -= 1
        """catch exceptions"""
        if last_two_chars in ("يا", "يه", "ية"):
            if with_index:
                return "ي", len(clean_bait) + i
            return "ي"
        if last_char == "ا":
            continue
        if last_char == "ه" or last_char == "ة":
            if second_last_char not in "اوي":
                continue
        if last_char == "ي":
            continue
        if last_char == "ى":
            continue
        if last_char == "و":
            continue
        if last_char == "ك":
            if second_last_char not in "اوي":
                continue
        """unify rawwy"""
        if last_char in "ؤئأء":
            last_char = "ء"
        if last_char in "هة":
            last_char = "ه"
        if with_index:
            return last_char, len(clean_bait) + i + 1
        return last_char


def get_qafiah_type(bait):
    clean_bait = normalize(bait)
    rawwy, rawwy_index = get_rawwy_char(bait, with_index=True)
    qafiyh_type = f"قافية بحرف الروي: {rawwy} ، "
    if rawwy_index == len(clean_bait) - 1 or (
        rawwy_index == len(clean_bait) - 2 and clean_bait[-1] in "ىاوي"
    ):
        if remove_unaccepted_chars(bait).strip()[-1] != SUKUN:
            remove_unaccepted_chars(bait).strip()[-1]
            qafiyh_type += " زاد لها الوصل بإشباع رويها"
    if (
        rawwy_index == len(clean_bait) - 2
        and clean_bait[-1] in "كهة"
        and remove_unaccepted_chars(bait).strip()[-1] == SUKUN
    ):
        qafiyh_type += f" زاد لها الوصل بـ: {clean_bait[-1]}"
    elif (
        rawwy_index == len(clean_bait) - 3
        and clean_bait[-2] in "كهة"
        and clean_bait[-1] in "اوي"
    ):
        qafiyh_type += f" زاد لها الوصل بـ: {clean_bait[-2]} والخَروج"

    elif (
        rawwy_index == len(clean_bait) - 2
        and clean_bait[-1] in "كهة"
        and remove_unaccepted_chars(bait).strip()[-1] != SUKUN
    ):
        qafiyh_type += " و زاد لها الوصل و الخَروج"

    if clean_bait[rawwy_index - 1] in "اويآى":
        qafiyh_type += " زاد لها الردف"
    elif clean_bait[rawwy_index - 2] in "اآ":
        qafiyh_type += " زاد لها التأسيس"
    return qafiyh_type


def get_qafiah_type_short(bait):
    clean_bait = normalize(bait)
    rawwy, rawwy_index = get_rawwy_char(bait, with_index=True)
    qafiyh_type = f""
    if rawwy_index == len(clean_bait) - 1 or (
        rawwy_index == len(clean_bait) - 2 and clean_bait[-1] in "ىاوي"
    ):
        if remove_unaccepted_chars(bait).strip()[-1] != SUKUN:
            remove_unaccepted_chars(bait).strip()[-1]
            qafiyh_type += "الوصل "
    if (
        rawwy_index == len(clean_bait) - 2
        and clean_bait[-1] in "كهة"
        and remove_unaccepted_chars(bait).strip()[-1] == SUKUN
    ):
        qafiyh_type += f"الوصل "
    elif (
        rawwy_index == len(clean_bait) - 3
        and clean_bait[-2] in "كهة"
        and clean_bait[-1] in "اوي"
    ):
        qafiyh_type += f"الوصل والخَروج "

    elif (
        rawwy_index == len(clean_bait) - 2
        and clean_bait[-1] in "كهة"
        and remove_unaccepted_chars(bait).strip()[-1] != SUKUN
    ):
        qafiyh_type += "الوصل والخَروج "

    if clean_bait[rawwy_index - 1] in "اويآى":
        qafiyh_type += "والردف "
    elif clean_bait[rawwy_index - 2] in "اآ":
        qafiyh_type += "والتأسيس "
    return qafiyh_type


# from poem_samples_large import samples

# jump = 111
# for poem_index, sample in enumerate(samples[jump:]):
#     print("#" * 80)
#     print("poem index:", poem_index + jump)
#     for bait in sample:
#         print(bait)
#         print(get_rawwy_char(bait))
#         print(get_qafiah_type(bait))
#         print("-" * 40)
#     print("#" * 80)
#     try:
#         if int(input("enter 0 to go out")) == 0:
#             break
#     except ValueError as e:
#         pass


def get_qafiyah(baits, short=False):
    results = []
    get_qafiah = get_qafiah_type_short if short is True else get_qafiah_type
    for bait in baits:
        results.append((get_rawwy_char(bait), get_qafiah(bait)))
    return results
