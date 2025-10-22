#!/usr/bin/env python3
"""
Chief AI Officer University Audio Generator
Generates high-quality audio for all 16 modules

Options:
1. Google TTS (gTTS) - Free, basic quality
2. ElevenLabs - Premium AI voices ($$$)
3. OpenAI TTS - High quality ($$)
"""

import os
import sys

def generate_with_gtts(script_file, output_file):
    """Generate audio using free Google TTS"""
    try:
        from gtts import gTTS
    except ImportError:
        print("Installing gTTS...")
        os.system("pip3 install gtts")
        from gtts import gTTS

    print(f"Reading script: {script_file}")
    with open(script_file, 'r') as f:
        text = f.read()

    print(f"Generating audio with gTTS...")
    tts = gTTS(text=text, lang='en', slow=False)

    print(f"Saving to: {output_file}")
    tts.save(output_file)

    print(f"✅ Generated {output_file}")
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"   File size: {file_size:.2f} MB")

    return output_file

def generate_with_elevenlabs(script_file, output_file, voice_id="ErXwobaYiN019PkySvjV"):
    """Generate audio using ElevenLabs (requires API key)"""
    try:
        from elevenlabs import generate, save, set_api_key
    except ImportError:
        print("Installing ElevenLabs...")
        os.system("pip3 install elevenlabs")
        from elevenlabs import generate, save, set_api_key

    # Get API key from environment or prompt
    api_key = os.getenv('ELEVEN_API_KEY')
    if not api_key:
        print("⚠️  ElevenLabs API key not found")
        print("Get your key at: https://elevenlabs.io/")
        api_key = input("Enter API key (or press Enter to skip): ").strip()
        if not api_key:
            print("Skipping ElevenLabs generation")
            return None

    set_api_key(api_key)

    print(f"Reading script: {script_file}")
    with open(script_file, 'r') as f:
        text = f.read()

    print(f"Generating audio with ElevenLabs (voice: {voice_id})...")
    audio = generate(
        text=text,
        voice=voice_id,  # Antoni voice (professional male)
        model="eleven_monolingual_v1"
    )

    print(f"Saving to: {output_file}")
    save(audio, output_file)

    print(f"✅ Generated {output_file} with ElevenLabs")
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"   File size: {file_size:.2f} MB")

    return output_file

def generate_with_openai(script_file, output_file, voice="onyx"):
    """Generate audio using OpenAI TTS (requires API key)"""
    try:
        from openai import OpenAI
    except ImportError:
        print("Installing OpenAI...")
        os.system("pip3 install openai")
        from openai import OpenAI

    # Get API key from environment or prompt
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OpenAI API key not found")
        print("Get your key at: https://platform.openai.com/api-keys")
        api_key = input("Enter API key (or press Enter to skip): ").strip()
        if not api_key:
            print("Skipping OpenAI generation")
            return None

    client = OpenAI(api_key=api_key)

    print(f"Reading script: {script_file}")
    with open(script_file, 'r') as f:
        text = f.read()

    # OpenAI has 4096 character limit per request
    # Need to chunk for long content
    max_chars = 4000
    chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

    print(f"Generating audio with OpenAI TTS ({len(chunks)} chunks, voice: {voice})...")

    audio_segments = []
    for i, chunk in enumerate(chunks):
        print(f"  Processing chunk {i+1}/{len(chunks)}...")
        response = client.audio.speech.create(
            model="tts-1-hd",  # HD quality
            voice=voice,  # onyx, alloy, echo, fable, nova, shimmer
            input=chunk,
            speed=1.0
        )
        audio_segments.append(response.content)

    # Combine all chunks
    print(f"Combining {len(audio_segments)} audio segments...")
    with open(output_file, 'wb') as f:
        for segment in audio_segments:
            f.write(segment)

    print(f"✅ Generated {output_file} with OpenAI TTS")
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"   File size: {file_size:.2f} MB")

    return output_file

def main():
    print("=" * 60)
    print("CAIO UNIVERSITY AUDIO GENERATOR")
    print("=" * 60)
    print()

    # Check if audio directory exists
    if not os.path.exists('audio'):
        print("Creating audio directory...")
        os.makedirs('audio')

    script_file = 'module-01-script.txt'

    if not os.path.exists(script_file):
        print(f"❌ Script file not found: {script_file}")
        print("   Make sure you're in the CircuitOS-DEPLOY-PACKAGE directory")
        sys.exit(1)

    print("Choose audio generation method:")
    print()
    print("1. Google TTS (gTTS)  - FREE, basic quality, robotic voice")
    print("2. OpenAI TTS         - $$$, high quality, natural voices")
    print("3. ElevenLabs         - $$$$, premium quality, most realistic")
    print()

    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"

    output_file = 'audio/module-01.mp3'

    if choice == "1":
        generate_with_gtts(script_file, output_file)
    elif choice == "2":
        result = generate_with_openai(script_file, output_file)
        if not result:
            print("\nFalling back to gTTS...")
            generate_with_gtts(script_file, output_file)
    elif choice == "3":
        result = generate_with_elevenlabs(script_file, output_file)
        if not result:
            print("\nFalling back to gTTS...")
            generate_with_gtts(script_file, output_file)
    else:
        print("Invalid choice, using gTTS")
        generate_with_gtts(script_file, output_file)

    print()
    print("=" * 60)
    print("✅ AUDIO GENERATION COMPLETE!")
    print("=" * 60)
    print()
    print(f"Audio file: {output_file}")
    print()
    print("Next steps:")
    print("1. Listen to the audio and verify quality")
    print("2. If satisfied, generate remaining 15 modules")
    print("3. Update audio platform HTML with working playback code")
    print()
    print("To play the audio:")
    print(f"  open {output_file}")
    print()

if __name__ == "__main__":
    main()
