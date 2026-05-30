from shuffle import randomize_and_patch
from nicegui import ui,app,run
from pathlib import Path
from randomInfo import RandomizationInfo
import os
import asyncio


UPLOAD_DIR = Path(__file__).parent / 'temp_uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

output_dir= Path(__file__).parent / 'output'


randInfo=RandomizationInfo()

def change_filter(key,value):
    if key in randInfo.filters:
        if value in randInfo.filters[key]:
            randInfo.filters[key].remove(value)
            if len(randInfo.filters[key])==0:
                randInfo.filters.pop(key,None)
        else:
            randInfo.filters[key].append(value)
    else:
        randInfo.filters[key]=[value]
    print("Current filters: "+ str(randInfo.filters))

def set_seed(value):
    try:
        randInfo.seed=int(value[:-2])
    except ValueError:
        randInfo.seed=0

def change_mods(value):
    if value in randInfo.mods:
        randInfo.mods.remove(value)
    else:
        randInfo.mods.append(value)
    print("Current mods: "+ str(randInfo.mods))

async def uploaded(e):
    extension=e.file.name.split(".")[1]
    if extension=="nds":
        full_path = UPLOAD_DIR / "dqmj2.nds"

        with open(full_path, 'wb') as f:
            f.write(await e.file.read())
            f.flush()
    else:
        show_dialog("Please import .nds file!\nAlso click on the check mark to remove the file and retry!")

async def try_randomization():
    if Path("temp_uploads/dqmj2.nds").exists():
        with ui.dialog() as dialog, ui.card().classes("dqmj2-font"):
            ui.label("ROM is being randomized, please wait...")
            ui.spinner(size='lg')
            percent_label = ui.label("0% Complete!")
        dialog.open()

        try:
            await run.io_bound(randomize_and_patch, percent_label, randInfo)
            
            dialog.close()
            show_dialog("ROM randomized successfully in output folder!")
        except Exception as error:
            dialog.close()

def show_dialog(message):
    with ui.dialog() as dialog,ui.card().classes("dqmj2-font"):
        ui.label(message)
        ui.button("OK",on_click=dialog.close)
    dialog.open()

