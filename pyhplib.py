import math
import sys
# // DECLARE CONSTANTS

BISCUIT_P_NLANES        = 1
BISCUIT_P_NBITS         = 16                                 #// Bit width of datapath
BISCUIT_C_LOG_NBITS     = int( math.log(BISCUIT_P_NBITS,2) ) #// # of bits needed to index into subword
BISCUIT_C_LOG_NBITS_STR = str(BISCUIT_C_LOG_NBITS)
BISCUIT_C_N_OFF         = 32/BISCUIT_P_NBITS                 #// Number of total n-bit chunks per word. 
BISCUIT_C_OFFBITS       = int( math.log(BISCUIT_C_N_OFF,2) ) #// # of bits needed to index the n-bit chunks.
BISCUIT_C_OFFBITS_STR   = str(BISCUIT_C_OFFBITS)
BISCUIT_N_CTRL_SIGNALS  = 74 #//74 for multiplier 58 for baseline
import BISCUIT_microcode as mc
