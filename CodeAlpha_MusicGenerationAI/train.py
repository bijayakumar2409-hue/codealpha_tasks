import os
import glob
import numpy as np
from music21 import converter, instrument, note, chord
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
def get_notes():
    notes = []

    for file in glob.glob("**/*.mid", recursive=True):
        midi = converter.parse(file)

        for element in midi.flatten().notes:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    return notes


notes = get_notes()
print("Total notes:", len(notes))
sequence_length = 100

pitchnames = sorted(set(notes))
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]

    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])

n_patterns = len(network_input)

network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
network_input = network_input / float(len(pitchnames))

network_output = to_categorical(network_output)
model = Sequential()

model.add(LSTM(
    256,
    input_shape=(network_input.shape[1], network_input.shape[2]),
    return_sequences=True
))
model.add(Dropout(0.3))

model.add(LSTM(256))
model.add(Dropout(0.3))

model.add(Dense(128, activation="relu"))
model.add(Dense(network_output.shape[1], activation="softmax"))

model.compile(
    loss="categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)

print(model.summary())
model.fit(
    network_input,
    network_output,
    epochs=20,
    batch_size=64
)

model.save("music_model.h5")

print("Training Completed!")