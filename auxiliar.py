import os
import json
from variables import CONFIG_FILE_PATH

def limpiar_consola():
  """  
  limpia la consola
  """
  if os.name in ["ce", "nt", "dos"]: # windows
    os.system("cls")
  else: # linux o mac
    os.system("clear")

def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)