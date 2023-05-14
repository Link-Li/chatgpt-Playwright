# -*- coding: utf-8 -*-
"""
@Time        : 2023/5/14 21:23
@Author      : noahzhenli
@Email       : noahzhenli@tencent.com
@Description : 
"""

from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset

# load model and processor
model_file = "/Users/lizhen/F/code/工具/模型文件/whisper/tiny"
processor = WhisperProcessor.from_pretrained(model_file)
model = WhisperForConditionalGeneration.from_pretrained(model_file)
model.config.forced_decoder_ids = None

# load dummy dataset and read audio files
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = ds[0]["audio"]
input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features

# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
