import site
import os, sys, shutil, errno
from ConfigParser import SafeConfigParser
from six.moves import input
import tarfile
import os.path
import pkg_resources
from sdexception import EnvironmentNotSet
# import sdlog


class PostInstallCommand():
    """
    Post installation for installation mode
    """

    def update_conf_file(self, root_folder):
        """
        Updates the sdt.conf file with the new key files locations.
        :param root_folder:
        :return:
        """
        with open(os.path.join(root_folder, 'sdt.conf')) as conf_file:
            pass

    def run_db_scripts(self):
        """
        Creates db structure
        """
        import bin.sddb

    def configuration_setup(self):
        """
        Using sdt.conf template, config file is filled with proper paths to key data_package files.
        """
        cfg = SafeConfigParser()
        cfg.read(os.path.join(self.synda_home, 'conf/sdt.conf'))
        cfg.set('core', 'db_path', str(os.path.join(self.synda_home, 'db')))
        cfg.set('core', 'selection_path', str(os.path.join(self.synda_home, 'selection')))
        cfg.set('core', 'sandbox_path', str(os.path.join(self.synda_home, 'sandbox')))
        cfg.set('core', 'default_path', str(os.path.join(self.synda_home, '')))
        with open(os.path.join(self.synda_home, 'conf/sdt.conf'), "w+") as configfile:
            cfg.write(configfile)

        # To ease up credentials setting.
        answer = ''
        while answer not in ['y', 'n']:
            answer = raw_input('Would you like to set your openID credentials? y/n: ').lower()
            if answer == 'y':
                openID = raw_input('openID url: ').lower()
                password = raw_input('password: ')
                cred = SafeConfigParser()
                cred.read(os.path.join(self.synda_home, 'conf/credentials.conf'))
                cred.set('esgf_credential', 'openid', openID)
                cred.set('esgf_credential', 'password', password)
                with open(os.path.join(self.synda_home, 'conf/credentials.conf'), 'w+') as credfile:
                    cred.write(credfile)
            else:
                pass



    def run(self):
        # Checking the install environment
        if check_environment():
            self.synda_home = os.getenv('ST_HOME')
        else:
            print("Please set the environment variable ST_HOME")
            sys.exit(1)
        # sdlog.debug("SDTSETUP-001", "ST_HOME is detected in environment. Using {}".format(self.synda_home))
        # Checking key files
        key_file_list = [
            'bin/sdcleanup_tree.sh',
            'bin/sdconvert.sh',
            'bin/sdgetg.sh',
            'bin/sdget.sh',
            'bin/sdparsewgetoutput.sh',
            'conf/sdt.conf',
            'conf/credentials.conf',
            'db/sdt.db'
        ]

        key_dir_list = [
            'tmp',
            'log',
            'selection'
        ]

        key_dir_to_create = [
            'data_package',
            'sandbox'
        ]
        #  File check loop
        for key_file in key_file_list:
            if not os.path.isfile(os.path.join(self.synda_home, key_file)):
                print('Key file missing: {}'.format(key_file))
                print('You can either copy previously used file into your ST_HOME ({}) or use synda init-env command to '
                      'initialize a new synda home file system with stubs to fill properly.'.format(self.synda_home))
                return False
                # raise EnvironmentNotSet('SDTSETUP-001', 'Environment not initialized.')
        for key_dir in key_dir_list:
            if not os.path.isdir(os.path.join(self.synda_home, key_dir)):
                print('Key directory missing: {}'.format(key_dir))
                print(
                    'You can either copy previously used file into your ST_HOME ({}) or use synda init-env command to '
                    'initialize a new synda home file system with stubs to fill properly.'.format(self.synda_home))
                return False
                # raise EnvironmentNotSet('SDTSETUP-001', 'Environment not initialized.')
        # Configuration files were all found, filling up sdt.conf with proper files.
        self.configuration_setup()
        print('Check complete.')
        return True

def check_environment():
    """
    used to make sure ST_HOME is set
    :return:
    """
    if os.getenv('ST_HOME') is None:
        return False
    else:
        return True


def touch(file_path):
    """
    Creates empty file
    :param file_path: path to file to create
    """
    open(file_path, 'a').close()


def copy_file(src, dst):
    """
    layer over shutil copyfile creates dir if not existent
    :param src:
    :param dst:
    :return:
    """
    try:
        shutil.copy(src, dst)
    except IOError as e:
        if e.errno != errno.ENOENT and e.errno != errno.EEXIST:
            raise
        elif e.errno == errno.EEXIST:
            os.mkdir(os.path.join(dst, os.path.basename(src)))

        os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)


def copy_tree(src_root, dst_root):
    for item in os.listdir(src_root):
        if os.path.isfile(os.path.join(src_root, item)):
            copy_file(os.path.join(src_root, item), dst_root)
            print('copying {} -> {}'.format(os.path.join(src_root, item), dst_root))
            print('copied')
        elif os.path.isdir(os.path.join(src_root, item)):
            copy_tree(os.path.join(src_root, item), os.path.join(dst_root, item))



class EnvInit():
    def __init__(self):
        self.st_home = os.getenv('ST_HOME')
        self.data_tar = str(pkg_resources.resource_filename(__name__, "data.tar.gz"))

    def untar_data_package(self):
        opener, mode = tarfile.open, 'r:gz'
        data_tar = opener(self.data_tar, mode)
        try:
            data_tar.extractall(self.st_home)
        finally:
            data_tar.close()

    def run(self):
        self.untar_data_package()
        print('(RE)initialized a new synda environment (db and conf files).')
        print('If you think this is a mistake, copy your old data files to {}'.format(os.getenv('ST_HOME')))
