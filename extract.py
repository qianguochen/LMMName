
import configparser
import os
from argparse import ArgumentParser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    ulr = config.get('GPT', 'url')
    file = config.get('GPT', 'DATA_SAVE_DIR')
    dir = config.get('GPT', 'PROJECT_DIR')
    parser = ArgumentParser()
    parser.add_argument("--num_threads", dest="num_threads", required=True, default=8)
    parser.add_argument("--contain_content", dest="contain_content", action='store_true')
    parser.add_argument("--jar", dest="jar", required=True)
    args = parser.parse_args()
    project_name = dir.strip('/').split('/')[-1]
    if args.contain_content:
        command = 'java -jar ' + args.jar + ' --num_threads ' + \
                  args.num_threads + ' --contain_content ' + ' --file ' + file + project_name + '_content' + ' --dir ' + dir
        print(command)
    else:
        command = 'java -jar ' + args.jar + ' --num_threads ' + \
                  args.num_threads + ' --file ' + file + project_name + ' --dir ' + dir
        print(command)
    os.system(command)
