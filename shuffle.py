import random
import struct
import os

def randomize_and_patch(seed=None, filters=None):
    # --- CONFIGURATION ---
    input_bin = "BtlEnmyPrm2.bin"      # Original .bin file extracted from the ROM
    rom_original = "temp_uploads/dqmj2.nds"      # Original ROM (must match the one used to extract the .bin,will be removerd in the future for security reasons)
    rom_output = "dqmj2_RANDOM.nds"   # Output ROM with randomized monsters
    
    entry_size = 100
    header_size = 8
    if filters is not None:
        print(f"Filters applied : {filters}")
    if seed is not None:
        random.seed(seed)
        rom_output = f"output/dqmj2_{seed}.nds"
    else:
        user_seed = random.randint(0, 999999)
        random.seed(user_seed)
        rom_output = f"output/dqmj2_{user_seed}.nds"

    # Read the original .bin file and parse its entries
    with open(input_bin, "rb") as f:
        data_bin = f.read()
        
    header = data_bin[:header_size]
    body = data_bin[header_size:]
    num_entries = len(body) // entry_size
    entries = [body[i * entry_size : (i + 1) * entry_size] for i in range(num_entries)]
        
    # Filtering monster that have an ID superior to 0
    valid_indices = [i for i, e in enumerate(entries) if struct.unpack("<H", e[0:2])[0] > 0]#623
        
    print(f"Monsters with ID : {len(valid_indices)} / {num_entries}")#623/1400
        
    #Advanced filtering based on user input
    valid_indices=filter_monsters(id_indices=valid_indices, filters=filters)

    if len(valid_indices)==0:
        print("No monsters available! Raising Exception")
        raise Exception("no monsters")
    base_pool = [entries[i] for i in valid_indices]

    pool=list(base_pool)
        
    while len(pool)<1400:
        pool.append(random.choice(base_pool))
    random.shuffle(pool)

    new_entries = pool
            
    # Reconstructing the new .bin content
    randomized_bin_content = header + b"".join(new_entries)

    # 3. Injecting the randomized .bin into the ROM
    if not os.path.exists(rom_original):
        print(f"Error : File {rom_original} not found!")
        return

    print(f"Opening ROM {rom_original} for injection...")
    with open(rom_original, "rb") as f:
        rom_data = bytearray(f.read())

    # Looking for the original .bin data in the ROM to find the correct offset for patching
    search_pattern = data_bin[:64]
    offset = rom_data.find(search_pattern)

    if offset == -1:
        print("Error : Impossible to find the location of the .bin file in the ROM.")
        print("Please ensure you are using the correct ROM from which the .bin was extracted.")
        return

    print(f"File found in the ROM at offset : {hex(offset)}")
        
    # Replacing the original .bin content with the new randomized content
    rom_data[offset : offset + len(randomized_bin_content)] = randomized_bin_content

    # Saving the modified ROM
    with open(rom_output, "wb") as f:
        f.write(rom_data)

    print(f"Processing completed! New ROM created : {rom_output}")
    if seed:
        print(f"Seed used : {seed}")


def filter_monsters(id_indices,filters=None):
    monster_db="valid_monsters.txt"
    with open(monster_db, 'r') as f:
            lines=f.readlines()
    if filters==None:
        valid_indices=[int(i.split(",")[0]) for i in lines]
    else:
        #filtering problematic monsters
        valid_indices=[int(i.split(",")[0]) for i in lines]
        for key,value in filters.items():
            if key=="rank":#exclude following ranks
                filtered_indices=[int(i.split(",")[0]) for i in lines if i.split(",")[9].strip() not in value]
                valid_indices=list(set(valid_indices) & set(filtered_indices))
            if key=="family":#exclude following families
                filtered_indices=[int(i.split(",")[0]) for i in lines if i.split(",")[10].strip() not in value]
                valid_indices=list(set(valid_indices) & set(filtered_indices))
            if key=="size":#exclude following sizes
                filtered_indices=[int(i.split(",")[0]) for i in lines if i.split(",")[11].strip() not in value]
                valid_indices=list(set(valid_indices) & set(filtered_indices))
    global_indices=[id_indices[e] for i,e in enumerate(valid_indices)]
    return global_indices

#if __name__ == "__main__":
#    randomize_and_patch()