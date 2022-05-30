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
    Tafeela,
)
from bohour.zehaf import (
    Asab,
    Batr,
    Edmaar,
    Hadhf,
    HadhfAndKhaban,
    Hathath,
    HathathAndEdmaar,
    Kaff,
    Kasf,
    Khabal,
    Khaban,
    KhabanAndQataa,
    NoZehafNorEllah,
    Qabadh,
    Qataa,
    QataaAndEdmaar,
    Qataf,
    Salam,
    Shakal,
    Tarfeel,
    TarfeelAndEdmaar,
    TarfeelAndKhaban,
    Tasbeegh,
    Tasheeth,
    Tatheel,
    TatheelAndEdmaar,
    Tay,
    TayAndKasf,
    Thalm,
    Tharm,
    Waqf,
    WaqfAndTay,
    KhabalAndKasf,
)


class Bahr:
    tafeelat = tuple()
    arod_dharbs_map = dict()
    sub_bahrs = tuple()
    only_one_shatr = False

    @property
    def disallowed_zehafs_for_hashw(self):
        """
        This will be replaced by a class attr in subclasses
        It was done this way here just to infere the size of tafeelat
        """
        return {
            0: tuple([] for _ in range(len(self.tafeelat[:-1]))),
            1: tuple([] for _ in range(len(self.tafeelat[:-1]))),
        }

    def remove_disallowed_tafeelas_in_hashw(
        self,
        tafeela_forms,
        tafeela_hashw_index,
        shatr_index,
    ):
        assert (
            len(self.disallowed_zehafs_for_hashw[shatr_index]) == len(self.tafeelat) - 1
        ), "hashw tafeelat and `disallowed_zehafs_for_hashw` list should match in size"
        filtered_forms = list()
        for tafeela in tafeela_forms:
            assert (
                tafeela.applied_ella_zehaf_class is None
                or tafeela.applied_ella_zehaf_class in tafeela.allowed_zehafs
            ), f"zehaf {tafeela.applied_ella_zehaf_class} is not allowed for {tafeela}"
            if (
                tafeela.applied_ella_zehaf_class
                not in self.disallowed_zehafs_for_hashw[shatr_index][
                    tafeela_hashw_index
                ]
            ):
                filtered_forms.append(tafeela)
        return filtered_forms

    def get_shatr_hashw_combinations(self, shatr_index=0):
        combinations = list()
        for tafeela_index, tafeela_class in enumerate(self.tafeelat[:-1]):
            tafeela = tafeela_class()
            all_tafeela_forms = tafeela.all_zehaf_tafeela_forms()
            filtered_tafeela_forms = self.remove_disallowed_tafeelas_in_hashw(
                tafeela_forms=all_tafeela_forms,
                tafeela_hashw_index=tafeela_index,
                shatr_index=shatr_index,
            )
            combinations.append(filtered_tafeela_forms)
        return combinations

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
                *self.get_shatr_hashw_combinations(),
                [
                    arood_class(self.last_tafeela).modified_tafeela
                    for arood_class in self.arod_dharbs_map
                ],
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
                itertools.product(
                    *self.get_shatr_hashw_combinations(shatr_index=0),
                    [ella.modified_tafeela]
                    + [  # for tasree patterns
                        dharb_class(self.last_tafeela).modified_tafeela
                        for dharb_class in dharb_classes
                    ],
                )
            )
            second_shatr_combinations = list(
                itertools.product(
                    *self.get_shatr_hashw_combinations(shatr_index=1),
                    [
                        dharb_class(self.last_tafeela).modified_tafeela
                        for dharb_class in dharb_classes
                    ],
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
        # remove duplicates, if any
        # combinations = list(set(combinations))
        combinations = list(dict.fromkeys(combinations)) # remove and maintain the order
        return combinations

    @property
    def all_combinations_patterns(self):
        patterns = list()
        for combination in self.all_combinations:
            pattern = ""
            if isinstance(combination[0], Tafeela):
                shatr = combination
                pattern += "".join(
                    "".join(map(str, tafeela.pattern)) for tafeela in shatr
                )
            else:
                first_shatr, second_shatr = combination
                pattern += "".join(
                    "".join(map(str, tafeela.pattern)) for tafeela in first_shatr
                )
                pattern += "".join(
                    "".join(map(str, tafeela.pattern)) for tafeela in second_shatr
                )
            patterns.append(pattern)
        return patterns

    @property
    def max_pattern_length(self):
        return len(max(self.all_combinations_patterns, key=len))

    @property
    def min_pattern_length(self):
        return len(min(self.all_combinations_patterns, key=len))


class Taweel(Bahr):
    tafeelat = (Fawlon, Mafaeelon, Fawlon, Mafaeelon)
    arod_dharbs_map = {Qabadh: (Qabadh, Hadhf, NoZehafNorEllah)}
    disallowed_zehafs_for_hashw = {
        0: ([], [], [Thalm, Tharm]),
        1: ([Thalm, Tharm], [], [Thalm, Tharm]),
    }


class Madeed(Bahr):
    tafeelat = (Faelaton, Faelon, Faelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah,),
        Hadhf: (Qataa,),
        HadhfAndKhaban: (HadhfAndKhaban,),
    }
    disallowed_zehafs_for_hashw = {
        0: ([Shakal, Tasheeth], [Tasheeth]),
        1: ([Shakal, Tasheeth], [Tasheeth]),
    }

    @property
    def all_combinations(self):
        """
        تطبيق المعاقبة: وذلك أنه لا يجوز اجتماع خبن فاعلن وكف فاعلاتن،
        """
        combinations = super().all_combinations
        filtered_combinations = list()
        for combination in combinations:
            first_shatr, second_shatr = combination
            if first_shatr[0].applied_ella_zehaf_class == Kaff:
                if first_shatr[1].applied_ella_zehaf_class == Khaban:
                    continue
            if second_shatr[0].applied_ella_zehaf_class == Kaff:
                if second_shatr[1].applied_ella_zehaf_class == Khaban:
                    continue
            filtered_combinations.append(combination)
        return filtered_combinations


class BaseetMajzoo(Bahr):
    tafeelat = (Mustafelon, Faelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Tatheel, Qataa),
        Qataa: (NoZehafNorEllah,),
    }
    disallowed_zehafs_for_hashw = {
        0: ([], [Tasheeth]),
        1: ([], [Tasheeth]),
    }


