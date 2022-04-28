import copy


class BaseEllahZehaf:
    def __init__(self, tafeela):
        self.tafeela = copy.deepcopy(tafeela)

    def modify_tafeela(self):
        """This method needs to be overridden. If not, it will return the tafeela unchanged"""

    @property
    def modified_tafeela(self):
        if hasattr(self, "assertions"):
            assert all(self.assertions), "assertions failed"
        self.modify_tafeela()
        self.tafeela.applied_zehaf = self.__class__
        return self.tafeela


class NoZehafNorEllah(BaseEllahZehaf):
    @property
    def modified_tafeela(self):
        self.tafeela.applied_zehaf = None
        return self.tafeela


class BaseHazfZehaf(BaseEllahZehaf):
    affected_index = None

    def modify_tafeela(self):
        self.tafeela.delete_from_pattern(self.affected_index)


class BaseTaskeenZehaf(BaseEllahZehaf):
    affected_index = None

    def modify_tafeela(self):
        assert (
            self.tafeela.pattern[self.affected_index] == 1
        ), f"tafeela pattern index {self.affected_index} should be sakin"
        self.tafeela.edit_pattern_at_index(index=self.affected_index, number=0)


class Khaban(BaseHazfZehaf):
    affected_index = 1


class Tay(BaseHazfZehaf):
    affected_index = 4


class Waqas(BaseHazfZehaf):
    affected_index = 1


class Qabadh(BaseHazfZehaf):
    affected_index = 4


class Kaff(BaseHazfZehaf):
    affected_index = 6


class Akal(BaseHazfZehaf):
    affected_index = 4


class Edmaar(BaseTaskeenZehaf):
    affected_index = 1


class Asab(BaseTaskeenZehaf):
    affected_index = 4


"""DOUBLED ZEHAFS"""


class BaseDoubledZehaf(BaseEllahZehaf):
    zehafs = []

    def modify_tafeela(self):
        assert len(self.zehafs) == 2, "maximum allowed zehafs should be 2"
        hazf_zehafs = filter(
            lambda zehaf: isinstance(zehaf, BaseHazfZehaf), self.zehafs
        )
        taskeen_zehafs = filter(
            lambda zehaf: isinstance(zehaf, BaseTaskeenZehaf),
            self.zehafs,
        )
        # https://stackoverflow.com/a/28697246/4412324
        deletion_indices = sorted(
            [zehaf.affected_index for zehaf in hazf_zehafs],
            reverse=True,
        )
        for index in deletion_indices:
            del self.tafeela.pattern[index]
        for zehaf in taskeen_zehafs:
            self.tafeela = zehaf.modified_tafeela


class Khabal(BaseDoubledZehaf):
    zehafs = [Khaban, Tay]


class Khazal(BaseDoubledZehaf):
    zehafs = [Edmaar, Tay]


class Shakal(BaseDoubledZehaf):
    zehafs = [Khaban, Kaff]


class Nakas(BaseDoubledZehaf):
    zehafs = [Asab, Kaff]


## Added Ellal


class Hadhf(BaseEllahZehaf):
    """حذف السبب الأخير"""

    def modify_tafeela(self):
        assert self.tafeela.pattern[-2:] == [
            1,
            0,
        ], "last two items of the tafeela pattern should be 1,0"
        for _ in range(2):
            self.tafeela.delete_from_pattern(index=len(self.tafeela.pattern) - 1)


# class Qasar(BaseEllahZehaf):
#     """حذف الساكن الأخير وتسكين ما قبله"""

#     def modify_tafeela(self):
#         assert (
#             self.tafeela.pattern[-1] == 0 and self.tafeela.pattern[-2] == 1
#         ), f"last tow items of tafeela {self.tafeela} should be 0,1"
#         self.tafeela.delete_from_pattern(index=len(self.tafeela.pattern) - 1)
#         self.tafeela.pattern[-1] = 0


class HadhfAndKhaban(BaseEllahZehaf):
    """الحذف والخبن معا"""

    def modify_tafeela(self):
        # hadhf
        hadhf = Hadhf(self.tafeela)
        self.tafeela = hadhf.modified_tafeela
        # khaban
        kaban = Khaban(self.tafeela)
        self.tafeela = kaban.modified_tafeela


class Qataf(BaseEllahZehaf):
    def modify_tafeela(self):
        # hadhf
        hadhf = Hadhf(self.tafeela)
        self.tafeela = hadhf.modified_tafeela
        # asab
        asab = Asab(self.tafeela)
        self.tafeela = asab.modified_tafeela


class Qataa(BaseEllahZehaf):
    """حذف آخر الوتد المجموع وتسكين ما قبله"""

    """
    هو ذات القصر، 
    لكنه اصطلاح آخر للتفريق بين التفعيلة التي آخرها وتد مجموع أو أخرها سبب خفيف
    """

    def modify_tafeela(self):
        assert (
            self.tafeela.pattern[-1] == 0 and self.tafeela.pattern[-2] == 1
        ), f"last tow items of tafeela {self.tafeela} should be 0,1"
        self.tafeela.delete_from_pattern(index=len(self.tafeela.pattern) - 1)
        self.tafeela.edit_pattern_at_index(
            index=len(self.tafeela.pattern) - 1,
            number=0,
        )


