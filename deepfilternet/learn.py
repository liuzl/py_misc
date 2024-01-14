from df.enhance import enhance, init_df, load_audio, save_audio
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <input_audio> <output_audio>")
        exit(1)
    # Load default model
    model, df_state, _ = init_df()
    audio, _ = load_audio(sys.argv[1], sr=df_state.sr())
    # Denoise the audio
    enhanced = enhance(model, df_state, audio)
    # Save for listening
    save_audio(sys.argv[2], enhanced, df_state.sr())