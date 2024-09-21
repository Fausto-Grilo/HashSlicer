# HashSlicer

HashSlicer is a Python-based password-cracking tool designed for penetration testers and ethical hackers to weaponize data breaches efficiently. It generates password combinations based on a known segment of the password and then uses these combinations to attempt to crack SHA-1 hashed passwords. CrackForge integrates seamlessly with Hashcat, providing a powerful means to simulate real-world attacks against compromised or leaked hashes.

## Key Features
- **Segmented Processing:** Efficiently divides password combinations into segments to handle large datasets.
- **Parallel Processing:** Utilizes multiple CPU cores to accelerate password generation and cracking.
- **Integration with Hashcat:** Works in conjunction with Hashcat for effective hash-cracking attacks.
- **Custom Wordlist Generation:** Creates password variants based on known portions, reducing the cracking time.

## Installation

### Prerequisites
- **Python 3.x**: Download from [Python's official website](https://www.python.org/downloads/).
- **Hashcat**: Download and install from [Hashcat's website](https://hashcat.net/hashcat/).

### Clone the Repository
```bash
git clone https://github.com/Fausto-Grilo/HashSlicer.git
cd HashSlicer
```

## Usage
To use HashSlicer, run the script using the following command:

```bash
python3 hashslicer.py -p <known_part> -u <unknown_length> -t <total_segments> --hash <SHA-1_hash>
```

### Command-Line Arguments
- `-p` or `--part`: **(Required)** The known part of the password.
- `-u` or `--unknown`: **(Required)** The number of unknown characters in the password.
- `-t` or `--total_segments`: **(Required)** The total number of segments to divide the combinations into.
- `--hash`: **(Required)** The SHA-1 hash to crack.
- `-o` or `--output`: **(Optional)** The base name for output files (default: `password_combinations.txt`).
- `-s` or `--segment`: **(Optional)** The specific segment of combinations to generate.

### Example Usage
If the known part of the password is "Pass123" with 3 unknown characters and we want to split the workload into 5 segments, you can run:
```bash
python3 hashslicer.py -p Pass123 -u 3 -t 5 --hash d3486ae9136e7856bc42212385ea797094475802
```

## How It Works
1. **Password Generation**: HashSlicer generates all possible combinations for the unknown part using letters, numbers, and special characters.
2. **Segmented Processing**: Password combinations are split into segments, enabling parallel processing and efficient handling of large datasets.
3. **Integration with Hashcat**: Each generated segment is processed with Hashcat to attempt to crack the hash.
4. **Stopping on Success**: When the correct password is found, all temporary files are cleaned up, and the process halts.

## Estimated Space Requirements
The tool calculates the estimated space required for storing generated password combinations based on the password length, ensuring efficient usage of disk space.

## Output
- **Wordlist Files**: Generated password combinations are stored as `password_combinations_segment_<number>.txt`.
- **Cracked Passwords**: If successful, cracked passwords are saved in `cracked_password_<segment>.txt`.

## Combining with Hashcat
You can use the generated wordlist files directly with Hashcat for password cracking:
```bash
hashcat -m 100 -a 0 hash.txt password_combinations_segment_1.txt --outfile cracked_password.txt
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
We welcome contributions! If you'd like to contribute, please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Disclaimer
HashSlicer is intended for ethical hacking and educational purposes only. Unauthorized usage against systems without permission is illegal and unethical. Always obtain explicit authorization before testing any system.

## Contact
For any questions, suggestions, or feedback, feel free to reach out:
- GitHub: [Fausto-Grilo](https://github.com/Fausto-Grilo)
