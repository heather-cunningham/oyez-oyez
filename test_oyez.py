import requests
import time
from pprint import pprint

## For Mistral 7B Instruct LLMs
# url = "http://localhost:8080/v1/completions"
##
##
# headers = {"Content-Type": "application/json"}
##
##
# data = {
#     "model": "mistral-7b-instruct-v0.1.Q2_K.gguf",
#     "prompt": "Explain the concept of gravity in simple terms.",
#     "temperature": 0.7,
#     "max_tokens": 100,
# }


## For Tiny Llama chat LLMs
url = "http://localhost:8080/v1/chat/completions"


headers = {"Content-Type": "application/json"}


## For Tiny Llama chat LLMs
data = {
    "model": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the concept of gravity in simple terms."}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}


# Start the timer
start_time = time.time()  
start_time_str = time.strftime("%H:%M:%S", time.localtime(start_time))
print("#### start_time", start_time_str)


response = requests.post(url, headers=headers, json=data)
json_response = response.json()


# End the timer
end_time = time.time()
end_time_str = time.strftime("%H:%M:%S", time.localtime(end_time))
print("#### end_time", end_time_str)  


# Calculate elapsed time
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"#### Total response time in SECONDS: {elapsed_time:.2f} seconds")
print(f"#### Time Elapsed:  {minutes} mins {seconds} secs")

# Output the LLM's response
print("#### LLM Response:")
pprint(json_response)

