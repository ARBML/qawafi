from bohour.zehaf import (
    Akal,
    Asab,
    Edmaar,
    Hadhf,
    HadhfAndKhaban,
    Hathath,
    HathathAndEdmaar,
    Kaff,
    Khabal,
    KhabanAndQataa,
    Khazal,
    Nakas,
    Qabadh,
    Khaban,
    Qataa,
    QataaAndEdmaar,
    Qataf,
    Shakal,
    Tarfeel,
    TarfeelAndEdmaar,
    Tasheeth,
    Tatheel,
    TatheelAndEdmaar,
    Tay,
    Waqas,
)


class Tafeela:
    name = ""
    allwed_zehafs = list()
    pattern_int = 0
    applied_zehaf = None

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

    def _delete_from_name(self, index):
        if " " in self.name:
            non_spaced_name = self.name.replace(" ", "")
            new_name = non_spaced_name[:index] + non_spaced_name[index + 1 :]
            space_index = self.name.index(" ")
            new_name = new_name[:space_index] + " " + new_name[space_index:]
            self.name = new_name
        else:
            self.name = self.name[:index] + self.name[index + 1 :]

    def delete_from_pattern(self, index):
        del self.pattern[index]
        self._delete_from_name(index=index)
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
    # allowed_zehafs = [Edmaar, Waqas, Khazal]
    allowed_zehafs = [Edmaar]
    pattern_int = 1110110


class Mafaelaton(Tafeela):
    name = "مفاعلتن"
    # allowed_zehafs = [Asab, Akal, Nakas]
    allowed_zehafs = [Asab]
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
    # allowed_zehafs = [Khaban, Kaff, Shakal, Tasheeth]
    allowed_zehafs = [Khaban, Kaff]
    pattern_int = 1011010
