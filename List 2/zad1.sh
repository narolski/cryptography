# Oracle mode demo
python3 zad1.py --opmode oracle --aes-mode OFB --input_files fiflak.jpeg fiflak_wide.jpeg test.txt --keystore_path aes-keystore.jck --keystore_pass mystorepass --key_id jceksaes --key_pass mykeypass --iv 4179834583632307

# Challenge mode demo
python3 zad1.py --opmode challenge --aes-mode OFB --input_files fiflak.jpeg fiflak_wide.jpeg --keystore_path aes-keystore.jck --keystore_pass mystorepass --key_id jceksaes --key_pass mykeypass --iv 4179834583632307

# Decryption mode demo
python3 zad1.py --opmode decrypt --aes-mode OFB --input_files fiflak.jpeg.enc fiflak_wide.jpeg.enc test.txt.enc --keystore_path aes-keystore.jck --keystore_pass mystorepass --key_id jceksaes --key_pass mykeypass --iv 4179834583632307