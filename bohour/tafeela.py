from bohour.zehaf import (
    Akal,
    Asab,
    Edmaar,
    Kaff,
    Khabal,
    Khazal,
    Nakas,
    Qabadh,
    Khaban,
    Shakal,
    Tay,
    Waqas,
)


class Tafeela:
    name = ""
    allwed_zehafs = list()
    pattern_int = 0

    def __init__(self, *args, **kwargs):
        self.original_pattern = list(map(int, str(self.pattern_int)))
        self.pattern = self.original_pattern[:]
        self._assert_length_consistency()

    def _assert_length_consistency(self):
        assert (
            len(self.pattern)
            == len(self.name.replace(" ", ""))
            == len(str(self.pattern_int))
        ), "pattern and name should have the same length"

    def delete_from_pattern(self, index):
        del self.pattern[index]
        self.name = self.name[:index] + self.name[index + 1 :]
        self.pattern_int = int("".join(map(str, self.pattern)))
        self._assert_length_consistency()

    def add_to_pattern(self, index, number, char_mask):
        self.pattern.insert(index, number)
        self.name = self.name[:index] + char_mask + self.name[index:]
        self.pattern_int = int("".join(map(str, self.pattern)))
        self._assert_length_consistency()

    def edit_pattern_at_index(self, index, number):
        self.pattern[index] = number
        self.pattern_int = int("".join(map(str, self.pattern)))
        self._assert_length_consistency

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
    allowed_zehafs = [Qabadh]
    pattern_int = 11010


class Faelon(Tafeela):
    name = "فاعلن"
    allowed_zehafs = [Khaban]
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
    pattern_int = 1110110


class Mafaelaton(Tafeela):
    name = "مفاعلتن"
    allowed_zehafs = [Asab, Akal, Nakas]
    pattern_int = 1101110


class Mafoolato(Tafeela):
    name = "مفعولات"
    allowed_zehafs = [Khaban, Tay]
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
    allowed_zehafs = [Khaban, Kaff, Shakal]
    pattern_int = 1011010
