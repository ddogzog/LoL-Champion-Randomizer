import tkinter as tk
import random
import time
import math
import pygame
import json
from PIL import Image, ImageTk
from tkinter import Tk, Label
import os
import sys

'''
Plans for next revision are to use the currently labeled 'Undo' button as a bank/hold option that appends the current_champion into a new list.
That list will be structured identiacally to champions and completed_champions. The append will put the champion into its appropriate lane.
That way, the held champion only displays above the randomizer button if the appropriate lane is selected, which means up to 5 champions can
be held. Since it is not moved into completed_champions, which is what is referenced for most of the stats, it should not interfere with that code.
But, it will still be available in the randomizer pool unless an if statement is added that checks against that list as well for available champs.
potentially turn the undo button into hold/swap button

The action for it would first check to see if it can swap, if no swap available, it will append the list and clear the spinframe, it would then unlock
the randomizer button so another champion can be randomized.
'''
#List of Champions left in Random Pool
champions = {
    "Top":
    ["Aatrox", "Ambessa", "Aurora", "Camille", "Cho'Gath", "Darius", "Dr. Mundo", 
    "Fiora", "Gangplank", "Garen", "Gnar", "Gwen", "Heimerdinger", "Illaoi", 
    "Irelia", "Jax", "Jayce", "Kayle", "Kennen", "Kled", "K'Sante", "Malphite", 
    "Mordekaiser", "Nasus", "Olaf", "Ornn", "Quinn", "Renekton", "Riven", 
    "Rumble", "Sett", "Shen", "Singed", "Sion", "Teemo", "Tryndamere", 
    "Urgot", "Volibear", "Wukong", "Yorick"],
    
    "Jungle":
    ["Amumu", "Bel'Veth", "Briar", "Diana", "Ekko", "Elise", "Evelynn", "Fiddlesticks", 
    "Gragas", "Graves", "Hecarim", "Ivern", "Jarvan IV", "Karthus", "Kayn", 
    "Kha'Zix", "Kindred", "Lee Sin", "Lilia", "Master Yi", "Neeko", "Nidalee", 
    "Nocturne", "Nunu & Willump", "Poppy", "Rammus", "Rek'Sai", "Rengar", 
    "Sejuani", "Shaco", "Shyvana", "Skarner", "Trundle", "Udyr", "Vi", "Viego", 
    "Warwick", "Xin Zhao", "Zac"],
    
    "Middle":
    ["Ahri", "Akali", "Akshan", "Anivia", "Annie", "Aurelion Sol", "Azir", 
    "Cassiopeia", "Fizz", "Galio", "Hwei", "Kassadin", "Katarina", 
    "LeBlanc", "Lissandra", "Malzahar", "Naafiri", "Orianna", "Pantheon", 
    "Qiyana", "Ryze", "Sylas", "Syndra", "Taliyah", "Talon", "Twisted Fate", 
    "Veigar", "Vex", "Viktor", "Vladimir", "Yasuo", "Yone", "Zed", "Ziggs", "Zoe"],
    
    "Bottom":
    ["Aphelios", "Ashe", "Caitlyn", "Corki", "Draven", "Ezreal", "Jhin", "Jinx", "Kai'sa", 
    "Kalista", "Kog'Maw", "Lucian", "Miss Fortune", "Nilah", "Samira", "Sivir", 
    "Smolder", "Tristana", "Twitch", "Varus", "Vayne", "Xayah", "Zeri"],
    
    "Support":
    ["Alistar", "Bard", "Blitzcrank", "Brand", "Braum", "Janna", "Karma", "Leona", 
    "Lulu", "Lux", "Maokai", "Milio", "Morgana", "Nami", "Nautilus", "Pyke", 
    "Rakan", "Rell", "Renata Glasc", "Senna", "Seraphine", "Sona", "Soraka", 
    "Swain", "Tahm Kench", "Taric", "Thresh", "Vel'Koz", "Xerath", "Yuumi", 
    "Zilean", "Zyra"]
}

