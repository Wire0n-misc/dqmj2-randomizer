import random
import struct
import os
import nicegui
from randomInfo import RandomizationInfo
def randomize_and_patch(progress_label,randInfo=RandomizationInfo()):
    # --- CONFIGURATION ---
    input_bin = "BtlEnmyPrm2.bin"      # Original .bin file extracted from the ROM
    rom_original = "temp_uploads/dqmj2.nds"      # Original ROM (must match the one used to extract the .bin,will be removerd in the future for security reasons)
    rom_output = "dqmj2_RANDOM.nds"   # Output ROM with randomized monsters
    
    entry_size = 100
    header_size = 8

    randInfo.current_progress=0
    randInfo.max_progress=determine_task_number(randInfo)
    
    if randInfo.filters is not None:
        print(f"Filters applied : {randInfo.filters}")
    if randInfo.seed!=0:
        random.seed(randInfo.seed)
        rom_output = f"output/dqmj2_{randInfo.seed}.nds"
    else:
        user_seed = random.randint(0, 999999)
        random.seed(user_seed)
        rom_output = f"output/dqmj2_{user_seed}.nds"

    updateProgress(progress_label,randInfo)#task 1

    # Read the original .bin file and parse its entries
    with open(input_bin, "rb") as f:
        data_bin = f.read()
        
    header = data_bin[:header_size]
    body = data_bin[header_size:]
    num_entries = len(body) // entry_size
    entries = [body[i * entry_size : (i + 1) * entry_size] for i in range(num_entries)]
    
    updateProgress(progress_label,randInfo)#task 2

    # Filtering monster that have an ID superior to 0
    id_valid_indices = [i for i, e in enumerate(entries) if struct.unpack("<H", e[0:2])[0] > 0]#623
    print("Possible monsters before user filtering: "+str(len(id_valid_indices)))
    #print(f"Monsters with ID : {len(valid_indices)} / {num_entries}")#623/1400
    
    updateProgress(progress_label,randInfo)#task 3

    #Advanced filtering based on user input
    filtered_indices=filter_monsters(id_valid_indices,randInfo=randInfo,progress_label=progress_label,entries=entries)
    print("Possible monsters after user filtering: "+str(len(filtered_indices)))

    updateProgress(progress_label,randInfo)#task 4

    if len(filtered_indices)==0:
        print("No monsters available! Raising Exception")
        raise Exception("no monsters")
    final_valid_indices=[id_valid_indices[indice] for indice in filtered_indices]
    base_pool = [entries[i] for i in final_valid_indices]

    updateProgress(progress_label,randInfo)#task 5

    base_pool=mod_pool(base_pool,randInfo,progress_label)
    print("final possible monsters: "+str(len(base_pool)))
    pool=list(base_pool)

    updateProgress(progress_label,randInfo)#task 6

    while len(pool)<1400:
        pool.append(random.choice(base_pool))
    random.shuffle(pool)

    new_entries = pool
    
    updateProgress(progress_label,randInfo)#task 7

    # Reconstructing the new .bin content
    randomized_bin_content = header + b"".join(new_entries)

    # Injecting the randomized .bin into the ROM
    if not os.path.exists(rom_original):
        print(f"Error : File {rom_original} not found!")
        return

    print(f"Opening ROM {rom_original} for injection...")
    with open(rom_original, "rb") as f:
        rom_data = bytearray(f.read())

    # Looking for the original .bin data in the ROM to find the correct offset for patching
    search_pattern = data_bin[:64]
    offset = rom_data.find(search_pattern)

    updateProgress(progress_label,randInfo)#task 8

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
    
    updateProgress(progress_label,randInfo)#task 9

    print(f"Processing completed! New ROM created : {rom_output}")
    if randInfo.seed!=0:
        print(f"Seed used : {randInfo.seed}")

