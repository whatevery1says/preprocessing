#!/usr/bin/env python3
import os
from shutil import copyfile
from zip_preprocess import zip_batch_process

def test():
    """Test the script.
    
    The base test data is kept in a non-zip extension to 
    avoid accidentally altering its contents. On the test run,
    test the data.
    
    """

    
    zip_dir_root = os.path.join(os.getcwd(), 'data_zip')
    source_field = 'content'
    preprocessing_log = '_preprocessing_log.csv'
    wikifier_output_dir = 'wikifier'
    skip_rerun = True

    # 
    test_zips = ['test.zip.BAK']
    for filename in test_zips:
        try:
            source = os.path.join(zip_dir_root, filename)
            dest = os.path.join(zip_dir_root, filename + '.zip')
            copyfile(source, dest)
        except FileNotFoundError:
            print("No such file:", source)
            pass
            
    zip_batch_process(zip_dir_root=zip_dir_root,
                      source_field=source_field,
                      preprocessing_log=preprocessing_log,
                      wikifier_output_dir=wikifier_output_dir,
                      skip_rerun=skip_rerun
                      )

test()