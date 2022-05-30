import os
import sys

# get the path of this file
this_file_path = os.path.dirname(os.path.realpath(__file__))
# append parent and current directories to path
sys.path.append(f"{this_file_path}/..")
sys.path.append(".")

from bohour import bohours_list

output_path = this_file_path + "/../bohour_patterns"

for bahr_class in bohours_list:
    bahr = bahr_class()
    combinations = bahr.all_combinations
    with open(f"{output_path}/strs/{bahr_class.__name__.lower()}.txt", "w") as file:
        combinations_str = ""
        for combination in combinations:
            if isinstance(
                combination[0],
                tuple,
            ):  # the combination has more than one shatr
                first_shatr, second_shatr = combination
                combinations_str += (
                    " ".join(str(tafeela) for tafeela in first_shatr)
                    + " # "
                    + " ".join(str(tafeela) for tafeela in second_shatr)
                    + "\n"
                )
            else:
                combinations_str += " ".join(str(tafeelah) for tafeelah in combination)
                combinations_str += "\n"
        combinations_str.strip()
        file.write(combinations_str)

    combinations_patterns = bahr_class().all_combinations_patterns
    with open(f"{output_path}/ints/{bahr_class.__name__.lower()}.txt", "w") as file:
        file.write("\n".join(str(pattern) for pattern in combinations_patterns))
