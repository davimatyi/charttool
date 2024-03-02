import os
import re
import time
import subprocess

import pygame

def read_chart_file(chart_file):
    song_info = {}
    synctrack = []
    events = []
    notes = []

    with open(chart_file, 'r') as file:
        section = "Song"
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                continue
            if section == 'Song' and '=' in line:
                key, value = line.split('=')
                song_info[key.strip()] = value.strip().strip('"')
            elif section == 'SyncTrack':
                match = re.match(r'(\d+)\s+=\s+B\s+([\w\s]+)', line)
                if match:
                    synctrack.append((int(match.group(1)), int(match.group(2))))
            elif section == 'Events':
                match = re.match(r'(\d+)\s+=\s+E\s+"(lyric[^"]+)"', line)
                if match:
                    events.append((int(match.group(1)), match.group(2)))
            elif "Single" in section:
                match = re.match(r'(\d+)\s+=\s+N\s+([\w\s]+)\s+([\w\s]+)', line)
                if match:
                    notes.append((int(match.group(1)), int(match.group(2))))

    return song_info, synctrack, events, notes

def play_music(mp3_file):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()

def synchronize_lyrics(song_info, synctrack, events, notes):
    resolution = int(song_info.get('Resolution', 192))

    current_bpm_index = 1
    current_event_index = 1
    current_note_index = 1
    current_bpm_position, current_bpm = synctrack[0]
    current_event_position, current_event = events[0]
    current_note_position, current_note = notes[0]
    ticks_elapsed = 0
    start_time = int(time.time() * 1000)
    current_time = int(time.time() * 1000)
    
    while current_event_index < len(events):
        current_time = int(time.time() * 1000)
        tpms = current_bpm * resolution / 60 / 1000.0
        ticks_elapsed = int((current_time - start_time) / 1000.0 * tpms)
        
        temp_notes = []
        while current_note_index < len(notes) and current_note_position <= ticks_elapsed:
            temp_notes.append(current_note)
            current_note_position, current_note = notes[current_note_index]
            current_note_index += 1
        
        temp_str = ''
        if len(temp_notes) > 0:
            if 0 in temp_notes: temp_str += '#'
            else: temp_str += '.'
            if 1 in temp_notes: temp_str += '#'
            else: temp_str += '.'
            if 2 in temp_notes: temp_str += '#'
            else: temp_str += '.'
            if 3 in temp_notes: temp_str += '#'
            else: temp_str += '.'
            if 4 in temp_notes: temp_str += '#'
            else: temp_str += '.'
            print(temp_str)
        
        while current_event_index < len(events) and current_event_position <= ticks_elapsed:
            # print(ticks_elapsed, current_event)
            current_event_position, current_event = events[current_event_index]
            current_event_index += 1
        if current_bpm_index < len(synctrack) and current_bpm_position <= ticks_elapsed:
            current_bpm_position, current_bpm = synctrack[current_bpm_index]
            current_bpm_index += 1
            
        


if __name__ == "__main__":
    chart_file = "./EC_Tekkno/notes.chart"  # Change this to your .chart file path
    mp3_file = "./EC_Tekkno/song.ogg"  # Change this to your audio file path

    if not os.path.isfile(chart_file):
        print("Error: Chart file not found.")
    elif not os.path.isfile(mp3_file):
        print("Error: MP3 file not found.")
    else:
        song_info, synctrack, events, notes = read_chart_file(chart_file)
        print(song_info['Name'])
        play_music(mp3_file)
        synchronize_lyrics(song_info, synctrack, events, notes)