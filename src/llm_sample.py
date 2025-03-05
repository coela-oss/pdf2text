from gpt4all import GPT4All
from openvino import Core
import vulkan as vk


def check_vulkan():
    instance_info = vk.VkInstanceCreateInfo()
    instance = vk.vkCreateInstance(instance_info, None)
    physical_devices = vk.vkEnumeratePhysicalDevices(instance)
    print(f"Found {len(physical_devices)} Vulkan devices.")
    for device in physical_devices:
        properties = vk.vkGetPhysicalDeviceProperties(device)
        print(f"Device: {properties.deviceName}")

check_vulkan()

core = Core()
devices = core.available_devices
print("Available devices1:", devices)
#print("Available devices2:", GPT4All.list_gpus())

model_path = "./mnt/models/models--microsoft--Phi-3-mini-4k-instruct-gguf/"
model_file = "./mnt/models/models--microsoft--Phi-3-mini-4k-instruct-gguf/Phi-3-mini-4k-instruct-q4.gguf"
model = GPT4All(
    "Phi-3-mini-4k-instruct-q4.gguf",
    device="kompute",
    model_path=model_path,
    ngl=8,
    n_threads=8,
    n_ctx=4096,
    allow_download=False
)

output = model.generate("こんにちは", max_tokens=1, temp=0)
print(output)
