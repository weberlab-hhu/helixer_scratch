import os
import subprocess
import json
import shutil

def main():
    experiment_json = subprocess.check_output(['nnictl', 'experiment', 'show'])
    exp_id = json.loads(experiment_json)['id']
    home = os.environ['HOME']
    start_dir = f'{home}/nni-experiments/{exp_id}/start'
    os.mkdir(start_dir)
    shutil.copy('search_space.json', start_dir)
    shutil.copy('config.yml', start_dir)
    print(f'the following files successfully copied to : {start_dir}')
    print(subprocess.check_output(['ls', start_dir]))

if __name__ == "__main__":
    main()