stats = {
    "Top":      {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
    "Jungle":   {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
    "Middle":   {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
    "Bottom":   {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
    "Support":  {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
    "Overall":  {"wins": 0, "losses": 0, "games": 0, "progress":0.0}
}

#List of Completed Champions
completed_champions = {
    "Top":
    [],
    
    "Jungle":
    [],
    
    "Middle":
    [],
    
    "Bottom":
    [],
    
    "Support":
    []
}

poolchampions = []

lanes = list(champions.keys())
is_muted = False

file_path = "stats.json"

action_stack = []
max_stack_size = 10
if len(action_stack) >= max_stack_size:
    action_stack.pop(0)

#Defined
def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

def jsonsave(file_path):
    data = {
        "stats": stats,
        "completed_champions": completed_champions
    }
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)  # Indent for readability

def jsonload(file_path):
    global stats, completed_champions
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            stats = data.get("stats", stats)  # Use existing stats as fallback
            completed_champions = data.get("completed_champions", completed_champions)
            return data
    except FileNotFoundError:
        return{}
    except json.JSONDecodeError:
        return{}

def randomize():
    if not poolchampions:
        return
    for i in range(15):  # Number of steps in the animation
        disablerandomize()
        random_option = random.choice(poolchampions)  # Pick a random combination
        spinlabel.config(text=random_option, fg="#6F96CB")  # Update the visible label
        root.update()  # Refresh the GUI to display changes
        time.sleep(0.05 + (i / 120))  # Gradually slow down the rolling effect
    # Display the final result
    final_choice = random.choice(poolchampions)
    spinlabel.config(text=final_choice, fg="green")
    enablewinloss()

def winner():
    current_lane = lane_selector.get()
    empty = spinlabel.cget("text")
    current_champion = spinlabel.cget("text")
    if current_lane in stats and empty in poolchampions:
        update_stats(current_lane, is_win=True)
    disablewinloss()
    enablerandomize()

def disablerandomize():
    button3.configure(command= 0)

def enablerandomize():
    button3.configure(command=randomize)

def disablewinloss():
    button.configure(command= 0)
    button1.configure(command= 0)
    button2.configure(command= 0)

def enablewinloss():
    button.configure(command=winner)
    button1.configure(command=loser)
    button2.configure(command= 0) #change to undo button command once finished

def laneselect(selected_lane):
    global poolchampions
    lane_selector.set(selected_lane)
    poolchampions = [champion for champion in champions[lane_selector.get()] if champion not in completed_champions[lane_selector.get()]]
    spinlabel.config(text="                    " if poolchampions else "Completed")
    lanechoice.config(text=selected_lane)

def update_remainder():
    global poolchampions
    poolchampions = [champion for champion in champions[lane_selector.get()] if champion not in completed_champions[lane_selector.get()]]

def reset():
    global completed_champions, stats
    stats = {
        "Top":      {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
        "Jungle":   {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
        "Middle":   {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
        "Bottom":   {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
        "Support":  {"wins": 0, "losses": 0, "games": 0, "progress":0.0},
        "Overall":  {"wins": 0, "losses": 0, "games": 0, "progress":0.0}
    }
    #Update Labels
    ovtot.config(text="0")
    ovwr.config(text="0.0%")
    ovper.config(text="0.0%")
    toptot.config(text="0")
    juntot.config(text="0")
    midtot.config(text="0")
    bottot.config(text="0")
    suptot.config(text="0")
    topwr.config(text="0.0%")
    junwr.config(text="0.0%")
    midwr.config(text="0.0%")
    botwr.config(text="0.0%")
    supwr.config(text="0.0%")
    topper.config(text="0.0%")
    junper.config(text="0.0%")
    midper.config(text="0.0%")
    botper.config(text="0.0%")
    supper.config(text="0.0%")
       
    completed_champions = {
        "Top":
        [],
        
        "Jungle":
        [],
        
        "Middle":
        [],
        
        "Bottom":
        [],
        
        "Support":
        []
    }
    spinlabel.config(text="                    ")
    jsonsave(file_path)

def loser():
    current_lane = lane_selector.get()
    empty = spinlabel.cget("text")
    if current_lane in stats and empty in poolchampions:
        update_stats(current_lane, is_win=False)
    spinlabel.config(text="                    ")
    disablewinloss()
    enablerandomize()

def toggle_mute():
    global is_muted
    if is_muted:
        pygame.mixer.music.set_volume(volume_slider.get() / 100)  # Restore volume
        mute_button.config(text="Mute")
        is_muted = False
    else:
        pygame.mixer.music.set_volume(0)  # Mute music
        mute_button.config(text="Unmute")
        is_muted = True

def set_volume(val):
    if not is_muted:  # Only change volume if not muted
        pygame.mixer.music.set_volume(float(val) / 100)

def update_stats(lane, is_win):
    # Update lane-specific stats
    lanechampions = len(champions[lane])
    current_champion = spinlabel.cget("text")
    if lane in stats:
        stats[lane]["games"] += 1
        if is_win:
            if current_champion in poolchampions and current_champion not in completed_champions:
                completed_champions[lane].append(current_champion)
                update_remainder()  
                empty = lanechoice.cget("text")
                spinlabel.config(text="                    " if poolchampions else "Completed" if empty != "" else "                    ")
                stats[lane]["wins"] += 1
                lanecompletedchampions = len(completed_champions.get(lane, []))
                stats[lane]["progress"] = (lanecompletedchampions / lanechampions) * 100
        else: 
            stats[lane]["losses"] += 1

        # Calculate win rate & progress
        if stats[lane]["games"] > 0:
            lane_win_rate = (stats[lane]["wins"] / stats[lane]["games"]) * 100
            lanecompletedchampions = len(completed_champions.get(lane, []))
            lane_progress = (lanecompletedchampions / lanechampions) * 100
        else:
            lane_win_rate = 0
            lane_progress = 0
        # Update labels for the selected lane
        lane_tot_label = globals()[f"{lane[:3].lower()}tot"]
        lane_wr_label = globals()[f"{lane[:3].lower()}wr"]
        lane_per_label = globals()[f"{lane[:3].lower()}per"]
        lane_tot_label.config(text=f"{stats[lane]['games']}")
        lane_wr_label.config(text=f"{lane_win_rate:.1f}%")
        lane_per_label.config(text=f"{lane_progress:.1f}%")

    # Update overall stats
    totalchampions = sum(len(champ_list) for champ_list in champions.values())
    totalcompletedchampions = sum(len(completed_list) for completed_list in completed_champions.values())
    stats["Overall"]["games"] += 1
    if is_win:
        stats["Overall"]["wins"] += 1
        stats["Overall"]["progress"] = (totalcompletedchampions / totalchampions) * 100
    else: 
        stats["Overall"]["losses"] += 1

    # Calculate overall win rate & progress
    if stats["Overall"]["games"] > 0:
        overall_win_rate = (stats["Overall"]["wins"] / stats["Overall"]["games"]) * 100
        overall_progress = (totalcompletedchampions / totalchampions) * 100
    else:
        overall_win_rate = 0
        overall_progress = 0
    # Update overall labels
    ovtot.config(text=f"{stats['Overall']['games']}")
    ovwr.config(text=f"{overall_win_rate:.1f}%")
    ovper.config(text=f"{overall_progress:.1f}%")
    jsonsave(file_path)

#Music
pygame.mixer.init()
pygame.mixer.music.load(get_path("sounds.wav"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.01) #change to 10 and change button slider to 10

root = tk.Tk()
root.title('Blueshell Champion Randomizer')
root.iconbitmap(get_path('icon.ico'))
root.configure(bg="#6F96CB")
root.geometry("1280x720")
root.resizable(False, False)

jsonload(file_path)

#Frames
frame = tk.Frame(root, bg="#202020", width=1240, height=680)
frame.grid_propagate(False)
frame.grid(row=0, column=0, padx=20, pady=20)

frame.grid_columnconfigure(0, weight=1, minsize=248)
frame.grid_columnconfigure(1, weight=1, minsize=248)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1, minsize=248)
frame.grid_columnconfigure(4, weight=1, minsize=248)

frame.grid_rowconfigure(0, weight=1, minsize=136)
frame.grid_rowconfigure(1, weight=1, minsize=136)
frame.grid_rowconfigure(2, weight=1, minsize=136)
frame.grid_rowconfigure(3, weight=1, minsize=136)
frame.grid_rowconfigure(4, weight=1, minsize=136)

frame1 = tk.Frame(frame, bg="#202020")
frame1.grid_propagate(False)
frame1.grid(row=1, column=0, columnspan=5, sticky="nsew")

frame1.grid_columnconfigure(0, weight=1, minsize=248)
frame1.grid_columnconfigure(1, weight=1, minsize=248)
frame1.grid_columnconfigure(2, weight=1, minsize=248)
frame1.grid_columnconfigure(3, weight=1, minsize=248)
frame1.grid_columnconfigure(4, weight=1, minsize=248)

frame2 = tk.Frame(frame, bg="#202020", height=75, width=300)
frame2.grid_propagate(True)
frame2.grid(row=3, column=1, columnspan=3)

frame2.grid_columnconfigure(0, weight=1, minsize=100)
frame2.grid_columnconfigure(1, weight=1, minsize=100)
frame2.grid_columnconfigure(2, weight=1, minsize=100)

frame2.grid_rowconfigure(0, weight=1, minsize=25)
frame2.grid_rowconfigure(1, weight=1, minsize=25)
frame2.grid_rowconfigure(2, weight=1, minsize=25)

frame3 = tk.Frame(frame, bg="#202020")
frame3.grid_propagate(False)
frame3.grid(row=3, column=4, sticky="nsew")

#Music Buttons/Sliders
mute_button = tk.Button(frame, text="Mute", command=toggle_mute, font=("Stencil", 10), bg="#202020", fg="#6F96CB")
mute_button.grid(row=0, column=4, sticky="n")

volume_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", command=set_volume, font=("Stencil", 10), bg="#202020", fg="#6F96CB", highlightthickness=0)
volume_slider.set(1)  # Set initial volume
volume_slider.grid(row=0, column=4, sticky="ne")

#Logo Image
image = Image.open(get_path("blueshellbitmap.png"))
image = image.resize((100, 100), Image.Resampling.LANCZOS)
image_tk = ImageTk.PhotoImage(image)

#Buttons
button = tk.Button(frame, text= "Win", font=("Stencil", 16), command= 0, bg="#6F96CB", bd=15, relief="ridge")
button.grid(row=2, column=1, sticky="e")

button1 = tk.Button(frame, text= "Loss", font=("Stencil", 16), command= 0, bg="#6F96CB", bd=15, relief="ridge")
button1.grid(row=2, column=2)

button2 = tk.Button(frame, text= "Undo", font=("Stencil", 16), command= 0, bg="#6F96CB", bd=15, relief="ridge")
button2.grid(row=2, column=3, sticky="w")

button3 = tk.Button(frame, text= "Randomize", command=randomize, font=("Stencil", 16), bg="#6F96CB", bd=15, relief="ridge")
button3.grid(row=4, column=2)

button4 = tk.Button(frame, text= "Reset", font=("Stencil", 14), command=reset, bg="#6F96CB")
button4.grid(row=4, column=4, sticky="se")

#Labels
holdswap = tk.Label(frame, text= "", font=("Stencil", 12), bg="#202020", fg="#6F96CB")
holdswap.grid(row=3, column=2, sticky="s")

label = tk.Label(frame, text= "Blueshell Champion Randomizer", font=("Stencil", 20), bg="#202020", fg="#6F96CB")
label.grid(row=4, column=0, columnspan=2, sticky="n")

label1 = tk.Label(frame, text= "By: Ddogzog", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label1.grid(row=4, column=0, columnspan=2)

label2 = tk.Label(frame, image=image_tk, bg="#202020")
label2.grid(row=4, column=0, sticky="sw")

label3 = tk.Label(frame1, text= "Top", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label3.grid(row=0, column=0, sticky="e")

label4 = tk.Label(frame1, text= "Jungle", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label4.grid(row=0, column=1)

label4 = tk.Label(frame1, text= "Middle", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label4.grid(row=0, column=2)

label5 = tk.Label(frame1, text= "Bottom", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label5.grid(row=0, column=3)

label6 = tk.Label(frame1, text= "Support", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label6.grid(row=0, column=4)

label7 = tk.Label(frame3, text= "Overall", font=("Stencil", 18), bg="#202020", fg="#6F96CB")
label7.grid(row=0, column=1)

label11 = tk.Label(frame3, text= "Progress", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
label11.grid(row=1, column=0, sticky="w")

label12 = tk.Label(frame3, text= "Tot Games", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
label12.grid(row=3, column=0, sticky="w")

label13 = tk.Label(frame3, text= "W/R", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
label13.grid(row=2, column=0, sticky="w")

lanechoice = tk.Label(frame, text= "", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
lanechoice.grid(row=3, column=2, sticky="n")

ovper = tk.Label(frame3, text=f"{stats['Overall']['progress']:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
ovper.grid(row=1, column=1)

ovtot = tk.Label(frame3, text=f"{stats['Overall']['games']}", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
ovtot.grid(row=3, column=1)

ovwr = tk.Label(frame3, text=f"{(stats['Overall']['wins'] / stats['Overall']['games'] * 100) if stats['Overall']['games'] > 0 else 0:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
ovwr.grid(row=2, column=1)

label8 = tk.Label(frame1, text= "Progress", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
label8.grid(row=1, column=0, sticky="w")

label9 = tk.Label(frame1, text= "Tot Games", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
label9.grid(row=3, column=0, sticky="w")

label10 = tk.Label(frame1, text= "W/R", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
label10.grid(row=2, column=0, sticky="w")

topper = tk.Label(frame1, text=f"{stats['Top']['progress']:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
topper.grid(row=1, column=0, sticky="e")

toptot = tk.Label(frame1, text=f"{stats['Top']['games']}", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
toptot.grid(row=3, column=0, sticky="e")

topwr = tk.Label(frame1, text=f"{(stats['Top']['wins'] / stats['Top']['games'] * 100) if stats['Top']['games'] > 0 else 0:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
topwr.grid(row=2, column=0, sticky="e")

junper = tk.Label(frame1, text=f"{stats['Jungle']['progress']:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
junper.grid(row=1, column=1)

juntot = tk.Label(frame1, text=f"{stats['Jungle']['games']}", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
juntot.grid(row=3, column=1)

junwr = tk.Label(frame1, text=f"{(stats['Jungle']['wins'] / stats['Jungle']['games'] * 100) if stats['Jungle']['games'] > 0 else 0:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
junwr.grid(row=2, column=1)

midper = tk.Label(frame1, text=f"{stats['Middle']['progress']:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
midper.grid(row=1, column=2)

midtot = tk.Label(frame1, text=f"{stats['Middle']['games']}", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
midtot.grid(row=3, column=2)

midwr = tk.Label(frame1, text=f"{(stats['Middle']['wins'] / stats['Middle']['games'] * 100) if stats['Middle']['games'] > 0 else 0:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
midwr.grid(row=2, column=2)

botper = tk.Label(frame1, text=f"{stats['Bottom']['progress']:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
botper.grid(row=1, column=3)

bottot = tk.Label(frame1, text=f"{stats['Bottom']['games']}", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
bottot.grid(row=3, column=3)

botwr = tk.Label(frame1, text=f"{(stats['Bottom']['wins'] / stats['Bottom']['games'] * 100) if stats['Bottom']['games'] > 0 else 0:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
botwr.grid(row=2, column=3)

supper = tk.Label(frame1, text=f"{stats['Support']['progress']:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
supper.grid(row=1, column=4)

suptot = tk.Label(frame1, text=f"{stats['Support']['games']}", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
suptot.grid(row=3, column=4)

supwr = tk.Label(frame1, text=f"{(stats['Support']['wins'] / stats['Support']['games'] * 100) if stats['Support']['games'] > 0 else 0:.1f}%", font=("Stencil", 16), bg="#202020", fg="#6F96CB")
supwr.grid(row=2, column=4)

spinlabel = tk.Label(frame2, text="                    ", font=("Stencil", 30, "bold"), bg="#202020", fg="#6F96CB", bd=5, relief="ridge", padx=5, pady=5)
spinlabel.grid(row=1, column=1)

#Dropdown menu
lane_selector = tk.StringVar (frame)
lane_selector.set("Choose your Lane")
dropdown = tk.OptionMenu(frame, lane_selector, *lanes, command=laneselect)
dropdown.config(font=("Stencil", 12), bg="#202020", fg="#6F96CB", highlightthickness=0)
dropdown["menu"].config(bg="#202020", fg="#6F96CB", font=("Stencil", 12))
dropdown.grid(row=0, column=0, sticky="nw")


root.mainloop()
