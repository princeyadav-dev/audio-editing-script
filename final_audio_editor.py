from pydub import AudioSegment, silence, effects

def full_audio_edit(input_file, output_file, silence_thresh=-40, min_silence_len=500):
    # Step 1: Load audio
    audio = AudioSegment.from_file(input_file, format="mp3")

    # Step 2: Remove silence
    chunks = silence.split_on_silence(audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    audio = AudioSegment.empty()
    for chunk in chunks:
        audio += chunk + AudioSegment.silent(duration=150)  # natural pause

    # Step 3: Normalize
    audio = effects.normalize(audio)

    # Step 4: Speed increase by 2%
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1)
    }).set_frame_rate(audio.frame_rate)

    # Step 5: Noise reduction (fake basic way)
    audio = audio.low_pass_filter(20000).high_pass_filter(100)  # simulate basic noise reduce

    # Step 6: Amplify (optional: here we boost by 5dB)
    audio += 5

    # Step 7: Set sample rate to 16000 Hz
    audio = audio.set_frame_rate(16000)

    # Step 8: Convert to mono
    audio = audio.set_channels(1)

    # Step 9: Final normalize
    audio = effects.normalize(audio)

    # Step 10: Export
    audio.export(output_file, format="mp3")
    print("✅ Final audio saved as:", output_file)

# Example run
input_path = "C:/Users/admin/Desktop/animeaudio/input_audio.mp3"
output_path = "C:/Users/admin/Desktop/animeaudio/final_output.mp3"

full_audio_edit(input_path, output_path)
