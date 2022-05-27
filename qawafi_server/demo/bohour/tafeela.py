from bohour.zehaf import (
    Akal,
    Asab,
    Edmaar,
    Kaff,
    Khabal,
    Thalm,
    Khazal,
    Nakas,
    Qabadh,
    Khaban,
    Shakal,
    Tasheeth,
    Tay,
    Tharm,
    Waqas,
)

SUKUN_CHAR = "ْ"


class Tafeela:
    name = ""
    allowed_zehafs = list()
    pattern_int = 0
    applied_ella_zehaf_class = None

    def __init__(self, *args, **kwargs):
        self.original_pattern = list(map(int, str(self.pattern_int)))
        self.pattern = self.original_pattern[:]
        self._assert_length_consistency()
        self._manage_sukun_char()

    def _manage_sukun_char(self, deleted_char_index=None):
        clean_name = self.name.replace(SUKUN_CHAR, "")
        space_index = clean_name.find(" ") if " " in self.name else None
        clean_name = clean_name.replace(" ", "")
        new_name = ""
        assert len(self.pattern) == len(clean_name)
        for i, (pattern_num, char) in enumerate(zip(self.pattern, clean_name)):
            new_name += char
            if pattern_num == 1 or char in "اوي":
                continue
            new_name += SUKUN_CHAR
            if space_index and i != len(self.pattern) - 1:
                space_index += 1
        if space_index:
            new_name = new_name[:space_index] + " " + new_name[space_index:]
        self.name = new_name

    def _assert_length_consistency(self):
        assert (
            len(self.pattern)
            == len(self.name.replace(" ", "").replace(SUKUN_CHAR, ""))
            == len(str(self.pattern_int))
        ), "pattern and name should have the same length"

    def _delete_from_name(self, index):
        clean_name = self.name.replace(SUKUN_CHAR, "")
        if " " in self.name:
            space_index = clean_name.index(" ")
            if space_index < index:
                new_name = clean_name[: index + 1] + clean_name[index + 2 :]
            else:
                new_name = clean_name[:index] + clean_name[index + 1 :]
            self.name = new_name
        else:
            self.name = clean_name[:index] + clean_name[index + 1 :]

    def delete_from_pattern(self, index):
        del self.pattern[index]
        self._delete_from_name(index=index)
        self.pattern_int = int("".join(map(str, self.pattern)))
        self._assert_length_consistency()
        self._manage_sukun_char(deleted_char_index=index)

    def add_to_pattern(self, index, number, char_mask):
        self.pattern.insert(index, number)
        clean_name = self.name.replace(SUKUN_CHAR, "")
        self.name = clean_name[:index] + char_mask + clean_name[index:]
        self.pattern_int = int("".join(map(str, self.pattern)))
        self._assert_length_consistency()
        self._manage_sukun_char()

    def edit_pattern_at_index(self, index, number):
        self.pattern[index] = number
        self.pattern_int = int("".join(map(str, self.pattern)))
        self._assert_length_consistency()
        self._manage_sukun_char()

    def all_zehaf_tafeela_forms(self):
        forms = [self]
        for zehaf_class in self.allowed_zehafs:
            zehaf = zehaf_class(self)
            forms.append(zehaf.modified_tafeela)
        return forms

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class Fawlon(Tafeela):
    name = "فعولن"
    allowed_zehafs = [Qabadh, Thalm, Tharm]
    pattern_int = 11010


class Faelon(Tafeela):
    name = "فاعلن"
    allowed_zehafs = [Khaban, Tasheeth]
    pattern_int = 10110


class Mafaeelon(Tafeela):
    name = "مفاعيلن"
    allowed_zehafs = [Qabadh, Kaff]
    pattern_int = 1101010


class Mustafelon(Tafeela):
    name = "مستفعلن"
    allowed_zehafs = [Khaban, Tay, Khabal]
    pattern_int = 1010110


class Mutafaelon(Tafeela):
    name = "متفاعلن"
    allowed_zehafs = [Edmaar, Waqas, Khazal]
    # allowed_zehafs = [Edmaar]
    pattern_int = 1110110


class Mafaelaton(Tafeela):
    name = "مفاعلتن"
    # allowed_zehafs = [Asab, Akal, Nakas]
    allowed_zehafs = [Asab]
    pattern_int = 1101110


class Mafoolato(Tafeela):
    name = "مفعولات"
    allowed_zehafs = [Khaban, Tay, Khabal]
    pattern_int = 1010101


class Fae_laton(Tafeela):
    name = "فاع لاتن"
    allowed_zehafs = [Kaff]
    pattern_int = 1011010


class Mustafe_lon(Tafeela):
    name = "مستفع لن"
    allowed_zehafs = [Khaban, Kaff]
    pattern_int = 1010110


class Faelaton(Tafeela):
    name = "فاعلاتن"
    allowed_zehafs = [Khaban, Kaff, Shakal, Tasheeth]
    pattern_int = 1011010
