#!/usr/bin/env python
import shutil
import subprocess
import pathlib

def create_archive(location_to_make:str = None, input_dir:str = None)->str:
    if not (location_to_make or input_dir):
        raise Exception("Need location to output and an input directory!")
        return None
    output = pathlib.Path(location_to_make)
    input_dir = pathlib.Path(input_dir)
    file_name = shutil.make_archive(output, 'zip', input_dir)
    return file_name

if __name__ == '__main__':
    zipfile_upload = create_archive('function', 'lambda')
    fp = "fileb://{}".format(zipfile_upload)
    subproces_commands = ['aws', 'lambda', 'update-function-code', '--function-name', 'medassistantfunc', '--zip-file', fp]
    subprocess.run(args = subproces_commands, shell=True)