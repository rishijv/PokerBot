import os
import pyautogui
import time
import pyperclip
import requests  # New import for making API requests
import json      # New import for handling JSON data

# --- Get the OpenRouter API Key ---
try:
    API_KEY = os.environ["OPENROUTER_API_KEY"]
except KeyError:
    print("❌ OPENROUTER_API_KEY not found. Please set the environment variable.")
    exit()

def get_text_via_copy_paste():
    """
    Clicks a button, simulates 'select all' and 'copy', then reads from the clipboard.
    """
    button_x, button_y = 55, 590

    print("Getting game text from hand history...")
    pyautogui.click(button_x, button_y)
    pyautogui.click(button_x, button_y)
    time.sleep(0.5)

    pyautogui.hotkey('command', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('command', 'c')
    time.sleep(0.2)

    game_text = pyperclip.paste()
    return game_text

def get_openrouter_decision_from_text(game_text):
    """
    Sends the copied game text to OpenRouter and asks for a decision.
    """
    prompt = f"""
    You are a No Limit Texas Hold'em bot playing Game Theory Optimal (GTO).
    Analyze the following hand history text. It is your turn to act.

    Hand History:
    ---
    {game_text}
    ---

    Based on the text, what is the GTO move?
    Respond with a single line: "FOLD", "CALL", "CHECK", or "RAISE <amount>".
    Example: RAISE 2.50
    """
    
    print("🤖 Analyzing text with OpenRouter...")
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "nousresearch/nous-hermes-2-mistral-7b-dpo:free", # Using a free model
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })
        )
        response.raise_for_status() # Will raise an error for bad status codes (4xx or 5xx)

        response_json = response.json()
        decision_text = response_json['choices'][0]['message']['content'].strip().upper()
        
        print(f"✅ OpenRouter decided: {decision_text}")
        return decision_text
        
    except requests.exceptions.RequestException as e:
        print(f"❌ An API error occurred: {e}")
        return None

# --- Main Part of the Script ---
if __name__ == "__main__":
    game_text = get_text_via_copy_paste()

    if game_text and len(game_text) > 20:
        print("--- Copied Text ---")
        print(game_text)
        print("--------------------")

        decision = get_openrouter_decision_from_text(game_text)
        
        # execute_action(decision)
    else:
        print("❌ Failed to copy any significant text from the page.")