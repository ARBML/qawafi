import itertools


from bohour.tafeela import (
    Fae_laton,
    Faelaton,
    Faelon,
    Fawlon,
    Mafaeelon,
    Mafaelaton,
    Mafoolato,
    Mustafe_lon,
    Mustafelon,
    Mutafaelon,
)
from bohour.zehaf import (
    Asab,
    Hadhf,
    HadhfAndKhaban,
    Khaban,
    KhabanAndQataa,
    NoZehafNorEllah,
    Qabadh,
    Qataa,
    Qataf,
    Tatheel,
)


class BaseBahr:
    tafeelat = tuple()
    ella_dharbs_map = dict()
    sub_bahrs = tuple()
    only_one_shatr = False

    @property
    def all_shatr_combinations(self):
        tafeelas_forms = list()
        for tafeela_class in self.tafeelat[:-1]:
            tafeela = tafeela_class()
            tafeelas_forms.append(tafeela.all_zehaf_tafeela_forms())
        return tafeelas_forms

    @property
    def sub_bahrs_combinations(self):
        combinations = list()
        if self.sub_bahrs:
            for sub_bahr_class in self.sub_bahrs:
                sub_bahr = sub_bahr_class()
                combinations.extend(sub_bahr.all_combinations)
        return combinations

    @property
    def last_tafeela(self):
        last_tafeela_class = self.tafeelat[-1]
        last_tafeela = last_tafeela_class()
        return last_tafeela

    @property
    def _one_shatr_combinations(self):
        assert isinstance(
            self.arod_dharbs_map, set
        ), "if only_one_shatr is true, arood_dharbs_map should be a set"
        return list(
            itertools.product(
                *self.all_shatr_combinations,
                [
                    arood_class(self.last_tafeela).modified_tafeela
                    for arood_class in self.arod_dharbs_map
                ]
            )
        )

    @property
    def all_combinations(self):
        combinations = list()
        if self.only_one_shatr:
            return self._one_shatr_combinations
        for ella_class, dharb_classes in self.arod_dharbs_map.items():
            ella = ella_class(self.last_tafeela)
            first_shatr_combinations = list(
                itertools.product(*self.all_shatr_combinations, [ella.modified_tafeela])
            )
            second_shatr_combinations = list(
                itertools.product(
                    *self.all_shatr_combinations,
                    [
                        dharb_class(self.last_tafeela).modified_tafeela
                        for dharb_class in dharb_classes
                    ]
                )
            )
            combinations.extend(
                list(
                    itertools.product(
                        first_shatr_combinations,
                        second_shatr_combinations,
                    )
                )
            )
        # add combinations for sub bahrs
        combinations.extend(self.sub_bahrs_combinations)
        return combinations

    @property
    def all_combinations_patterns(self):
        patterns = list()
        for combination in self.all_combinations:
            pattern = ""
            first_shatr, second_shatr = combination
            pattern += "".join(
                "".join(map(str, tafeela.pattern)) for tafeela in first_shatr
            )
            pattern += "".join(
                "".join(map(str, tafeela.pattern)) for tafeela in second_shatr
            )
            patterns.append(pattern)
        return patterns


class Taweel(BaseBahr):
    tafeelat = (Fawlon, Mafaeelon, Fawlon, Mafaeelon)
    arod_dharbs_map = {
        Qabadh: (
            Qabadh,
            Hadhf,
            NoZehafNorEllah,
        )
    }


class Madeed(BaseBahr):
    tafeelat = (Faelaton, Faelon, Faelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah,),
        Hadhf: (Qataa,),
        HadhfAndKhaban: (HadhfAndKhaban,),
    }


class BaseetMajzoo(BaseBahr):
    tafeelat = (Mustafelon, Faelon, Mustafelon)
    arod_dharbs_map = {
        Qataa: (NoZehafNorEllah,),
        NoZehafNorEllah: (NoZehafNorEllah, Tatheel, Qataa),
    }


class BaseetMukhalla(BaseetMajzoo):
    arod_dharbs_map = {KhabanAndQataa: (KhabanAndQataa,)}


