import argparse
import subprocess
import os
from pathlib import Path
import logging


def read_template(filename):
    """
    Read the contents of a template file.

    Args:
        filename (str): Path to the template file.

    Returns:
        str: Contents of the template file.
    """
    with open(filename) as file:
        lines = file.read()
    return lines

def guess_user():
    """
    Guess the current user.

    Returns:
        str: 'vuillaume' if the username matches specific patterns, None otherwise.
    """
    import getpass
    username = getpass.getuser()
    if username in ['tvuil', 'thomas.vuillaume', 'vuillaume']:
        return 'vuillaume'

def guess_cluster():
    """
    Guess the current cluster based on the hostname.

    Returns:
        str: 'must' if the hostname contains 'lappusmb' or 'lappui',
             'lapalma' if the hostname contains 'cp',
             None otherwise.
    """
    import socket
    hostname = socket.gethostname()
    if 'lappusmb' in hostname or 'lappui' in hostname:
        return 'must'
    if 'cp' in hostname:
        return 'lapalma'

def guess_exp_directory(cluster_name):
    """
    Determine the experiment directory based on the cluster name.

    Args:
        cluster_name (str): Name of the cluster.

    Returns:
        str: Path to the experiment directory.

    Raises:
        ValueError: If the cluster name is unknown.
    """
    if cluster_name == 'must':
        return '/uds_data/glearn/Data/experiments/'
    elif cluster_name == 'lapalma':
        return '/fefs/aswg/workspace/gammalearn/Data/experiments/'
    else:
        raise ValueError("Unknown cluster")


if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    parser = argparse.ArgumentParser(description='generate the template to start an experiment with a given name')
    parser.add_argument('exp_name', type=str, help='experiment name')
    parser.add_argument('--cluster', type=str, help='cluster where the exp is running: lapalma, must. If not provided, will try to guess from hostname.')
    parser.add_argument('--user', type=str, help="username. If not provided, will try to guess from whoami")
    parser.add_argument('--outdir', type=str, help='output directory.  default="."', default=os.path.realpath('.'), required=False)
    parser.add_argument('--email', type=str, required=False, default=None)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.info(f"Generating experiment {args.exp_name}")

    if args.cluster:
        cluster_name = args.cluster
    elif guess_cluster():
        cluster_name = guess_cluster()
    else:
        raise ValueError("Unkown cluster")
    logging.info(f'configured for cluster {cluster_name}')

    if args.user:
        username = args.user
    elif guess_user():
        username = guess_user()
    else:
        raise ValueError("Unkown user")
    logging.info(f'configured for user {username}')

    templates_dict = {
        'condor': os.path.join(dir_path, 'condor_template.submit'),
        'settings': os.path.join(dir_path, 'experiments_settings_template.py'),
        'executable': os.path.join(dir_path, 'executable_template.sh'),
        'slurm': os.path.join(dir_path, 'slurm_template.slurm'),
    }

    if cluster_name == 'lapalma':
        templates_dict.pop('condor')  # lapalma uses slurm
    if cluster_name == 'must':
        templates_dict.pop('slurm')  # must uses HHTCondor


    if args.email is None:
        try:
            git_email = subprocess.run(['git', 'config', 'user.email'], capture_output=True, check=True)
            email = git_email.stdout.decode().replace('\n', '')
        except subprocess.CalledProcessError:
            pass
    else:
        email = args.email

    nets_file = Path(__file__).absolute().parents[2].joinpath('nets.py').resolve().as_posix()

    for template_name, template_file in templates_dict.items():
        template = read_template(template_file)
        template = template.replace('{exp_name}', args.exp_name)
        template = template.replace('{email}', email)
        template = template.replace('{nets_file}', nets_file)
        template = template.replace('{main_directory}', guess_exp_directory(cluster_name))

        os.makedirs(args.outdir, exist_ok=True)
        output_file = os.path.join(args.outdir, os.path.basename(template_file).replace('template', args.exp_name))

        with open(output_file, 'w') as file:
            file.write(template)
        templates_dict[template_name] = output_file

    os.chmod(templates_dict['executable'], 0o744)

    logging.info(f"Files generated for the exp: "
                 f"{[template_file for template_name, template_file in templates_dict.items()]}")
