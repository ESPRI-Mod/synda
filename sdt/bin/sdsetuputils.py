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

        # TODO needs to fill the proper keyfile locations just in case. mainly sdt.db
        cfg = SafeConfigParser()
        cfg.read(os.path.join(self.synda_home, 'conf/sdt.conf'))
        # cfg.set('core', 'db_path', str(os.path.join(self.target_root, 'sdt.db')))
        cfg.set('core', 'db_path', str(os.path.join(self.synda_home, 'db')))
        cfg.set('core', 'selection_path', str(os.path.join(self.synda_home, 'selection')))
        cfg.set('core', 'sandbox_path', str(os.path.join(self.synda_home, 'sandbox')))
        cfg.set('core', 'default_path', str(os.path.join(self.synda_home, '')))
        with open(os.path.join(self.synda_home, 'conf/sdt.conf'), "w+") as configfile:
            cfg.write(configfile)
        # sdlog.debug('SDTSETUP-001','Successfully set the default paths in config file to {}'.format(cfg.get('core', 'default_path')))

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
        """
        for key_file in key_file_list:
            if not os.path.isfile(os.path.join(self.synda_home, key_file)) :
                # in this case sys admin did not copy an old file into root dir.
                print('Key file missing: {}'.format(key_file))
                copy_file(os.path.join(sys.exec_prefix, key_file), os.path.join(self.synda_home, key_file))

        # key directory stubs to be copied.
        try:
            shutil.copytree(os.path.join(sys.exec_prefix, 'tmp'), os.path.join(self.synda_home, 'tmp'))
            shutil.copytree(os.path.join(sys.exec_prefix, 'log'), os.path.join(self.synda_home, 'log'))
            shutil.copytree(os.path.join(sys.exec_prefix, 'selection/sample'),
                            os.path.join(self.synda_home, 'selection/sample'))
        except OSError, e:
            if e.errno != os.errno.EEXIST:
                print('File exists, please verify your synda home directory.')
                sys.exit(1)
            pass

        # key directory stubs to be created.
        for key_dir in key_dir_to_create:
            if not os.path.isdir(os.path.join(self.synda_home, key_dir)):
                os.mkdir(os.path.join(self.synda_home, key_dir))
        """
        # Configuration files were all found, filling up sdt.conf with proper files.
        self.configuration_setup()
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
        print('Init new synda environment (db and configuration).')
        print('If you think this is a mistake, copy your old data files to {}'.format(os.getenv('ST_HOME')))


    #     opener, mode = tarfile.open, 'r:gz'
    #     file = opener(self.data_tar, mode)
    #     try: file.extractall()
    #     finally: file.close()


    # # cfg_dir = appdirs.user_config_dir('synda')
    # shutil.copytree(cfg_dir, os.getenv('ST_HOME'))
    # def create_conf_files(self):
    #     pass
    # def create_db_file(self):
    #     pass
    # def create_key_dirs(self):
    #     pass
    # def create_log_files(self):
    #     pass
    # def create_bin_files(self):
    #     pass
