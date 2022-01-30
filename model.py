import os
import time

!pip install qiskit

from qiskit import BasicAer, execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

# from quantuminspire.credentials import get_authentication
# from quantuminspire.qiskit import QI

# QI_URL = os.getenv('42ca57206e553107fd2180b65ab21c3764c70e5a', 'https://api.quantum-inspire.com/')


# authentication = get_authentication()
# QI.set_authentication(authentication, QI_URL)
# qi_backend = QI.get_backend('Spin-2')

!pip install quantuminspire
from quantuminspire.credentials import get_authentication
from quantuminspire.qiskit import QI
QI_URL = os.getenv('42ca57206e553107fd2180b65ab21c3764c70e5a', 'https://api.quantum-inspire.com/')


authentication = get_authentication()
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('Spin-2')


# Creating Alice's Bits and Bases
global qkd
def alice(length):
    alice_bits = []
    alice_bases = []
    global Length
    Length = length
    
    #BIT GENERATION
    for i in range(length):
        alice_bits.append(getrandbits(1))
        
        # 0 means encode in the Z basis and 1 means encode in the X,Y basis
        alice_bases.append(getrandbits(1))
    print(len(alice_bases))
        

    encoded_qubits = [] #an array of qc circuits with 1 qubit each
    for i in range(length):
        # create a brand new quantum circuit called qc
        qc = QuantumCircuit(1,1)

        if alice_bases[i] == 0:
            # 0 Means we are encoding in the z basis
            if alice_bits[i] == 0:
                # We want to encode a |0> state, as states are intialized
                # in |0> by default we don't need to add anything here
                pass
            
            elif alice_bits[i] == 1:
                # We want to encode a |1> state
                # We apply an X gate to generate |1>
                qc.x(0)
                
        elif alice_bases[i] == 1:
            # 1 Means we are encoding in the x basis
            if alice_bits[i] == 0:
                # We apply an H gate to generate |+>
                qc.h(0)
            elif alice_bits[i] == 1:
                # We apply an X and an H gate to generate |->
                qc.x(0)
                qc.h(0)
            
        # add this quantum circuit to the list of encoded_qubits
        encoded_qubits.append(qc)
        
        global alice_bases_xz
        alice_bases_xz = []
        for i in range(length):
            if(alice_bases[i] == 0):
                alice_bases_xz.append("Z")
            else:
                alice_bases_xz.append("X")
    return encoded_qubits

def key(length, bob_bitstring, measure_bases):
    #Converting Alice Bases from 0,1 to X, Z 
    c_KEY = []
    for x in range(length):
        if (alice_bases_xz[x] == measure_bases[x]):
            c_KEY.append(bob_bitstring[x])
            
    return c_KEY

def bowser_key(c_KEY): 
    x = []
    if len(c_KEY) >=3:
        #Replace 1 of Key values
        for i in range(len(c_KEY)):
            x.append(i)
        y = random.randint(0,len(c_KEY)-1)
        corrupted_key = c_KEY
        if c_KEY[y] == '0':
            corrupted_key[y] = '1'
        else:
            corrupted_key[y] = '0'
        x.pop(y)
        
        #Replace second key value
        y = random.randint(0,len(c_KEY)-1)
        corrupted_key = c_KEY
        if c_KEY[y] == '0':
            corrupted_key[y] = '1'
        else:
            corrupted_key[y] = '0'
        x.pop(y)
        
        return corrupted_key
    
    elif len(c_KEY)>1:
        y = getrandbits(1)
        corrupted_key = c_KEY
        if c_KEY[y] == '0':
            corrupted_key[y] = '1'
        else:
            corrupted_key[y] = '0'
        
        return corrupted_key
    
    elif len(c_KEY)==1:
        if c_KEY[0] == '0':
            corrupted_key[0] = '1'
        else:
            corrupted_key[0] = '0'
        
        return corrupted_key
        
    
    else:
        while len(c_KEY) == 0:
            print("Not working")
            #QKD(5)
        