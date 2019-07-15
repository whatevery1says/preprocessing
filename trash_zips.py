import os
from libs.zipeditor.zipeditor import zip_scanner_excludedirs

def trash_zips_from_file(del_file, source_path, trash_path='trash', inspect=True):
    """loop over a text file of filepaths
       and walk a root directory for zips.
       any zip whose name perfectly matches a name in the file:
          move it to the trash directory.
    """

    os.makedirs(trash_path, exist_ok=True)
    zip_files = zip_scanner_excludedirs(source_path=source_path,
                                        exclude_list=[], join=False)

    print('\nzip_files:')
    for zip_file in zip_files:
        print('  ', zip_file)

    trash_list = []
    with open(del_file, 'r') as trash_lines:
        for trash_line in trash_lines:
            trash_list.append(trash_line.strip())

    print('\ntrash_list:')
    for trash_file in trash_list:
        print('  ', trash_file)
    print('')

    for trashname in trash_list:
        # print('trashname:', trashname)
        for zip_file in zip_files:
            # print('zip_file:', zip_file, zip_file[1])
            if zip_file[1].strip()==trashname.strip():
                if inspect:
                    print('inspect rename:', os.path.join(zip_file[0], zip_file[1]), ':', os.path.join(trash_path, zip_file[1]))
                else:
                    print('rename:', os.path.join(zip_file[0], zip_file[1]), ':', os.path.join(trash_path, zip_file[1]))
                    os.rename(os.path.join(zip_file[0], zip_file[1]), os.path.join(trash_path, zip_file[1]))

def main():

    # del_file = 'data_zip/_trash_fpath_list.txt'
    # source_path = 'data_zip'
    # trash_path = '_trash'

    del_file = '/home/we1s-data/data/_trash_fpath_list.txt'
    source_path = '/home/we1s-data/data/collect'
    trash_path = '/home/we1s-data/data/trash'

    trash_zips_from_file(del_file=del_file, source_path=source_path, trash_path=trash_path, inspect=True)

if __name__ == '__main__':
    main()
