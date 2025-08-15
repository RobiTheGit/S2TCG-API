#!/usr/bin/python3

# Sonic 2 Title Card Mappings Code Generator API
# This is not intended to be a standalone program, but the base code for generating the mappings
# May be compatible for website usage


import re

DisasmLabel = 0 # Determine if we want to use generic TC_XXZ names or the disasm labels
global XPOS, INDEX, _2PINDEX
XPOS = 0
INDEX = 0
_2PINDEX = 0

def Generate(TextToGenerate, Zone, Label_Type):
    REGEX_STEP = re.sub(r"[^a-zA-Z ]", "", TextToGenerate)     # remove unmapped characters
    LENGTH_STEP = REGEX_STEP.replace(" ", "")
    L_STEP_HEX = hex(len(LENGTH_STEP)).upper()
    POS_AFTER_0 = False    
    if len(REGEX_STEP) <= 8:
        POS_AFTER_0 = True
    StartLoc = [0x70,0x60,0x50,0x40,0x30,0x20, 0x10, 0x00, 0xFFF0, 0xFFE0, 0xFFD0, 0xFFC0, 0xFFB0, 0xFFA0, 0xFF90]
    ZONE_LIST = ["EHZ","CPZ","ARZ","CNZ","HTZ","MCZ","OOZ","MTZ","SCZ","WFZ","DEZ","HPZ"]
    DISASM_LABELS = ['word_147E8', 'word_14A1E', 'word_14A88', 'word_149C4', 'word_14894', 'word_14972', 'word_14930', 'word_14842', 'word_14AE2', 'word_14B24', 'word_14B86', 'word_148CE']
    
    XPOS = StartLoc[len(REGEX_STEP)]
    INDEX = 0x5DE #S2 maxes out at 5FA in the stock title cards
    WIDTH = 0x5
    _2PINDEX = 0x2ED
    INDECIES = []
    _2PINDECIES = []
    CURR_CHAR = ''
    ALL_CHAR = []
    USED_CHARS = []
    OUTPUT = []
    if Label_Type == "OLD":
        _tempindex = ZONE_LIST.index(Zone)
        OUTPUT.append(f"{DISASM_LABELS[_tempindex]}: dc.w {L_STEP_HEX.replace('0X', '$')}")
    else:
        OUTPUT.append(f"TC_{ZONE_LIST[ZONE_LIST.index(Zone)]}: dc.w {L_STEP_HEX.replace('0X', '$')}")
    for CURR_CHAR in REGEX_STEP:
        ALL_CHAR.append(CURR_CHAR.upper())
#=================================================================
#  End of variable setup
#=================================================================
    for CURR_CHAR in ALL_CHAR:
# Set up some letter variables
        if XPOS > 0xFFFF:
            XPOS -= 0x10000
        if CURR_CHAR in USED_CHARS and CURR_CHAR != "Z"  and CURR_CHAR != "O"  and CURR_CHAR != "N"  and CURR_CHAR != "E" :
         
            REUSED_CHAR = USED_CHARS.index(CURR_CHAR)
            REUSED_INDEX = INDECIES[REUSED_CHAR]
            OUTPUT.append(f"\t" + REUSED_INDEX + f" {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            if CURR_CHAR == "I":
                XPOS += 0x8
            elif CURR_CHAR == "M" or CURR_CHAR == "W":
                XPOS += 0x18
            else:
                XPOS += 0x10
        elif CURR_CHAR == "I":
            WIDTH = 0x1
            OUTPUT.append(f"\tdc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(_2PINDEX+0x8000).replace('0x', '$').upper()}, {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            USED_CHARS.append(CURR_CHAR)
            INDECIES.append(f"dc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(_2PINDEX+0x8000).replace('0x', '$').upper()},")

            XPOS += 0x8
            INDEX += 0x2
            _2PINDEX += 0x1
        elif CURR_CHAR == "M" or CURR_CHAR == "W":
            WIDTH = 0x9
            INDECIES.append(f"dc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(_2PINDEX+0x8000).replace('0x', '$').upper()},")
            USED_CHARS.append(CURR_CHAR)
            OUTPUT.append(f"\tdc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(_2PINDEX+0x8000).replace('0x', '$').upper()}, {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            XPOS += 0x18
            INDEX += 0x6
            _2PINDEX += 0x4
        elif CURR_CHAR == "Z":

            OUTPUT.append(f"\tdc.w $5, $858C, $82C6, {hex(XPOS).replace('0x', '$').upper()} ;Z")
            XPOS += 0x10
        elif CURR_CHAR == "O":

            OUTPUT.append(f"\tdc.w $5, $8588, $82C4, {hex(XPOS).replace('0x', '$').upper()} ;O")
            XPOS += 0x10
        elif CURR_CHAR == "N":

            OUTPUT.append(f"\tdc.w $5, $8584, $82C2, {hex(XPOS).replace('0x', '$').upper()} ;N")
            XPOS += 0x10
        elif CURR_CHAR == "E":

            OUTPUT.append(f"\tdc.w $5, $8580, $82C0, {hex(XPOS).replace('0x', '$').upper()} ;E")
            XPOS += 0x10
        elif CURR_CHAR == " " or CURR_CHAR == "":        
            OUTPUT.append("")
            XPOS += 0x10
        
        else:
            WIDTH = 0x5
            USED_CHARS.append(CURR_CHAR)
            INDECIES.append(f"dc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(_2PINDEX+0x8000).replace('0x', '$').upper()},")

            OUTPUT.append(f"\tdc.w {hex(WIDTH).replace('0x', '$').upper()}, {hex(INDEX+0x8000).replace('0x', '$').upper()}, {hex(_2PINDEX+0x8000).replace('0x', '$').upper()}, {hex(XPOS).replace('0x', '$').upper()} ;{CURR_CHAR}")
            XPOS += 0x10
            INDEX += 0x4
            _2PINDEX += 0x2
    for x in OUTPUT:
        print(x)
    return OUTPUT
    
if __name__ == "__main__":
    Generate("EMERALD HILL", "EHZ", "")

