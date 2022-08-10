import sys, os, shutil

from tkinter import filedialog
from tkinter import *


# helper function
def rename_and_move_subtitles_in_subs_folder(subtitles_folder, movie_file_name, movie_folder_path):
    for subtitle_file in os.listdir(subtitles_folder):
        if(subtitle_file.endswith('.srt')):
            subs_file = subtitle_file
            print('\t\tFound Subtitle File '+ subs_file)
            
            # rename subs file
            new_sub_name = movie_file_name[:-4] + '.' + subs_file
            print('\t\tRenamed to Subtitle File '+new_sub_name)
            # Rename Subs Files
            old_subs_path = os.path.join(subtitles_folder, subs_file)
            new_subs_path = os.path.join(subtitles_folder, new_sub_name)
            os.rename(old_subs_path,new_subs_path)

            # move to movie_folder_path
            new_sub_location = os.path.join(movie_folder_path, new_sub_name)
            shutil.move(new_subs_path, new_sub_location)
            
            print('Renamed & Moved: '+ new_sub_location)
            
            # check if subtitles folder is empty
            if(len(os.listdir(subtitles_folder)) == 0):
                # Delete subtitles folder
                print('\t\tDeleting Subs Folder')
                os.rmdir(subtitles_folder)
            else:
                print('Additional Files in Subs Folder')
                


root = Tk()
root.withdraw()
# directory with all movie folders
d = filedialog.askdirectory()
if d == '' or d is None:
    sys.exit(0)

# get all subfolders i.e. every movie folder of root
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
#print(subdirs)

# loop through them and check if there is a subs folder
for movie_folder_path in subdirs:
    sub_dir_files = os.listdir(movie_folder_path)
    movie_folder_name = os.path.basename(movie_folder_path) 
    subtitles_folder = ''
    movie_file_location = ''
    movie_file_name=''
    found_subs_folder = False
    srt_files_in_folder = []
    amt_srt_files_in_folder = 0
    amt_srt_files_in_folder_renamed = 0
    print(movie_folder_name)
    for sb in sub_dir_files:
        if('subs' in sb.lower() and os.path.isdir(os.path.join(movie_folder_path, sb))):
            # found the subs folder
            subtitles_folder = os.path.join(movie_folder_path, sb)
            found_subs_folder = True
            print('\tFound Subs Folder '+sb)
        elif(sb.endswith('.mp4') or sb.endswith('.mkv') or sb.endswith('.avi')):
            # found the movie file
            movie_file_location = os.path.join(movie_folder_path, sb)
            movie_file_name = sb
            print('\tFound Movie File '+ sb)
        elif(sb.endswith('.srt')):
            print('\tFound Sub File '+ sb)
            amt_srt_files_in_folder += 1
            srt_files_in_folder.append(sb)
        elif(sb.lower() == "rarbg.txt" or sb.lower() == 'rarbg_do_not_mirror.exe'):
              # remove these files
            print('\tRemoving '+sb)
            os.remove(os.path.join(movie_folder_path, sb))

    if(movie_file_name != '' and movie_file_location != '' and len(srt_files_in_folder) > 0):
        movie_file_name_without_extension = movie_file_name[:-4]
        
        for srt in srt_files_in_folder:
            # check if srt file starts with movie_file_name_without_extension
            if(srt.startswith(movie_file_name_without_extension)):
                print('\t\tFound Subtitle File with Movie Name Already Appended '+srt)
            else:
                # rename the srt file
                print('\t\tRenaming Subtitle File '+srt)
                new_name = movie_file_name_without_extension + '.' + srt
                os.rename(os.path.join(movie_folder_path, srt), os.path.join(movie_folder_path, new_name))
                amt_srt_files_in_folder_renamed += 1
        
        print('\t\tAmount of SRT Files in Main Movie Folder: '+str(amt_srt_files_in_folder))
        print('\t\tAmount of SRT Files in Main Movie Folder Renamed: '+str(amt_srt_files_in_folder_renamed))
        
    elif(found_subs_folder):
        # check if filepath subtitles_folder exists
        if(os.path.exists(subtitles_folder)):
            rename_and_move_subtitles_in_subs_folder(subtitles_folder, movie_file_name, movie_folder_path)

        
    else:
        print('No Subs Folder found')

        
  
    
    
