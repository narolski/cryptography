import os
import pytest
import filecmp, jks

from Crypto.Cipher import AES
from zad1 import AES_MODES


TEST_KEYSTORE_PATH = 'aes-keystore.jck'
TEST_KEYSTORE_PASS = 'mystorepass'
TEST_KEY_ID = 'jceksaes'
TEST_KEY_PASS = 'mykeypass'

TEST_IN_FILE = 'fiflak.jpeg'
TEST_ENC_FILE = 'fiflak.jpeg.enc'
TEST_OUT_FILE = 'decrypted_fiflak.jpeg'

TEST_IV = '4179834583632307'
TEST_OPMODE_ORACLE = 'oracle'
TEST_OPMODE_DECRYPT = 'decrypt'


@pytest.mark.parametrize("mode", AES_MODES.keys())
def test_encryption_valid(mode):
    """
    Tests that the usage of the implemented
    encrypting/decrypting service results
    in an appropriate encryption and decryption
    of an input file, being given valid input parameters
    and valid input.
    """
    os.system("python3 zad1.py --opmode {} --aes-mode {} --input_files {} --keystore_path {} --keystore_pass {} --key_id {} --key_pass {} --iv {}".format(TEST_OPMODE_ORACLE, AES_MODES[mode], TEST_IN_FILE, TEST_KEYSTORE_PATH, TEST_KEYSTORE_PASS, TEST_KEY_ID, TEST_KEY_PASS, TEST_IV))

    os.system("python3 zad1.py --opmode {} --aes-mode {} --input_files {} --keystore_path {} --keystore_pass {} --key_id {} --key_pass {} --iv {}".format(TEST_OPMODE_DECRYPT, AES_MODES[mode], TEST_ENC_FILE, TEST_KEYSTORE_PATH, TEST_KEYSTORE_PASS, TEST_KEY_ID, TEST_KEY_PASS, TEST_IV))

    assert filecmp.cmp(TEST_IN_FILE, TEST_OUT_FILE)