class BaseetMukhalla(BaseetMajzoo):
    arod_dharbs_map = {KhabanAndQataa: (KhabanAndQataa,)}
    disallowed_zehafs_for_hashw = {
        0: ([], [Tasheeth]),
        1: ([], [Tasheeth]),
    }


class Baseet(Bahr):
    tafeelat = (Mustafelon, Faelon, Mustafelon, Faelon)
    arod_dharbs_map = {Khaban: (Khaban, Qataa)}
    disallowed_zehafs_for_hashw = {
        0: ([], [Tasheeth], []),
        1: ([], [Tasheeth], []),
    }
    sub_bahrs = (BaseetMajzoo, BaseetMukhalla)


class WaferMajzoo(Bahr):
    tafeelat = (Mafaelaton, Mafaelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Asab),
        Asab: (NoZehafNorEllah, Asab),
    }


class Wafer(Bahr):
    tafeelat = (Mafaelaton, Mafaelaton, Mafaelaton)
    arod_dharbs_map = {Qataf: (Qataf,)}
    sub_bahrs = (WaferMajzoo,)


class KamelMajzoo(Bahr):
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


class Kamel(Bahr):
    tafeelat = (Mutafaelon, Mutafaelon, Mutafaelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (
            NoZehafNorEllah,
            Edmaar,
            Qataa,
            QataaAndEdmaar,
            HathathAndEdmaar,
        ),
        Edmaar: (NoZehafNorEllah, Edmaar, Qataa, QataaAndEdmaar, HathathAndEdmaar),
        Hathath: (Hathath, HathathAndEdmaar),
    }
    sub_bahrs = (KamelMajzoo,)


