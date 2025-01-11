import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def print_memory_usage():
    import os
    import psutil

    process = psutil.Process(os.getpid())
    print(f"Memory in MB used by Python process: {process.memory_info().rss / 1024 / 1024} MB")

print_memory_usage()

print("Loading audio file...")
import soundfile as sf
audio, samp_rate = sf.read("Silvester 2024.flac")

print_memory_usage()

bucket_size_seconds = 60
chunk_size = samp_rate*bucket_size_seconds

aggregated_data = pd.DataFrame(columns=['time_bucket', 'amplitude'])

for start in range(0, len(audio), chunk_size):
    end = min(start + chunk_size, len(audio))
    audio_chunk = audio[start:end]
    time_chunk = np.arange(start, end) / samp_rate

    #print_memory_usage()
    #print(f"Aggregated data is {len(aggregated_data)} rows long.")
    #print(f"Last rows of aggregated data:")
    #print(aggregated_data.tail())
    #print(f"Processing chunk from {start} to {end}...")

    print(".", end="")

    # Convert chunk to a data frame
    audio_data_chunk = pd.DataFrame({
        'time': time_chunk,
        'amplitude': audio_chunk
    })

    # Change the amplitude to a positive value
    audio_data_chunk['amplitude'] = audio_data_chunk['amplitude'].abs()

    # Add up all the amplitudes in the chunk
    aggregated_chunk = audio_data_chunk['amplitude'].sum()

    # Add the time and the aggregated amplitude to the aggregated data
    aggregated_data = pd.concat([aggregated_data, pd.DataFrame({
        'time_bucket': [(time_chunk.min() / 60)],
        'amplitude': [aggregated_chunk]
    })], ignore_index=True)

# Show the first few rows of the aggregated data
#print("Aggregated audio data:")
#print(aggregated_data.head())

print("\n")
print(f"Aggregated data is {len(aggregated_data)} rows long.")
print(f"Last rows of aggregated data:")
print(aggregated_data.tail())

print(f"Plotting aggregated data...")
plt.plot(aggregated_data['time_bucket'], aggregated_data['amplitude'])
plt.xticks(ticks=np.arange(0, aggregated_data['time_bucket'].max(), 10))
plt.xlabel("Time (minutes since 22:37)")
plt.ylabel("Amplitude")
plt.title("Aggregated Audio Data")
plt.show()
