import numpy as np
from tensorflow.keras.models import load_model
from music21 import instrument, note, stream

# Load trained model
model = load_model("music_model.h5")

# Create a simple music stream
output_notes = []

for i in range(50):
    new_note = note.Note(np.random.choice(
        ['C4','D4','E4','F4','G4','A4','B4']
    ))
    new_note.offset = i * 0.5
    new_note.storedInstrument = instrument.Piano()
    output_notes.append(new_note)

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='generated_music.mid')

print("Music generated successfully!")