@ui.page('/')
def root():
    app.add_static_files('/static', 'fonts')
    ui.add_head_html(r'''
    <style>
    @font-face{
        font-family: "depixelklein";
        src: url('/static/depixelklein.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }
    .dqmj2-font{
        font-family: 'depixelklein';
                      }
    .section-banner{
                     background: radial-gradient(#083973, #105aad);
                     font-color: white;
    }
    .custom-btn:hover {
            background: red !important;
        }
    .custom-btn:hover .q-focus-helper {
            background: #fc7e0f !important;
            opacity: 1 !important;
        }
    .dqmj2-checkbox{
                     
                     }
    </style>
    ''')
    ui.query('body').style('background: radial-gradient(#bfbfbf, #636363); height: 100vh;')
    with ui.card().style("background: black;width: 100%").classes('text-center'):
        with ui.row():
            ui.label("DQMJ2 Randomizer").style("font-size: 40px;font-family: 'depixelklein'; color: white;")
            #ui.button("Close Randomizer",on_click=os.kill(os.getpid(), signal.SIGTERM))

    
    with ui.card().style("background:#5a5a5a;border-color: #bdbdbd;border-style: solid;border-width: 2px;width: 100%").classes('dqmj2-font'):
        with ui.row().classes("w-full"):
            ui.upload(auto_upload=True,label="Import EU DQMJ2 ROM:",max_files=1,on_upload=lambda e: uploaded(e))
            ui.number("Seed", value=0, precision=0,step=1, on_change=lambda e: set_seed(str(e.value))).style("background: white;")
        if Path("temp_uploads/dqmj2.nds").exists():
                ui.label("ROM already imported!").classes("text-green")
        with ui.tabs().classes('w-full') as tabs:
            monsters = ui.tab('Monsters')
            challenges = ui.tab('Challenges')
        with ui.tab_panels(tabs, value=monsters).classes('w-full'):
            with ui.tab_panel(monsters):
                with ui.checkbox("Allow Flee and Scout for all battles", value=True, on_change=lambda e: change_mods("always_flee")):
                    ui.tooltip("Make Flee and Scout options always available,even in boss fights").classes("bg-cyan")
                with ui.checkbox("Remove 0 XP monsters (such as arena monsters)", value=True, on_change=lambda e: change_filter("special","no_arena_monsters")):
                     ui.tooltip("Remove special monster such as arena monsters giving 0 XP and sometime 0 Gold").classes("bg-cyan")
                with ui.expansion('Filter Ranks', icon='font_download',caption="Include or exclude monster ranks you want").classes('w-full section-banner text-white rounded'):
                    with ui.row().classes('w-full'):
                        ui.checkbox("???", value=True, on_change=lambda e: change_filter("rank","???"))
                        ui.checkbox("X", value=True, on_change=lambda e: change_filter("rank","X"))
                        ui.checkbox("S", value=True, on_change=lambda e: change_filter("rank","S"))
                        ui.checkbox("A", value=True, on_change=lambda e: change_filter("rank","A"))
                        ui.checkbox("B", value=True, on_change=lambda e: change_filter("rank","B"))
                        ui.checkbox("C", value=True, on_change=lambda e: change_filter("rank","C"))
                        ui.checkbox("D", value=True, on_change=lambda e: change_filter("rank","D"))
                        ui.checkbox("E", value=True, on_change=lambda e: change_filter("rank","E"))
                        ui.checkbox("F", value=True, on_change=lambda e: change_filter("rank","F"))

                with ui.expansion('Filter Families', icon='pets',caption="Include or exclude monster families you want").classes('w-full section-banner text-white rounded'):
                    with ui.row().classes('w-full'):
                        ui.checkbox("Beast", value=True, on_change=lambda e: change_filter("family","Beast"))
                        ui.checkbox("Nature", value=True, on_change=lambda e: change_filter("family","Nature"))
                        ui.checkbox("Dragon", value=True, on_change=lambda e: change_filter("family","Dragon"))
                        ui.checkbox("Demon", value=True, on_change=lambda e: change_filter("family","Demon"))
                        ui.checkbox("Undead", value=True, on_change=lambda e: change_filter("family","Undead"))
                        ui.checkbox("Material", value=True, on_change=lambda e: change_filter("family","Material"))
                        ui.checkbox("Slime", value=True, on_change=lambda e: change_filter("family","Slime"))
                        ui.checkbox("Boss", value=True, on_change=lambda e: change_filter("family","Boss"))

                with ui.expansion('Filter Size', icon='height',caption="Include or exclude monster sizes you want").classes('w-full section-banner text-white rounded'):
                    with ui.row().classes('w-full'):
                        ui.checkbox("Small", value=True, on_change=lambda e: change_filter("size","1"))
                        ui.checkbox("Medium", value=True, on_change=lambda e: change_filter("size","2"))
                        ui.checkbox("Giant", value=True, on_change=lambda e: change_filter("size","3"))
            with ui.tab_panel(challenges):
                with ui.checkbox("No flee challenge", value=False, on_change=lambda e: change_mods("no_flee")):
                    ui.tooltip("Do not flee anymore! Win or loss is the only way!   This challenge is disabled if \"Allow Flee and Scout for all battles\" is enabled!").classes("bg-cyan")
                with ui.checkbox("Stronger monsters (50% stats raise)", value=False, on_change=lambda e: change_mods("150%_stats")):
                    ui.tooltip("Monsters HP,MP,DEF,ATK,AGI and WIS are multiplied by 1.5").classes("bg-cyan")



        
    with ui.card().style("background:#5a5a5a;border-color: #bdbdbd;border-style: solid;border-width: 2px;width: 100%").classes('dqmj2-font'):
        with ui.row().classes("w-full"):
            ui.button("Randomize!", on_click=lambda: try_randomization()).classes('flex-1 text-white custom-btn').style("background: #105aad;")
            ui.button("Open output folder",on_click=lambda: os.startfile(output_dir)).classes("w-1/4")
if __name__ == '__main__':
    ui.run(reload=False,title="DQMJ2 Randomizer")