class Hazaj(Bahr):
    tafeelat = (Mafaeelon, Mafaeelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Hadhf),
        Kaff: (NoZehafNorEllah, Hadhf),
    }
    disallowed_zehafs_for_hashw = {
        0: ([Qabadh],),
        1: ([Qabadh],),
    }


class RajazManhook(Bahr):
    tafeelat = (Mustafelon, Mustafelon)
    arod_dharbs_map = {NoZehafNorEllah, Khaban, Tay, Khabal, Qataa, KhabanAndQataa}
    only_one_shatr = True


class RajazMashtoor(Bahr):
    tafeelat = (Mustafelon, Mustafelon, Mustafelon)
    arod_dharbs_map = {NoZehafNorEllah, Khaban, Tay, Khabal, Qataa, KhabanAndQataa}
    only_one_shatr = True


class RajazMajzoo(Bahr):
    tafeelat = (Mustafelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Khaban, Tay, Khabal),
        Khaban: (NoZehafNorEllah, Khaban, Tay, Khabal),
        Tay: (NoZehafNorEllah, Khaban, Tay, Khabal),
        Khabal: (NoZehafNorEllah, Khaban, Tay, Khabal),
    }


class Rajaz(Bahr):
    tafeelat = (Mustafelon, Mustafelon, Mustafelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Khaban, Tay, Khabal, Qataa, KhabanAndQataa),
        Khaban: (NoZehafNorEllah, Khaban, Tay, Khabal, Qataa, KhabanAndQataa),
        Tay: (NoZehafNorEllah, Khaban, Tay, Khabal, Qataa, KhabanAndQataa),
        Khabal: (NoZehafNorEllah, Khaban, Tay, Khabal, Qataa, KhabanAndQataa),
    }
    sub_bahrs = (RajazMajzoo, RajazMashtoor, RajazManhook)


class RamalMajzoo(Bahr):
    tafeelat = (Faelaton, Faelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Khaban, Tasbeegh, Hadhf, HadhfAndKhaban),
        Khaban: {NoZehafNorEllah, Khaban, Tasbeegh, Hadhf, HadhfAndKhaban},
    }
    disallowed_zehafs_for_hashw = {
        0: ([Tasheeth],),
        1: ([Tasheeth],),
    }


class Ramal(Bahr):
    tafeelat = (Faelaton, Faelaton, Faelaton)
    arod_dharbs_map = {
        Hadhf: (
            NoZehafNorEllah,
            Khaban,
            Hadhf,
            HadhfAndKhaban,
            Qataa,  # originally Qasar, bu they are technically the same
            KhabanAndQataa,
        ),
        HadhfAndKhaban: {
            NoZehafNorEllah,
            Khaban,
            Hadhf,
            HadhfAndKhaban,
            Qataa,
            KhabanAndQataa,
        },
    }
    sub_bahrs = (RamalMajzoo,)
    disallowed_zehafs_for_hashw = {
        0: ([Tasheeth], [Tasheeth]),
        1: ([Tasheeth], [Tasheeth]),
    }


class SareeMashtoor(Bahr):
    tafeelat = (Mustafelon, Mustafelon, Mafoolato)
    arod_dharbs_map = {Waqf, Kasf}
    only_one_shatr = True


class Saree(Bahr):
    tafeelat = (Mustafelon, Mustafelon, Mafoolato)
    arod_dharbs_map = {
        TayAndKasf: (TayAndKasf, Salam, WaqfAndTay),
        KhabalAndKasf: {KhabalAndKasf, Salam},
    }
    sub_bahrs = (SareeMashtoor,)


class MunsarehManhook(Bahr):
    tafeelat = (Mustafelon, Mafoolato)
    arod_dharbs_map = {Waqf, Kasf}
    only_one_shatr = True


class Munsareh(Bahr):
    tafeelat = (Mustafelon, Mafoolato, Mustafelon)
    arod_dharbs_map = {Tay: (Tay, Qataa)}
    sub_bahrs = (MunsarehManhook,)


