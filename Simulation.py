import random

file_path = 'data.txt' #global variable for the file path of the data being sent
number_bytes_to_send = None #set as None for no limit

#error rates
wired_tcp = 1.364e-5
wired_ipv4 = 7.773e-7
wired_ipv6 = 7.28e-8
wired_avg = 4.83e-6
wireless_tcp = 8.97e-7
wireless_ipv6 = 7.61e-6
wireless_avg = 2.806e-6
one_per = 0.01
five_per = 0.05
ten_per = 0.1
error_rates = [wired_tcp, wired_ipv4, wired_ipv6, wired_avg, wireless_tcp, wireless_ipv6, wireless_avg, one_per, five_per, ten_per] #array of error rates to be tested

def generate_file(num_bits):
    if num_bits < 1:
        raise ValueError("Number of bits must be a positive integer.")

    # Generate a string of random 1s and 0s
    random_bits = "".join(random.choice("01") for _ in range(num_bits))
    
    # Write the random bits to a file named data.txt
    with open("data.txt", "w") as file:
        file.write(random_bits)

    print(f"Generated file 'data.txt' with {num_bits} random bits.")

def introduce_error(bin, BER): 
    bits_flipped = 0
    corrupted_bin = []
    for bit in bin:
        if random.random() < BER:
            bits_flipped += 1
            corrupted_bin.append('0' if bit == '1' else '1')
        else:
            corrupted_bin.append(bit)
    return "".join(corrupted_bin), bits_flipped

def single_parity(bin): #odd parity
    count = bin.count('1')
    parity_bit = '1' if count % 2 == 0 else '0'
    return bin + parity_bit

def check_2Dparity(bin): 
    for i in range(0,7):
        result = check_parity(bin[i])
        if result:
            return result
        
    count = 0
    for i in range(0,7):
        for j in range(0,7):
            if bin[j][i] == "1":
                count += 1
        if count % 2 == 0:
            return True
        
    return False


def add_checksum(bin):
    checksum = ""
    carry = 0

    for i in range(0, 7):
        if bin[i] == "0" and bin[i+8] == "0":
            if carry == 1: 
                checksum += "1"
                carry = 0
            else: 
                checksum += "0"
        elif bin[i] == "0" and bin[i+8] == "1" or bin[i] == "1" and bin[i+8] == "0":
            if carry == 1:
                checksum += "0"
                carry = 1
            else: 
                checksum += "1"
        elif bin[i] == "1" and bin[i+8] == "1":
            if carry == 1:
                checksum += "1"
                carry = 1
            else: 
                checksum += "0"

    return bin + checksum

def check_checksum(bin):
    checksum = ""
    carry = 0

    real_checksum = bin[16:23]

    for i in range(0, 7):
        if bin[i] == "0" and bin[i+8] == "0":
            if carry == 1: 
                checksum += "1"
                carry = 0
            else: 
                checksum += "0"
        elif bin[i] == "0" and bin[i+8] == "1" or bin[i] == "1" and bin[i+8] == "0":
            if carry == 1:
                checksum += "0"
                carry = 1
            else: 
                checksum += "1"
        elif bin[i] == "1" and bin[i+8] == "1":
            if carry == 1:
                checksum += "1"
                carry = 1
            else: 
                checksum += "0"

    return not (checksum == real_checksum)


def calc_CRC(data, generator):
    if len(data) != 6 or len(generator) != 4 or not set(data + generator).issubset({'0', '1'}):
        raise ValueError("Invalid input. Ensure data is 6 bits and generator is 4 bits, both binary.")

    # Convert data and generator to lists for manipulation
    data_bits = list(data + '0' * (len(generator) - 1))  # Append (generator size - 1) zeros
    generator_bits = list(generator)

    # Perform XOR division to calculate the remainder
    for i in range(len(data)):
        # Only process if the current bit is '1'
        if data_bits[i] == '1':
            for j in range(len(generator_bits)):
                # XOR operation for division
                data_bits[i + j] = '0' if data_bits[i + j] == generator_bits[j] else '1'

    # Extract the remainder (last (len(generator)-1) bits)
    remainder = ''.join(data_bits[-(len(generator) - 1):])

    # Return the original data with the remainder appended
    return data + remainder

