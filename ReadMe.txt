This simulation was written for an accademic project. It simulates single parity, 2D parity, checksum, and CRC error detection techniques in experimentally accurate BER conditions. 

In order to run this simulation, simply run Python3 Simulation.py on a linux terminal. For editing,  you can change the error rates which are iterated through in the error_rates array near the top of the file.
The number of bits to be transmitted can be changed in the generate_file(100000000) line below the function declarations. It is currently set to 100 million, which can be quite slow. Make any other edits at your own risk, 
this code was designed for simulation in a very specific way, and may break otherwise. 