class KhafeefMajzoo(Bahr):
    tafeelat = (Faelaton, Mustafe_lon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, KhabanAndQataa),
        Khaban: (Khaban,),
    }
    disallowed_zehafs_for_hashw = {
        0: ([Kaff, Shakal, Tasheeth],),
        1: ([Kaff, Shakal, Tasheeth],),
    }


class Khafeef(Bahr):
    tafeelat = (Faelaton, Mustafe_lon, Faelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Tasheeth, Hadhf, HadhfAndKhaban),
        Khaban: (NoZehafNorEllah, Tasheeth, Hadhf, HadhfAndKhaban),
    }
    sub_bahrs = (KhafeefMajzoo,)
    disallowed_zehafs_for_hashw = {
        0: ([Kaff, Shakal], []),
        1: ([Kaff, Shakal], []),
    }


class Mudhare(Bahr):
    tafeelat = (Mafaeelon, Fae_laton)
    arod_dharbs_map = {NoZehafNorEllah: (NoZehafNorEllah,)}

    @property
    def all_combinations(self):
        """
        this bahr, unlike other bahrs, its hashaw should
        have zehaf!
        """
        combinations = super().all_combinations
        zehafed_combinations = list(
            filter(
                lambda combination: combination[0][0].applied_ella_zehaf_class
                is not None
                and combination[1][0].applied_ella_zehaf_class is not None,
                combinations,
            )
        )
        return zehafed_combinations


class Muqtadheb(Bahr):
    tafeelat = (Mafoolato, Mustafelon)
    arod_dharbs_map = {Tay: (Tay,)}
    disallowed_zehafs_for_hashw = {
        0: ([Khabal],),
        1: ([Khabal],),
    }


class Mujtath(Bahr):
    tafeelat = (Mustafe_lon, Faelaton)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Khaban, Tasheeth),
        Khaban: (NoZehafNorEllah, Khaban, Tasheeth),
    }
    disallowed_zehafs_for_hashw = {
        0: ([Kaff],),
        1: ([Kaff],),
    }


class MutaqarebMajzoo(Bahr):
    tafeelat = (Fawlon, Fawlon, Fawlon)
    arod_dharbs_map = {Hadhf: (Hadhf, Batr)}
    disallowed_zehafs_for_hashw = {
        0: ([], [Thalm, Tharm]),
        1: ([Thalm, Tharm], [Thalm, Tharm]),
    }


class Mutaqareb(Bahr):
    tafeelat = (Fawlon, Fawlon, Fawlon, Fawlon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Hadhf, Qataa, Batr),
        Qabadh: (NoZehafNorEllah, Hadhf, Qataa, Batr),
        Hadhf: (NoZehafNorEllah, Hadhf, Qataa, Batr),
    }
    disallowed_zehafs_for_hashw = {
        0: ([], [Thalm, Tharm], [Thalm, Tharm]),
        1: ([Thalm, Tharm], [Thalm, Tharm], [Thalm, Tharm]),
    }
    sub_bahrs = (MutaqarebMajzoo,)


class MutadarakMashtoor(Bahr):
    tafeelat = (Faelon, Faelon, Faelon)
    arod_dharbs_map = {NoZehafNorEllah, Khaban, Tasheeth, Tatheel, TarfeelAndKhaban}
    only_one_shatr = True


class MutadarakMajzoo(Bahr):
    tafeelat = (Faelon, Faelon, Faelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Khaban, Tasheeth, Tatheel, TarfeelAndKhaban),
        Khaban: (NoZehafNorEllah, Khaban, Tasheeth, Tatheel, TarfeelAndKhaban),
        Tasheeth: (NoZehafNorEllah, Khaban, Tasheeth, Tatheel, TarfeelAndKhaban),
    }


class Mutadarak(Bahr):
    tafeelat = (Faelon, Faelon, Faelon, Faelon)
    arod_dharbs_map = {
        NoZehafNorEllah: (NoZehafNorEllah, Khaban, Tasheeth),
        Khaban: (NoZehafNorEllah, Khaban, Tasheeth),
        Tasheeth: (NoZehafNorEllah, Khaban, Tasheeth),
    }
    sub_bahrs = (MutadarakMajzoo, MutadarakMashtoor)
