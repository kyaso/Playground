# Thanks ChatGPT :)
# Prompt used:
#
# I need a python script for the following algorithm:
#
# Read a binary file into a byte array
# For each byte in the array:
#  - Convert the byte into a bit string of length 8 (fill up leading 0s)
#  - Prepend the bit string to a list
#
# join the list to a single string
#
# The output should be string of 1s and 0s where the MSB of the binary file is at index 0 of the string
def binary_file_to_bit_string(file_path):
    try:
        with open(file_path, "rb") as file:
            content = file.read()
            bit_string_list = []
            for byte in content:
                # Convert byte to bit string and fill up leading zeros
                bit_string = format(byte, '08b')
                bit_string_list.insert(0, bit_string)  # Prepend the bit string to the list

            # Join the list of bit strings into a single string
            full_bit_string = ''.join(bit_string_list)
            return full_bit_string
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# No AI involved here ;)
def search_bit_string(source: str, pattern: str):
    print(f"Searching for pattern {pattern}...")
    pattern_len = len(pattern)
    source_len = len(source)
    idx = 0
    while idx <= (source_len - pattern_len):
        found_idx = source.find(pattern, idx)
        if found_idx == -1:
            break
        print_le_start_index(source_len, found_idx, pattern_len)
        idx = found_idx + pattern_len

    if idx == 0:
        print(f"Pattern {pattern} not found!")


def print_le_start_index(source_len, found_idx, pattern_len):
    found_end_idx = found_idx + pattern_len - 1
    reverse_start_idx = source_len - found_end_idx - 1
    # Use this IF in case you only want byte-aligned matches
    if reverse_start_idx % 8 == 0:
        print(f"Found occurrence at {found_idx}")
        reverse_start_idx_bytes = int(reverse_start_idx / 8)
        print(f"Entry start: 0x{reverse_start_idx_bytes:08x}")


# Example usage:
file_path = "file.bin"  # Path to your binary file
pattern = "100011
bit_string = binary_file_to_bit_string(file_path)
if bit_string:
    print(bit_string)
    print(f"Length of source string: {len(bit_string)}")
    search_bit_string(bit_string, pattern)
