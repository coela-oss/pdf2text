from gpt4all import GPT4All
from openvino import Core

core = Core()
devices = core.available_devices
print("Available devices:", devices)

model_path = "./mnt/models/models--microsoft--Phi-3-mini-4k-instruct-gguf/"
model_file = "./mnt/models/models--microsoft--Phi-3-mini-4k-instruct-gguf/Phi-3-mini-4k-instruct-q4.gguf"
model = GPT4All(
    "Phi-3-mini-4k-instruct-q4.gguf",
    device="gpu",
    model_path=model_path,
    ngl=8,
    n_threads=8,
    n_ctx=4096,
    allow_download=False
)
output = model.generate("こんにちは", max_tokens=1, temp=0)
print(output)