class Baseet(BaseBahr):
    tafeelat = (Mustafelon, Faelon, Mustafelon, Faelon)
    arod_dharbs_map = {Khaban: (Khaban, Qataa)}
    sub_bahrs = (BaseetMajzoo, BaseetMukhalla)


class WaferMajzoo(BaseBahr):
    tafeelat = (Mafaelaton, Mafaelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Asab),
        Asab: (NoZehafNorEllah, Asab),
    }


class Wafer(BaseBahr):
    tafeelat = (Mafaelaton, Mafaelaton, Mafaelaton)
    arod_dharbs_map = {Qataf: (Qataf,)}
    sub_bahrs = (WaferMajzoo,)


class KamelMajzoo(BaseBahr):
    tafeelat = (Mutafaelon, Mutafaelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (
            NoZehafNorEllah,
            Edmaar,
            Qataa,
            QataaAndEdmaar,
            Tatheel,
            TatheelAndEdmaar,
            Tarfeel,
            TarfeelAndEdmaar,
        ),
        Edmaar: (
            NoZehafNorEllah,
            Edmaar,
            Qataa,
            QataaAndEdmaar,
            Tatheel,
            TatheelAndEdmaar,
            Tarfeel,
            TarfeelAndEdmaar,
        ),
    }


class Kamel(BaseBahr):
    tafeelat = (Mutafaelon, Mutafaelon, Mutafaelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (
            NoZehafNorEllah,
            Edmaar,
            Qataa,
            QataaAndEdmaar,
            HathathAndEdmaar,
        ),
        Edmaar: (
            NoZehafNorEllah,
            Edmaar,
            Qataa,
            QataaAndEdmaar,
            HathathAndEdmaar,
        ),
        Hathath: (Hathath, HathathAndEdmaar),
    }
    sub_bahrs = (KamelMajzoo,)


class Hazaj(BaseBahr):
    tafeelat = (Mafaeelon, Mafaeelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Hadhf),
        Kaff: (
            NoZehafNorEllah,
            Hadhf,
        ),
    }


class RajazManhook(BaseBahr):
    tafeelat = (Mustafelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah,
        Khaban,
        Tay,
        Khabal,
        Qataa,
        KhabanAndQataa,
    }
    only_one_shatr = True


class RajazMashtoor(BaseBahr):
    tafeelat = (Mustafelon, Mustafelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah,
        Khaban,
        Tay,
        Khabal,
        Qataa,
        KhabanAndQataa,
    }
    only_one_shatr = True


class RajazMajzoo(BaseBahr):
    tafeelat = (Mustafelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
        ),
        Khaban: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
        ),
        Tay: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
        ),
        Khabal: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
        ),
    }


class Rajaz(BaseBahr):
    tafeelat = (Mustafelon, Mustafelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
            Qataa,
            KhabanAndQataa,
        ),
        Khaban: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
            Qataa,
            KhabanAndQataa,
        ),
        Tay: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
            Qataa,
            KhabanAndQataa,
        ),
        Khabal: (
            NoZehafNorEllah,
            Khaban,
            Tay,
            Khabal,
            Qataa,
            KhabanAndQataa,
        ),
    }
    sub_bahrs = (RajazMajzoo, RajazMashtoor, RajazManhook)


class Ramal:
    tafeelat = (Faelaton, Faelaton, Faelaton)


class Saree:
    tafeelat = (Mustafelon, Mustafelon, Mafoolato)


class Munsareh:
    tafeelat = (Mustafelon, Mafoolato, Mustafelon)


class Khafeef:
    tafeelat = (Faelaton, Mustafe_lon, Faelaton)


class Mudhare:
    tafeelat = (Mafaeelon, Fae_laton)


class Muqtadheb:
    tafeelat = (Mafoolato, Mustafelon)


class Mujtath:
    tafeelat = (Mustafe_lon, Faelaton)


class Mutaqareb:
    tafeelat = (Fawlon, Fawlon, Fawlon, Fawlon)


class Mutadarak:
    tafeelat = (Faelon, Faelon, Faelon, Faelon)