def check_CRC(data_with_crc, generator):
    if len(generator) != 4 or not set(data_with_crc + generator).issubset({'0', '1'}):
        raise ValueError("Invalid input. Ensure generator is 4 bits, and data_with_crc is binary.")

    # Convert data_with_crc and generator to lists for manipulation
    data_bits = list(data_with_crc)
    generator_bits = list(generator)

    # Perform XOR division to calculate the remainder
    for i in range(len(data_with_crc) - len(generator) + 1):
        # Only process if the current bit is '1'
        if data_bits[i] == '1':
            for j in range(len(generator_bits)):
                # XOR operation for division
                data_bits[i + j] = '0' if data_bits[i + j] == generator_bits[j] else '1'

    # Extract the remainder (last (len(generator)-1) bits)
    remainder = ''.join(data_bits[-(len(generator) - 1):])

    # If the remainder is all zeros, no error is detected
    return remainder != '0' * (len(generator) - 1)

def check_parity(bin):
    count = bin.count('1')  # Count all 1s in the byte (including parity bit)
    result = count % 2 == 1
    return not result  # Odd parity: valid if the total count is odd

def print_error_rates(total_intro, total_detect, intro, detect):
    if total_intro != 0:
        total_rate = total_detect / total_intro
    else:
        return

    print(f"Total detection rate: {total_rate * 100:.2f}%")

    percent_array = ['', '', '', '', '', '', '', '']
    for i in range(0, 8):
        if intro[i] != 0:
            percent = detect[i] / intro[i]
            percent_str = f"{percent * 100:.2f}%"
            percent_array[i] = percent_str
        else: 
            percent_array[i] = "N/A"

    print(percent_array)

#main method
#generate_file(100000000)
generate_file(1000)

#simulation of single parity
for error in error_rates:
    total_errors_introduced = 0
    errors_introduced = [0, 0, 0, 0, 0, 0, 0, 0] #position 0 for 1 bit errors, position 1 for 2 bit errors etc

    total_errors_detected = 0
    errors_detected = [0, 0, 0, 0, 0, 0, 0, 0]

    with open(file_path, 'r') as file:
        iteration = 0
        error_rate = error

        while True:
            # Read the next 7 characters from the file
            chunk = file.read(7)
            
            # Exit the loop if the chunk is less than 7 bits (end of file)
            if len(chunk) < 7:
                break
            
            #test single parity
            byte = single_parity(chunk)
            byte, num_error = introduce_error(byte, error_rate)
            result = check_parity(byte)

            if num_error != 0:
                errors_introduced[num_error - 1] += 1
                total_errors_introduced += 1
            if result: 
                errors_detected[num_error - 1] += 1
                total_errors_detected += 1
            
            # Check the iteration limit if number_bytes_to_send is set
            if number_bytes_to_send is not None and iteration >= number_bytes_to_send:
                break

            iteration += 1

    print(f"for error rate {error_rate} and {iteration} bytes sent")
    print(f"total errors: {total_errors_introduced}")
    print(errors_introduced)
    print(f"total errors detected: {total_errors_detected}")
    print(errors_detected)
    print_error_rates(total_errors_introduced, total_errors_detected, errors_introduced, errors_detected)
    print('')



#simulation of 2D parity

print("######Simulation of 2D parity#####")

for error in error_rates: 
    total_errors_introduced = 0
    errors_introduced = [0, 0, 0, 0, 0, 0, 0, 0] #position 0 for 1 bit errors, position 1 for 2 bit errors etc. Position 7 is for 8+ bit errors

    total_errors_detected = 0
    errors_detected = [0, 0, 0, 0, 0, 0, 0, 0]

    with open(file_path, 'r') as file:
        iteration = 0
        error_rate = error

        while True:
            chunk = file.read(49)
            if len(chunk) < 49:
                break
            
            matrix = []
            for i in range(7):
                matrix.append(chunk[i*7:(i+1)*7])

            #matrix = [file.read(7), file.read(7), file.read(7), file.read(7), file.read(7), file.read(7), file.read(7)]

            for i in range(0,6):
                matrix[i] = single_parity(matrix[i])

            parity_byte = ""
            for i in range(0, 7):
                one_count = 0
                for j in range(0, 6):
                    if matrix[j][i] == "1":
                        one_count += 1
                
                if one_count % 2 == 1:
                    parity_byte += "0"
                else:
                    parity_byte += "1"

            matrix.append(parity_byte)

            num_error = 0
            bit_errors = 0
            for i in range(0, 7): #introduce error to 2D matrix
                matrix[i], bit_errors = introduce_error(matrix[i], error)
                num_error += bit_errors

            result = check_2Dparity(matrix)

            if num_error != 0 and num_error < 8:
                errors_introduced[num_error - 1] += 1
                total_errors_introduced += 1
            elif num_error > 7:
                errors_introduced[7] += 1
                total_errors_introduced +=1
            if result and num_error < 8 and num_error != 0:
                errors_detected[num_error - 1] += 1
                total_errors_detected += 1
            elif result and num_error > 7:
                errors_detected[7] += 1
                total_errors_detected += 1

            if number_bytes_to_send is not None and iteration * 7 >= number_bytes_to_send:
                break

            iteration += 1

    print(f"for error rate {error_rate} and {iteration * 7} bytes sent")
    print(f"total errors: {total_errors_introduced}")
    print(errors_introduced)
    print(f"total errors detected: {total_errors_detected}")
    print(errors_detected)
    print_error_rates(total_errors_introduced, total_errors_detected, errors_introduced, errors_detected)
    print('')
            