class Tatheel(BaseEllahZehaf):
    """زيادة حرف ساكن على آخر الوتد المجموع"""

    def modify_tafeela(self):
        """
        technically, we should add to the last.
         However, after adding we need to change
         the one to last character, usually 'noon', to 'alef'.
         we thought we just add 'alef' before last and that is it.
        """
        assert self.tafeela.pattern[-3:] == [
            1,
            1,
            0,
        ], f"tafeela {self.tafeela}'s pattern should end with 1,1,0"
        self.tafeela.add_to_pattern(
            index=len(self.tafeela.pattern) - 1, number=0, char_mask="ا"
        )


class Tasbeegh(BaseEllahZehaf):
    """زيادة حرف ساكن على آخر السبب الخفيف"""

    def modify_tafeela(self):
        """
        technically, we should add to the last.
         However, after adding we need to change
         the one to last character, usually 'noon', to 'alef'.
         we thought we just add 'alef' before last and that is it.
        """
        assert self.tafeela.pattern[-2:] == [
            1,
            0,
        ], f"tafeela {self.tafeela}'s pattern should end with 1,0"
        self.tafeela.add_to_pattern(
            index=len(self.tafeela.pattern) - 1, number=0, char_mask="ا"
        )


class TatheelAndEdmaar(BaseEllahZehaf):
    def modify_tafeela(self):
        # Tatheel
        tatheel = Tatheel(self.tafeela)
        self.tafeela = tatheel.modified_tafeela
        # Edmaar
        edmaar = Edmaar(self.tafeela)
        self.tafeela = edmaar.modified_tafeela


class Tarfeel(BaseEllahZehaf):
    """زيادة سبب خفيف"""

    def modify_tafeela(self):
        for number, char_mask in zip((1, 0), "تن"):
            self.tafeela.add_to_pattern(
                index=len(self.tafeela.pattern) - 1,
                number=number,
                char_mask=char_mask,
            )
            """change the originally last noon to alef to make the tafeela more familiar"""
            # self.tafeela.name = self.tafeela.name[:-3] + "ا" + self.tafeela.name[-3:]


class TarfeelAndEdmaar(BaseEllahZehaf):
    def modify_tafeela(self):
        # Tarfeel
        tarfeel = Tarfeel(self.tafeela)
        self.tafeela = tarfeel.modified_tafeela
        # Edmaar
        edmaar = Edmaar(self.tafeela)
        self.tafeela = edmaar.modified_tafeela


class KhabanAndQataa(BaseEllahZehaf):
    """الخبن والقطع معا"""

    def modify_tafeela(self):
        # hadhf
        qataa = Qataa(self.tafeela)
        self.tafeela = qataa.modified_tafeela
        # khaban
        kaban = Khaban(self.tafeela)
        self.tafeela = kaban.modified_tafeela


class QataaAndEdmaar(BaseEllahZehaf):
    def modify_tafeela(self):
        # Qataa
        qataa = Qataa(self.tafeela)
        self.tafeela = qataa.modified_tafeela
        # Edmaar
        edmaar = Edmaar(self.tafeela)
        self.tafeela = edmaar.modified_tafeela


class Hathath(BaseEllahZehaf):
    def modify_tafeela(self):
        assert self.tafeela.pattern[-3:] == [
            1,
            1,
            0,
        ], f"{self.tafeela}'s pattern should end with 1,1,0"
        for _ in range(3):
            index = len(self.tafeela.pattern) - 1
            self.tafeela.delete_from_pattern(index=index)


class HathathAndEdmaar(BaseEllahZehaf):
    def modify_tafeela(self):
        # Hathath
        hathath = Hathath(self.tafeela)
        self.tafeela = hathath.modified_tafeela
        # Edmaar
        edmaar = Edmaar(self.tafeela)
        self.tafeela = edmaar.modified_tafeela


class Salam(BaseEllahZehaf):
    """حذف الوتد المفروق الأخير من التفعيلة"""

    def modify_tafeela(self):
        assert self.tafeela.pattern[-3:] == [
            1,
            0,
            1,
        ], f"tafeela {self.tafeela}'s pattern should end with 1,0,1"
        for _ in range(3):
            index = len(self.tafeela.pattern) - 1
            self.tafeela.delete_from_pattern(index=index)


class Waqf(BaseEllahZehaf):
    """تسكين أخر الوتد المفروق من آخر التفعيلة"""

    def modify_tafeela(self):
        assert self.tafeela.pattern[-3:] == [
            1,
            0,
            1,
        ], f"tafeela {self.tafeela}'s pattern should end with 1,0,1"
        self.tafeela.edit_pattern_at_index(
            index=len(self.tafeela.pattern) - 1,
            number=0,
        )


class WaqfAndTay(BaseEllahZehaf):
    def modify_tafeela(self):
        # Tay
        tay = Tay(self.tafeela)
        self.tafeela = tay.modified_tafeela
        # Waqf
        waqf = Waqf(self.tafeela)
        self.tafeela = waqf.modified_tafeela
