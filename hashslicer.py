#!/bin/python3
import itertools
import argparse
import subprocess
import os
import sys
import multiprocessing

def generate_password_combinations(known_part, length_of_unknown_part, output_file, start_idx, end_idx, queue):
    possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*-_."
    combinations = itertools.product(possible_chars, repeat=length_of_unknown_part)
    with open(output_file, 'w') as file:
        for idx, combination in enumerate(combinations):
            if idx < start_idx:
                continue
            if idx >= end_idx:
                break
            password = known_part + ''.join(combination)
            file.write(password + '\n')
    queue.put(output_file)

def run_hashcat(hash_file, wordlist_file, output_file):
    try:
        cmd = [
            'hashcat', 
            '-m', '100',  # SHA-1 hash mode
            '-a', '0',    # Straight attack mode
            hash_file,    # File with hash
            wordlist_file,  # File with password list
            '--outfile', output_file  # Output file for cracked passwords
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("Hashcat stdout:")
        print(result.stdout)
        print("Hashcat stderr:")
        print(result.stderr)
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            with open(output_file, 'r') as file:
                lines = file.readlines()
                if lines:
                    for line in lines:
                        # Format: hash:password
                        print(line.strip())
                    return True
        else:
            print("Hash not found or output file is empty.")
            return False
    except FileNotFoundError:
        print("Hashcat not found. Please install Hashcat.")
        sys.exit(1)
def calculate_chunk_space(num_combinations, password_length):
    # Assume each line in the file is a password followed by a newline character.
    # Average password length + newline character
    line_length = password_length + 1  # +1 for the newline character
    # Size estimation: num_combinations * line_length * size_of_each_character
    # For simplicity, assume each character takes 1 byte.
    size_in_bytes = num_combinations * line_length
    size_in_gigabytes = size_in_bytes / (1024 ** 3)  # Convert bytes to GB
    return size_in_gigabytes



def main():
    parser = argparse.ArgumentParser(description='Generate and crack password combinations.')
    parser.add_argument('-p', '--part', type=str, required=True, help='The known part of the password')
    parser.add_argument('-u', '--unknown', type=int, required=True, help='The number of unknown characters')
    parser.add_argument('-o', '--output', type=str, default='password_combinations.txt', help='Output file for the password combinations')
    parser.add_argument('-s', '--segment', type=int, help='Generate only a specific segment of the combinations')
    parser.add_argument('-t', '--total_segments', type=int, help='Total number of segments to divide the combinations into')
    parser.add_argument('--hash', type=str, required=True, help='SHA-1 hash to crack')
    parser.add_argument('--hash_file', type=str, default='hash.txt', help='File to store SHA-1 hash')
    args = parser.parse_args()
  
    if not args.part or args.unknown is None or (args.segment is not None and args.total_segments is None) or (args.segment is None and args.total_segments is not None):
        parser.print_help()
        sys.exit(1)
    
    with open(args.hash_file, 'w') as f:
        f.write(args.hash + '\n')
    possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*-_."
    total_combinations = len(possible_chars) ** args.unknown
    segment_size = total_combinations // args.total_segments
    previous_segment_file = None


    for segment in range(1, args.total_segments + 1):
        start_idx = (segment - 1) * segment_size
        end_idx = total_combinations if segment == args.total_segments else segment * segment_size
        segment_output_file = f"{args.output}_segment_{segment}.txt"
        cracked_output_file = f"cracked_password_{segment}.txt"

        # Print number of possibilities being used and estimated space needed
        num_possibilities = end_idx - start_idx
        avg_password_length = len(args.part) + args.unknown
        estimated_space_gb = calculate_chunk_space(num_possibilities, avg_password_length)
        safe_space_gb = estimated_space_gb * 2  # Safe margin: twice the estimated space
        print(f"Segment {segment}: Generating {num_possibilities} possibilities (from index {start_idx} to {end_idx})")
        print(f"Estimated space needed for this segment: {estimated_space_gb:.2f} GB")
        print(f"Safe margin space for this segment: {safe_space_gb:.2f} GB")

        # Create a queue for inter-process communication
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=generate_password_combinations, args=(args.part, args.unknown, segment_output_file, start_idx, end_idx, queue))
        p.start()
        p.join()

        segment_output_file = queue.get()
        if run_hashcat(args.hash_file, segment_output_file, cracked_output_file):
            print(f"Password found in segment {segment}.")

            # Remove all wordlist files
            for i in range(1, segment + 1):
                wordlist_file = f"{args.output}_segment_{i}.txt"
                if os.path.exists(wordlist_file):
                    os.remove(wordlist_file)
            break
        else:
            print(f"Segment {segment} completed. Moving to next segment.")
        

        # Delete the previous segment file
        if previous_segment_file and os.path.exists(previous_segment_file):
            os.remove(previous_segment_file)

        # Update the previous segment file reference
        previous_segment_file = segment_output_file

        # Optionally remove the cracked output file if you don't need it
        if os.path.exists(cracked_output_file):
            os.remove(cracked_output_file)
    os.remove(args.hash_file)

if __name__ == '__main__':
    main()
