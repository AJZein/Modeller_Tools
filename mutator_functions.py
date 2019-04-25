# Python version 3.7.0
# mutator_functions version 1.1.2
def indexer(string, substring):
    """Gets the indexes of all occurences of substring in string"""
    n = True
    indexes = []
    start = 0
    while n:
        index = string.find(substring, start)
        if index != -1:
            indexes += [index]
            start = index + len(substring)
        else:
            n = False
    return indexes

def split_keep(string, substring):
    """Same as string.split(substring) except output still contains substring"""
    parts = string.split(substring)
    new_parts = []
    for i in range(len(parts)-1):
        new_parts.extend([parts[i], substring])
    new_parts.append(parts[-1])
    return new_parts


def proximity_replace(string, substring, replacer, origin, maximum=1, positions=False):
    """Replaces occureneces of 'substring' in 'string' with 'replacer' starting near
    'origin' and perfroming a maximum of 'maximum' replacements"""
    indexes = indexer(string, substring) #Get occurences of substring in string
    if len(indexes) == 0:
        return string
    elif maximum > len(indexes):
        maximum = len(indexes) # Ensures setting max too high doesnt cause errors
    
    ls = len(substring)-1
    distances = [] # Lists of lists that will contain an index and its distance from origin
    # To get distances properly the end of the substring is used if it occurs before origin
    # and the start is used if it occurs after origin
    for index in indexes:
        if index <= origin and origin <= index + ls: #In case origin is inside a substring
            distances.append([index, 0])
        elif index < origin:
            distances.append([index, origin-index-ls])
        else:
            distances.append([index, index-origin])
            
    distances.sort(key=lambda x: x[1]) # Sort by distance from origin
    indexes = [entry[0] for entry in distances][:maximum] # Discard distances and unused indexes
    start, end = min(indexes), max(indexes)+ls+1 # Start/end of the section in which to perform replacements
    replaced_section = string[start:end].replace(substring, replacer)
    string = string[:start] + replaced_section + string[end:]
    
    if positions:
        return string, sorted(indexes)
    else:
        return string

def line_convert(source):
    """Convert alignment file text to list of lines"""
    file = open(source + '.ali', 'r')
    data = file.read()
    file.close()
    lines = data.split('\n')
    return lines

def get_structure(ali_filename, sources):
    """Formats alignment file data. Output is a list, where the i'th entry is a list of all the 
    lines of the i'th source. The final entry is the target's list of lines."""
    output = []
    # Cutpoints contains the starting position of each source
    cutpoints = []
    lines = line_convert(ali_filename)
    # Checking each line
    for i in range(len(lines)):
        # Check if a line contains a source
        for source in sources:
            if lines[i].endswith(source):
                cutpoints.append(i)
                break
                    
    # Constructing the output by appending lists of lines
    output.append(lines[0:cutpoints[0]])
    for i in range(len(cutpoints) - 1):
        lower = cutpoints[i]
        upper = cutpoints[i+1]
        output.append(lines[lower:upper])
    output.append(lines[cutpoints[-1]:-1] + [lines[-1]])
    
    return tuple(tuple(x) for x in output)

def structure_to_file(structure, filename='untitled', extension='.txt'):
    """Writes structure to a file."""
    file = open(filename + extension, 'w+')
    slen = len(structure)
    for i in range(slen):
        block = structure[i]
        blen = len(block)
        for j in range(blen):
            line = block[j]
            # Ensuring the last line doesnt get a newline character after it
            if i == slen-1 and j == blen-1:
                file.write(line)
            else:
                file.write(line + '\n')
    file.close()
    return
        
def insert_mutation(structure, linenum, mutation, pos=-1):
    """If pos is specified, inserts mutation into said position.
    Otherwise the mutation is appended to the end of the line"""
    # Appends to end of line if pos is unchanged
    structure  = list(list(x) for x in structure)
    linenum += 2
    if pos==-1:
        pos = len(structure[-1][linenum])
        
    # Alligning sources, excluding first and last term since these 
    # are the header and target respectively
    
    for i in range(1, len(structure)-1):
        line = structure[i][linenum]
        structure[i][linenum] = line[:pos] + '-'*len(mutation) + line[pos:]
        
    # Mutating target
    line = structure[-1][linenum]
    structure[-1][linenum] = line[:pos] + mutation + line[pos:]

    return tuple(tuple(x) for x in structure)

def replace_mutation(structure, linenum, original='-', mutation='-', maximum=-1, origin = 0):
    """If original and mutation are specified, replaces original with mutation
    on the given line. If only original is specified deletes original from the
    specified line. If neither is specified, deletes the entire line."""
    structure  = list(list(x) for x in structure)
    linenum += 2
    line = structure[-1][linenum]
    
    # For deleting entire line
    if original == '-':
        original = line
    
    # Inserting '-' according to relative length of original and mutation
    diff = len(original) - len(mutation)
    if diff > 0:
        mutation += '-'*diff
        structure[-1][linenum] = proximity_replace(line, original, mutation, origin, maximum)
        
    elif diff < 0:
        structure[-1][linenum], positions = proximity_replace(line, original, mutation, origin, maximum, positions=True)
        positions = [position + len(original) for position in positions] # Making positions refer to ends of substrings
        for i in range(1, len(structure)-1):
            line = structure[i][linenum]

            for j in range(len(positions)):
                position = positions[j] + j*diff
                line = line[:position] + '-'*(-diff)  + line[position:]
                
            structure[i][linenum] = line
            
    else:
        structure[-1][linenum] = proximity_replace(line, original, mutation, origin, maximum)
    
    return tuple(tuple(x) for x in structure)
