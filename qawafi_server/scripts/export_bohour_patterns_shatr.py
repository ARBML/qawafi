import os
import sys


# get the path of this file
this_file_path = os.path.dirname(os.path.realpath(__file__))
# append parent and current directories to path
sys.path.append(f"{this_file_path}/..")
sys.path.append(".")
from bohour.tafeela import Tafeela

from bohour import bohours_list

output_path = this_file_path + "/../bohour_patterns_shatr"

for bahr_class in bohours_list:
    bahr = bahr_class()
    combinations = bahr.all_combinations
    with open(f"{output_path}/{bahr_class.__name__.lower()}.txt", "w") as file:
        patterns = list()
        for combination in bahr.all_combinations:
            if isinstance(combination[0], Tafeela):
                shatr = combination
                patterns.append(
                    (
                        "".join(
                            "".join(map(str, tafeela.pattern)) for tafeela in shatr
                        ),
                        " ".join(map(str, combination)),
                    )
                )

            else:
                first_shatr, second_shatr = combination
                patterns.append(
                    (
                        "".join(
                            "".join(map(str, tafeela.pattern))
                            for tafeela in first_shatr
                        ),
                        " ".join(map(str, first_shatr)),
                    )
                )

                patterns.append(
                    (
                        "".join(
                            "".join(map(str, tafeela.pattern))
                            for tafeela in second_shatr
                        ),
                        " ".join(map(str, second_shatr)),
                    )
                )
        patterns = list(dict.fromkeys(patterns))
        patterns = "\n".join(",".join(pattern) for pattern in patterns)
        file.write(patterns)
