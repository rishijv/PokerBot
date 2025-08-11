import os
import pyautogui
from PIL import Image # Pillow is used to handle the image data
import google.generativeai as genai # Import the new Google library

# --- Configure the Gemini client ---
# It will automatically find the GOOGLE_API_KEY from your environment
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("❌ GOOGLE_API_KEY not found. Please set the environment variable.")
    exit()


def capture_game_image(region):
    """
    Captures a region of the screen and returns it as an Image object.
    """
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

def get_gemini_decision_from_image(image):
    """
    Sends an image of the game state to Gemini Pro Vision and asks for a decision.
    """
    # Use the model that can handle image inputs
    vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = """
    You are a No Limit Texas Hold'em bot playing Game Theory Optimal (GTO). GTO means making mathematically balanced decisions—bet sizes, frequencies, and hand ranges—so opponents cannot exploit you. Mix bluffs and value bets in correct ratios, defend vs. aggression, and adjust only if others deviate from optimal. Be risk-averse; avoid big risks.

    In No Limit Hold'em, raises must be ≥ previous raise. If the frame is highlighted, it’s your turn. Use the pot size (above board cards), your hand, and bets from other players (numbers on table rim) to choose the +EV move.
    Respond with "FOLD", "CALL", "CHECK", or "RAISE". If raising, give an exact amount (e.g., "1.25") Understand that there is a minimum raise in No Limit Hold'em. Always play to maximize expected value.
    """
#Is it my turn to act? Respond with "YES" or "NO".
#   2.
    print("🤖 Analyzing image with Gemini...")
    
    # Generate content from the prompt and the image
    response = vision_model.generate_content([prompt, image])

    decision = response.text.strip().upper()
    print(f"✅ Gemini decided: {decision}")
    return decision


if __name__ == "__main__":
    # Define the area of your screen where the poker game is
    game_area = (5, 120, 980, 450)

    # 1. Capture the game screen
    game_image = capture_game_image(region=game_area)

    if game_image:
        # 2. Get a decision directly from the image using Gemini
        decision = get_gemini_decision_from_image(game_image)
        # 3. Execute the decision
        # Example:
        # if "RAISE" in decision:
        #     pyautogui.write("150") # Types the bet amount
        #     pyautogui.press("enter")
        # elif "CALL" in decision:
        #     ...