#Simulation of checksum
print("######Simulation of Checksum######\n")
for error in error_rates: 
    total_errors_introduced = 0
    errors_introduced = [0, 0, 0, 0, 0, 0, 0, 0] #position 0 for 1 bit errors, position 1 for 2 bit errors etc. Position 7 is for 8+ bit errors

    total_errors_detected = 0
    errors_detected = [0, 0, 0, 0, 0, 0, 0, 0]

    with open(file_path, 'r') as file:
        iteration = 0
        error_rate = error

        while True:
            chunk = file.read(16)
            if len(chunk) < 16:
                break
            
            chunk_with_checksum = add_checksum(chunk)
            chunk_with_checksum, num_error = introduce_error(chunk_with_checksum, error)
            result = check_checksum(chunk_with_checksum)

            if num_error != 0 and num_error < 8:
                errors_introduced[num_error - 1] += 1
                total_errors_introduced += 1
            elif num_error > 7:
                errors_introduced[7] += 1
                total_errors_introduced +=1
            if result and num_error < 8 and num_error != 0:
                errors_detected[num_error - 1] += 1
                total_errors_detected += 1
            elif result and num_error > 7:
                errors_detected[7] += 1
                total_errors_detected += 1

            if number_bytes_to_send is not None and iteration * 7 >= number_bytes_to_send:
                break

            iteration += 1

    print(f"for error rate {error_rate} and {iteration * 7} bytes sent")
    print(f"total errors: {total_errors_introduced}")
    print(errors_introduced)
    print(f"total errors detected: {total_errors_detected}")
    print(errors_detected)
    print_error_rates(total_errors_introduced, total_errors_detected, errors_introduced, errors_detected)
    print('')

print("#####Simulation of CRC#####")

for error in error_rates: 
    total_errors_introduced = 0
    errors_introduced = [0, 0, 0, 0, 0, 0, 0, 0] #position 0 for 1 bit errors, position 1 for 2 bit errors etc. Position 7 is for 8+ bit errors

    total_errors_detected = 0
    errors_detected = [0, 0, 0, 0, 0, 0, 0, 0]

    key = "1101"

    with open(file_path, 'r') as file:
        iteration = 0
        error_rate = error

        while True:
            chunk = file.read(6)
            if len(chunk) < 6:
                break
            
            chunk_with_crc = calc_CRC(chunk, key)
            chunk_with_crc, num_error = introduce_error(chunk_with_crc, error)
            result = check_CRC(chunk_with_crc, key)

            if num_error != 0 and num_error < 8:
                errors_introduced[num_error - 1] += 1
                total_errors_introduced += 1
            elif num_error > 7:
                errors_introduced[7] += 1
                total_errors_introduced +=1
            if result and num_error < 8 and num_error != 0:
                errors_detected[num_error - 1] += 1
                total_errors_detected += 1
            elif result and num_error > 7:
                errors_detected[7] += 1
                total_errors_detected += 1

            if number_bytes_to_send is not None and iteration * 7 >= number_bytes_to_send:
                break

            iteration += 1

    print(f"for error rate {error_rate} and {iteration * 7} bytes sent")
    print(f"total errors: {total_errors_introduced}")
    print(errors_introduced)
    print(f"total errors detected: {total_errors_detected}")
    print(errors_detected)
    print_error_rates(total_errors_introduced, total_errors_detected, errors_introduced, errors_detected)
    print('')







