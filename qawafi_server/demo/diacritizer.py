import tnkeeh as tn 
import os
with open("baits_input.txt", "w") as baits_file:
  baits = ['يا واحد مات أتى تأريخنا # للعلم بعدك وحشة يايونس']
  baits_file.write("\n".join(baits))
  tn.clean_data(
      file_path="baits_input.txt",
      save_path="baits_input.txt",
      remove_diacritics=True,
      # remove_special_chars=True,
      remove_tatweel=True,
  )
  # diacritize
  os.system("bash diacritization_command.bash")
  diacritized_baits = open("baits_output.txt").read().splitlines()