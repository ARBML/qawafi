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
    bait = ' # '.join(lines[i*2:(i+1)*2])
    baits.append(bait)
  open('/content/qawafi/demo/baits_input.txt', 'w').write('\n'.join(baits))