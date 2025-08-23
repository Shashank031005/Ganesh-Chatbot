import os
import subprocess
import platform
import sounddevice as sd
import soundfile as sf

def speak(text: str, lang: str = "hi"):
    """
    Convert text to speech using Piper TTS and play it.
    
    Args:
        text (str): The text to convert to speech
        lang (str): Language code (currently supports "hi")
    """

    # Folder where piper.exe and voices live
    piper_dir = "piper"
    output_file = "output.wav"

    # Detect piper binary (Windows vs Linux)
    if platform.system() == "Windows":
        piper_binary = os.path.join(piper_dir, "piper.exe")
    else:
        piper_binary = os.path.join(piper_dir, "piper")

    # Voice files directly inside `piper/`
    files = os.listdir(piper_dir)
    model_path = next((os.path.join(piper_dir, f) for f in files if f.endswith(".onnx")), None)
    json_path = next((os.path.join(piper_dir, f) for f in files if f.endswith(".json")), None)

    if not model_path or not json_path:
        raise FileNotFoundError("❌ Model (.onnx) or config (.json) not found in piper/ folder.")

    # Build Piper command
    command = [
        piper_binary,
        "-m", model_path,
        "-c", json_path,
        "-f", output_file
    ]

    print(f"🔊 Running Piper: {command}")

    # Run Piper (send text via stdin)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate(text.encode("utf-8"))
    process.wait()

    # Play generated audio
    if os.path.exists(output_file):
        data, samplerate = sf.read(output_file)
        sd.play(data, samplerate)
        sd.wait()
        print("✅ Done speaking")
    else:
        print("❌ Audio file not generated")


# Example usage
if __name__ == "__main__":
    speak("विघ्नहर्ता गणेश जी आपका मार्ग प्रशस्त करें।", "hi")
