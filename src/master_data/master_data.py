SETTING_DIR = "master_data/settings/"

l_type_list = []
with open(SETTING_DIR + "column4.txt") as f:
  l_type_list = f.readlines()

s_type_list = []
with open(SETTING_DIR + "column5.txt") as f:
  s_type_list = f.readlines()

free_format_list = []
with open(SETTING_DIR + "column6.txt") as f:
  free_format_list = f.readlines()

length_list = list(range(3,16))

diameter_list = []
with open(SETTING_DIR + "column8.txt") as f:
  diameter_list = f.readlines()


fittings_types_list = []
with open(SETTING_DIR + "column9_10.txt") as f:
  fittings_types_list = f.readlines()

delimiter_list = ["|"]
with open(SETTING_DIR + "delimiter.txt") as f:
  delimiter_list = f.readlines()