#altering the pool by modifying it's data (used for challenges)
def mod_pool(pool,randInfo=RandomizationInfo(),progress_label=None):
    new_pool=pool.copy()
    for mod in randInfo.mods:
        if mod=="no_flee" and "always_flee" not in randInfo.mods:
            for i,monster in enumerate(new_pool):
                new_pool[i]=monster[:98]+bytes([0x02])+monster[99:]
            updateProgress(progress_label,randInfo)
        if mod=="150%_stats":
            for i,monster in enumerate(new_pool):
                HP  = min(int(struct.unpack("<H", monster[48:50])[0] * 1.5), 9999)
                MP  = min(int(struct.unpack("<H", monster[50:52])[0] * 1.5), 9999)
                ATK = min(int(struct.unpack("<H", monster[52:54])[0] * 1.5), 9999)
                DEF = min(int(struct.unpack("<H", monster[54:56])[0] * 1.5), 9999)
                AGI = min(int(struct.unpack("<H", monster[56:58])[0] * 1.5), 9999)
                WIS = min(int(struct.unpack("<H", monster[58:60])[0] * 1.5), 9999)

                stats_pack = struct.pack("<6H", HP, MP, ATK, DEF, AGI, WIS)
                new_pool[i] = monster[:48] + stats_pack + monster[60:]
            updateProgress(progress_label,randInfo)
        if mod=="always_flee":
            for i,monster in enumerate(new_pool):
                new_pool[i]=monster[:98]+bytes([0x00])+monster[99:]
            updateProgress(progress_label,randInfo)
        if mod == "random_xp":
            probability_stack = {
                1: [0.0, 100.0, 0.0, 72.0],
                2: [100.0, 1000.0, 72.0, 92.0],
                3: [1000.0, 10000.0, 92.0, 97.0],
                4: [10000.0, 100000.0, 97.0, 99.0],
                5: [100000.0, 333333.0, 99.0, 100.0]
            }
            
            for i, monster in enumerate(new_pool):
                choosed = random.uniform(0.0, 100.0)
                
                for key in probability_stack:
                    interval = probability_stack[key] 
                    
                    if choosed > interval[2] and choosed <= interval[3]:
                        XP = int(random.uniform(interval[0], interval[1]))
                        new_pool[i] = monster[:39] + XP.to_bytes(3, "little") + monster[42:]
                        break 
                        
            updateProgress(progress_label, randInfo)
    return new_pool



def filter_monsters(id_indices,randInfo=RandomizationInfo(),progress_label=None,entries=None):
    monster_db="valid_monsters.txt"
    with open(monster_db, 'r') as f:
            lines=f.readlines()
    if randInfo.filters==None:
        valid_indices=[int(i.split(",")[0]) for i in lines]
    else:
        #filtering problematic monsters
        valid_indices=[int(i.split(",")[0]) for i in lines]
        for key,value in randInfo.filters.items():
            if key=="rank":#exclude following ranks
                filtered_indices=[int(i.split(",")[0]) for i in lines if i.split(",")[9].strip() not in value]
                valid_indices=list(set(valid_indices) & set(filtered_indices))
                updateProgress(progress_label,randInfo)

            if key=="family":#exclude following families
                filtered_indices=[int(i.split(",")[0]) for i in lines if i.split(",")[10].strip() not in value]
                valid_indices=list(set(valid_indices) & set(filtered_indices))
                updateProgress(progress_label,randInfo)

            if key=="size":#exclude following sizes
                filtered_indices=[int(i.split(",")[0]) for i in lines if i.split(",")[11].strip() not in value]
                valid_indices=list(set(valid_indices) & set(filtered_indices))
                updateProgress(progress_label,randInfo)

            if key=="special":#exlude special monsters such as arena monsters
                filtered_indices=[]
                for indice in valid_indices:
                    xp=int.from_bytes(entries[id_indices[indice]][39:42],byteorder="little")
                    if xp>0 :
                        filtered_indices.append(indice)
                
                valid_indices=list(set(valid_indices) & set(filtered_indices))
                updateProgress(progress_label,randInfo)
    return valid_indices


def determine_task_number(randInfo=RandomizationInfo()):
    res=0
    for mod in randInfo.mods:
        res+=1
    for filter in randInfo.filters:
        res+=1
    #manually defined tasks
    for i in range(0,9,1):
        res+=1
    return res

def updateProgress(progress_label,randInfo):
    randInfo.current_progress+=1
    progress = (randInfo.current_progress / randInfo.max_progress) * 100
    print(f"Randomization progression: {progress:.0f}%")
    progress_label.set_text(f"{progress:.0f}% Complete!")
    progress_label.update()

#debug function
def identify_monster_by_indice(indice):
    with open("valid_monsters.txt", 'r') as f:
            lines=f.readlines()
    for line in lines:
        if indice==int(line.split(",")[0]):
            print(line)
            return
    print("monster not found")

