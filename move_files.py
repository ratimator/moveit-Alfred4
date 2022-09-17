from subprocess import run, PIPE,check_output,Popen
import os
from pathlib import Path
import shutil

fromdir = os.getenv('source')
todir = os.getenv('destination')

# Artist and Track identifier in exiftool
artist='Artist'
track='Track'

# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(fromdir):
    files = [f for f in files if not f[0] == '.']
    for filename in files:
        # I use absolute path, case you want to move several dirs.
        old_name = os.path.join(root, filename )
        # Separate base from extension
        base, extension = os.path.splitext(filename)

        # Create new name based on criteria

        temp_exif_data=str(check_output(['exiftool', f'-{artist}', f'-{track}', old_name]).decode()).replace('\n',':').strip().split(':')
        temp_exif_data=[i.strip() for i in temp_exif_data]
        chk_list=[i for i in ['Artist','Track'] if i in temp_exif_data]
        if len(chk_list)>0:
            if 'Artist' in temp_exif_data : temp_exif_data.remove('Artist')
            if 'Track' in temp_exif_data : temp_exif_data.remove('Track')
            if '' in temp_exif_data : temp_exif_data.remove('')
            new_file_name=f"{temp_exif_data[0]} - {temp_exif_data[1]}.{extension}"

            new_name = os.path.join(todir, new_file_name)
            print(f"Transferred from :{old_name} to : {new_name}")
            os.makedirs(os.path.dirname(new_name), exist_ok=True)
            shutil.copy(old_name,new_name)
        else:
            print("Artist, track not found")