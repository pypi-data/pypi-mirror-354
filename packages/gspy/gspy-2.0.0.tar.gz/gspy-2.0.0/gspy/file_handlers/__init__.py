from os.path import isfile, splitext
from .aseg_gdf_handler import aseg_gdf2_handler
from .csv_handler import csv_handler
from .loupe_handler import loupe_handler

def file_handler(filename):

    file_name, file_extension = splitext(filename)
    file_extension = file_extension.lower()

    # Detect data type using file extensions.
    # Aseg .dat comes with a .dfn file
    # Loupe .dat comes with a .desc file
    # XYZ might be Workbench

    workbench_handler = None
    if file_extension == '.xyz':
        if isfile(file_name[:-3]+"dat.xyz") and isfile(file_name[:-3]+"inv.xyz") and isfile(file_name[:-3]+"syn.xyz"):
            return workbench_handler
    elif file_extension == '.dat':
        if isfile(file_name+'.dfn'):
            return aseg_gdf2_handler
        elif isfile(file_name+file_extension+'.desc'):
            return loupe_handler

    # Catch all others as a csv i.e. .xyz, .csv
    return csv_handler