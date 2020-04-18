import random, struct, os, binascii, jks, argparse, sys
from Crypto.Cipher import AES


AES_MODES = {
    "OFB": AES.MODE_OFB,
    "CTR": AES.MODE_CTR,
    "CBC": AES.MODE_CBC,
    "CFB": AES.MODE_CFB,
    "ECB": AES.MODE_ECB,
    "OPENPGP": AES.MODE_OPENPGP,
    "PGP": AES.MODE_PGP
}
OPMODES = (
    "decrypt",
    "oracle", 
    "challenge"
)


def encrypt_file(aes, input_file, chunksize=16, output_file=None):
    """ Encrypts a file with AES using the provided mode
        and an symetrical encryption/decryption key,
        as well as initialization vector value
        stored in AES encryptor object.

        In order to encrypt the file, an initialization vector
        (IV) is used, and appropriate padding based
        on the provided chunksize is applied.

        The input_file filesize is stored
        in a generated encrypted file for the purpouse
        of allowing a proper decryption of data. This value may
        not be kept secret without compromising the security
        of the encryption scheme.

        An encrypted file is stored with an .enc extension
        appended to the input_file filename.

        aes:
            An initialized AES encryptor with provided
            decryption key, AES mode, IV.

        input_file:
            Name of the input file.

        chunksize:
            Defines the size of the chunk used when reading
            and encrypting the file with AES. The larger the
            chunk size, the faster the encryption might be.
            Note that the chunksize value must be divisible
            by 16.
    """
    if not chunksize % 16 == 0: raise Exception("Chunksize must be divisible by 16")
    if not output_file: output_file = input_file + '.enc'
    
    filesize = os.path.getsize(input_file)

    with open(input_file, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0: break
                elif len(chunk) % 16 != 0: chunk += bytes((' ' * (16 - len(chunk) % 16)), encoding='utf8') 
                # The above applies the padding

                outfile.write(aes.encrypt(chunk))


def decrypt_file(aes, input_file, chunksize=16):
    """ Decrypts a file with AES using a provided mode
        and an symmetrical encryption/decryption key.

        A decrypted file is stored without an .enc extension
        from the input_file filename, with a 'decrypted' suffix
        added.
        
        aes:
            An initialized AES decryptor with provided
            decryption key, AES mode, IV.

        input_file:
            Name of the input file.

        chunksize:
            Defines the size of the chunk used when reading
            and encrypting the file with AES. The larger the
            chunk size, the faster the encryption might be.
            Note that the chunksize value must be divisible
            by 16.
    """
    output_file = 'decrypted_' + os.path.splitext(input_file)[0]

    with open(input_file, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]

        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0: break
                
                outfile.write(aes.decrypt(chunk))

            outfile.truncate(origsize)


def get_encryption_key(key_store_path, key_store_pass, key_id):
    """
    Returns an encryption key fetched from a keystore at a given path,
    using provided details.

    key_store_path:
        Path to the keystore (relative or absolute).

    key_store_pass:
        Password used to access the keystore.

    key_id:
        Identifier under which the encryption key is stored.
    """
    key_store = jks.KeyStore.load(key_store_path, key_store_pass)
    return key_store.secret_keys[key_id]


def main(args):
    keystore_key = get_encryption_key(args.keystore_path, args.keystore_pass, args.key_id)
    keystore_key.decrypt(args.key_pass)

    aes = AES.new(keystore_key._key, AES_MODES[args.aes_mode], bytes(args.iv, encoding="utf-8"))

    if args.opmode == "oracle":
        for file in args.input_files: encrypt_file(aes, file)
    elif args.opmode == "challenge":
        file = random.choice(args.input_files[:2])
        encrypt_file(aes, file, output_file='challenge.enc')
    elif args.opmode == "decrypt":
        for file in args.input_files: decrypt_file(aes, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keystore_path", required=True, help="Path where keystore is located")
    parser.add_argument("--keystore_pass", required=True, help="Password used to access keystore at a given path")
    parser.add_argument("--key_id", required=True, help="Identifier under which an encryption key is stored")
    parser.add_argument("--key_pass", required=True, help="Password used to access the encryption key")
    parser.add_argument("--iv", required=True, help="Value of initialization vector used during encryption/decryption")

    parser.add_argument("--opmode", required=True, choices=OPMODES, help="Operation mode")
    parser.add_argument("--aes-mode",required=True, choices=AES_MODES.keys(), help="AES encryption mode")
    parser.add_argument("--input_files", required=True, help="Paths to input files", nargs="+")
    args = parser.parse_args()
    main(args)