import argparse





def main(args):

    pass


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()


    parser.add_argument('scan_files_path',type=str)
    parser.add_argument('ROI_file',type=str)
    parser.add_argument("output_path",type=str)
    parser.add_argument('suffix',type=str)
    parser.add_argument('logPath',type=str)


    args = parser.parse_args()


    main(args)