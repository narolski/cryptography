# Oracle mode demo
python3 zad1.py --opmode oracle --aes-mode CBC --input_files fiflak.jpeg fiflak_wide.jpeg --keystore_path aes-keystore.jck --keystore_pass mystorepass --key_id jceksaes --key_pass mykeypass --iv 4179834583632307

# Challenge mode demo
python3 zad1.py --opmode challenge --aes-mode CBC --input_files fiflak.jpeg fiflak_wide.jpeg --keystore_path aes-keystore.jck --keystore_pass mystorepass --key_id jceksaes --key_pass mykeypass --iv 4179834583632307

# Decryption mode demo
python3 zad1.py --opmode decrypt --aes-mode CBC --input_files fiflak.jpeg.enc fiflak_wide.jpeg.enc --keystore_path aes-keystore.jck --keystore_pass mystorepass --key_id jceksaes --key_pass mykeypass --iv 4179834583632307