from diacritization_evaluation.util import extract_haraqat, combine_txt_and_haraqat

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
    "muqtatheb",
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


def override_auto_tashkeel(auto_diacritized_bait, user_diacritized_bait):
    _, user_undiacritized_bait, user_tashkeelat = extract_haraqat(user_diacritized_bait)
    _, auto_undiacritized_bait, auto_tashkeelat = extract_haraqat(auto_diacritized_bait)
    assert len(user_tashkeelat) == len(auto_tashkeelat)
    for index in range(len(user_tashkeelat)):
        if len(user_tashkeelat[index]) > 0:
            auto_tashkeelat[index] = user_tashkeelat[index]
    final_bait = combine_txt_and_haraqat(auto_undiacritized_bait, auto_tashkeelat)
    return final_bait


def override_auto_baits_tashkeel(auto_diacritized_baits, user_diacritized_baits):
    for auto_diacritized_bait, user_diacritized_bait in zip(
        auto_diacritized_baits, user_diacritized_baits
    ):
        pass
