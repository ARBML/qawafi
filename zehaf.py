import copy


class BaseEllahZehaf:
    def __init__(self, tafeela):
        self.tafeela = copy.deepcopy(tafeela)


class NoZehafNorEllah(BaseEllahZehaf):
    @property
    def modified_tafeela(self):
        return self.tafeela


class HazfZehaf(BaseEllahZehaf):
    affected_index = None

    @property
    def modified_tafeela(self):
        if hasattr(self, "assertions"):
            assert all(self.assertions), "assertions failed"
        self.tafeela.delete_from_tafeela_pattern(self.affected_index)
        return self.tafeela


class TaskeenZehaf(BaseEllahZehaf):
    affected_index = None

    @property
    def modified_tafeela(self):
        assert (
            self.tafeela.pattern[self.affected_index] == 1
        ), f"tafeela pattern index {self.affected_index} should be sakin"
        self.tafeela.pattern[self.affected_index] = 0
        return self.tafeela


class Khaban(HazfZehaf):
    affected_index = 1


class Tay(HazfZehaf):
    affected_index = 4


class Waqas(HazfZehaf):
    affected_index = 1


class Qabadh(HazfZehaf):
    affected_index = 4


class Kaff(HazfZehaf):
    affected_index = 6


class Akal(HazfZehaf):
    affected_index = 4


class Edmaar(TaskeenZehaf):
    affected_index = 1


class Asab(TaskeenZehaf):
    affected_index = 4


"""DOUBLED ZEHAFS"""


class BaseDoubledZehaf(BaseEllahZehaf):
    zehafs = []

    @property
    def modified_tafeela(self):
        assert len(self.zehafs) == 2, "maximum allowed zehafs should be 2"
        hazf_zehafs = filter(lambda zehaf: isinstance(zehaf, HazfZehaf), self.zehafs)
        taskeen_zehafs = filter(
            lambda zehaf: isinstance(zehaf, TaskeenZehaf), self.zehafs,
        )
        for zehaf in taskeen_zehafs:
            self.tafeela = zehaf.modified_tafeela
        # https://stackoverflow.com/a/28697246/4412324
        deletion_indices = sorted(
            [zehaf.affected_index for zehaf in hazf_zehafs], reverse=True,
        )
        for index in deletion_indices:
            del self.tafeela.pattern[index]


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
