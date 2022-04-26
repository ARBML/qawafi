import copy


class BaseEllahZehaf:
    def __init__(self, tafeela):
        self.tafeela = copy.deepcopy(tafeela)

    def modify_tafeela(self):
        """This method needs to be overridden. If not, it will return the tafeela unchanged"""

    @property
    def modified_tafeela(self):
        assert (
            self.__class__ in self.tafeela.allowed_zehafs
            or self.__class__ in self.tafeela.allowed_ellas
            or self.__class__ in self.tafeela.allowed_dharbs
            or self.__class__.__name__ == "NoZehafNorEllah"
        ), f"The zehaf/ella/dharb {self.__class__.__name__} is not allowed for {self.tafeela}"
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
            lambda zehaf: isinstance(zehaf, BaseTaskeenZehaf), self.zehafs,
        )
        # https://stackoverflow.com/a/28697246/4412324
        deletion_indices = sorted(
            [zehaf.affected_index for zehaf in hazf_zehafs], reverse=True,
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

    @property
    def modified_tafeela(self):
        assert self.tafeela.pattern[-2:] == [1, 0], "assertions failed"
        for _ in range(2):
            self.tafeela.delete_from_tafeela_pattern(
                index=len(self.tafeela.pattern) - 1
            )
        return self.tafeela
