import os
import re
import torch
import threading
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

# Disable Hugging Face progress bar
os.environ["TRANSFORMERS_NO_PROGRESS_BAR"] = "1"

# Load model
print("⏳ Loading model and tokenizer from Hugging Face...", end="", flush=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print("\r✅ Model and tokenizer loaded successfully.        ")

# Spinner animation
class Spinner:
    def __init__(self, message="⏳ Generating code"):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin)
        self.message = message

    def _spin(self):
        symbols = ['|', '/', '-', '\\']
        i = 0
        while not self._stop_event.is_set():
            print(f"\r{self.message}... {symbols[i % len(symbols)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
        print("\r✅ Code generated successfully.           ")

# 💡 Very strict code-only prompt
PROMPT = (
    "Write only valid Python code for the task below. "
    "Return ONLY the code — no explanations, comments, docstrings, markdown, or outputs. "
    "Do not include any formatting like ```python. Do not add print statements or examples. "
    "Respond with a single self-contained Python function or line that solves the task.\n\n"
    "Task: {}"
)

def extract_code(output: str) -> str:
    # Remove triple-quoted docstrings ("""...""" or '''...''')
    output = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', output, flags=re.DOTALL)

    # Match the first Python code block starting with def, class, or import
    match = re.search(r"(def\s+[^\n]+\n(?:\s+.+\n?)*)", output)
    if match:
        return match.group(0).strip()
    return output.strip()

def generate(task: str, max_tokens: int = 256, temperature: float = 0.2) -> str:
    prompt = PROMPT.format(task.strip())
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    spinner = Spinner()
    spinner.start()

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )

    spinner.stop()

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return extract_code(result)
