from functools import cached_property
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
from bohour.zehaf import Hadhf, NoZehafNorEllah, Qabadh


class BaseBahr:
    tafeelat = tuple()
    ella_dharbs_map = dict()
    sub_bahrs = tuple()

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
    def all_combinations(self):
        combinations = list()
        for ella_class, dharb_classes in self.ella_dharbs_map.items():
            last_tafeela_class = self.tafeelat[-1]
            last_tafeela = last_tafeela_class()
            ella = ella_class(last_tafeela)
            first_shatr_combinations = list(
                itertools.product(*self.all_shatr_combinations, [ella.modified_tafeela])
            )
            second_shatr_combinations = list(
                itertools.product(
                    *self.all_shatr_combinations,
                    [
                        dharb_class(last_tafeela).modified_tafeela
                        for dharb_class in dharb_classes
                    ]
                )
            )
            combinations.extend(
                list(
                    itertools.product(
                        first_shatr_combinations, second_shatr_combinations,
                    )
                )
            )
        # add combinations for sub bahrs
        combinations.extend(self.sub_bahrs_combinations)
        return combinations


class Taweel(BaseBahr):
    tafeelat = (Fawlon, Mafaeelon, Fawlon, Mafaeelon)
    ella_dharbs_map = {Qabadh: (Qabadh, Hadhf, NoZehafNorEllah,)}


class Madeed:
    tafeelat = (Faelaton, Faelon, Faelaton)


class Baseet:
    tafeelat = (Mustafelon, Faelon, Mustafelon, Faelon)


class Wafer:
    tafeelat = (Mafaelaton, Mafaelaton, Mafaelaton)


class Kamel:
    tafeelat = (Mutafaelon, Mutafaelon, Mutafaelon)


class Hazag:
    tafeelat = (Mafaeelon, Mafaeelon)


class Rajaz:
    tafeelat = (Mustafelon, Mustafelon, Mustafelon)


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

