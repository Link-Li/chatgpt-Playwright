# -*- coding: utf-8 -*-
"""
@Time        : 2023/5/14 21:23
@Author      : noahzhenli
@Email       : noahzhenli@tencent.com
@Description : 
"""

import json

from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset, Audio, Dataset
import pydub
from pydub import AudioSegment
pydub.AudioSegment.converter = 'D:\\ffmpeg-master-latest-win64-gpl\\bin/ffmpeg.exe'


env_dict = {}
with open("env", "r", encoding="utf-8") as f_read:
    for data_line in f_read.readlines():
        for key, value in json.loads(data_line.strip("\n")).items():
            env_dict[key] = value

# load model and processor

processor = WhisperProcessor.from_pretrained(env_dict["whisper_model_path"])
model = WhisperForConditionalGeneration.from_pretrained(env_dict["whisper_model_path"])
model.config.forced_decoder_ids = None


def m4a_to_mp3(input_file, output_file):
    audio = AudioSegment.from_file(input_file, format='m4a')
    audio.export(output_file, format='mp3')

# Example usage:
m4a_to_mp3('data/test.m4a', 'data/test_code.mp3')

audio_data = Dataset.from_dict({"audio": ["data/test.mp3"]}).cast_column("audio", Audio(sampling_rate=16000))
print(audio_data[0]["audio"])
input_features = processor(audio_data[0]["audio"]["array"], sampling_rate=audio_data[0]["audio"]["sampling_rate"], return_tensors="pt").input_features
predicted_ids = model.generate(input_features)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)

# load dummy dataset and read audio files
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = ds[0]["audio"]
input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features


# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)

print(transcription)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)
