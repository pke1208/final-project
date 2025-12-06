# import streamlit as st
# import random
# import time

# # Page config
# st.set_page_config(page_title="Slot Machine", page_icon="🎰", layout="centered")

# # Initialize session state
# if 'balance' not in st.session_state:
#     st.session_state.balance = 1000
# if 'total_spins' not in st.session_state:
#     st.session_state.total_spins = 0
# if 'total_wins' not in st.session_state:
#     st.session_state.total_wins = 0
# if 'reels' not in st.session_state:
#     st.session_state.reels = ['🍒', '🍋', '🍊', '🍇', '⭐']
# if 'message' not in st.session_state:
#     st.session_state.message = "Place your bet and spin!"
# if 'last_win_amount' not in st.session_state:
#     st.session_state.last_win_amount = 0
# if 'bet_amount' not in st.session_state:
#     st.session_state.bet_amount = 50
# if 'spinning' not in st.session_state:
#     st.session_state.spinning = False

# # Symbols for the slot machine
# SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣', '🔔']

# # Strategic parameters
# INITIAL_WIN_SPINS = 5
# INITIAL_WIN_RATE = 0.40
# HOUSE_ADVANTAGE_START = 6
# HOUSE_WIN_PROBABILITY = 0.85

# def check_win(reels):
#     """Check if reels result in a win and calculate payout multiplier"""
#     symbol_counts = {}
#     for symbol in reels:
#         symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
#     max_count = max(symbol_counts.values())
    
#     # Adjust multipliers based on spin count (lower payouts in first 5 spins)
#     is_early_game = st.session_state.total_spins <= INITIAL_WIN_SPINS
    
#     if max_count == 5:
#         winning_symbol = [s for s, c in symbol_counts.items() if c == 5][0]
#         if winning_symbol == '💎':
#             multiplier = 20 if is_early_game else 100
#             return True, multiplier, "💎 DIAMOND JACKPOT! 💎"
#         elif winning_symbol == '7️⃣':
#             multiplier = 10 if is_early_game else 50
#             return True, multiplier, "7️⃣ LUCKY SEVENS! 7️⃣"
#         else:
#             multiplier = 8 if is_early_game else 30
#             return True, multiplier, "🎰 FIVE OF A KIND! 🎰"
#     elif max_count == 4:
#         multiplier = 4 if is_early_game else 15
#         return True, multiplier, "✨ FOUR OF A KIND! ✨"
#     elif max_count == 3:
#         multiplier = 2 if is_early_game else 5
#         return True, multiplier, "🎉 THREE OF A KIND! 🎉"
    
#     return False, 0, ""

# def generate_winning_reels():
#     """Generate reels that will result in a win"""
#     win_type = random.choice(['three', 'four', 'five'])
    
#     if win_type == 'five':
#         symbol = random.choice(SYMBOLS)
#         return [symbol] * 5
#     elif win_type == 'four':
#         symbol = random.choice(SYMBOLS)
#         other = random.choice([s for s in SYMBOLS if s != symbol])
#         result = [symbol] * 4 + [other]
#         random.shuffle(result)
#         return result
#     else:
#         symbol = random.choice(SYMBOLS)
#         others = random.sample([s for s in SYMBOLS if s != symbol], 2)
#         result = [symbol] * 3 + others
#         random.shuffle(result)
#         return result

# def generate_losing_reels():
#     """Generate reels that will result in a loss"""
#     attempts = 0
#     while attempts < 100:
#         result = [random.choice(SYMBOLS) for _ in range(5)]
#         is_win, _, _ = check_win(result)
#         if not is_win:
#             return result
#         attempts += 1
    
#     return [SYMBOLS[0], SYMBOLS[1], SYMBOLS[2], SYMBOLS[3], SYMBOLS[4]]

# def spin_slot(bet_amount):
#     """Main slot machine logic with rigging"""
#     st.session_state.balance -= bet_amount
#     st.session_state.total_spins += 1
    
#     should_win = False
    
#     if st.session_state.total_spins <= INITIAL_WIN_SPINS:
#         should_win = random.random() < INITIAL_WIN_RATE
#     else:
#         should_win = random.random() > HOUSE_WIN_PROBABILITY
    
#     if should_win:
#         new_reels = generate_winning_reels()
#     else:
#         new_reels = generate_losing_reels()
    
#     st.session_state.reels = new_reels
    
#     is_win, multiplier, win_message = check_win(new_reels)
    
#     if is_win:
#         winnings = bet_amount * multiplier
#         st.session_state.balance += winnings
#         st.session_state.total_wins += 1
#         st.session_state.last_win_amount = winnings
#         st.session_state.message = f"{win_message} Won ${winnings}!"
#         return True
#     else:
#         st.session_state.last_win_amount = 0
#         st.session_state.message = "😔 No win this time. Try again!"
#         return False

# # Custom CSS
# st.markdown("""
#     <style>
#     .main {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     }
#     .stButton>button {
#         width: 100%;
#         background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%);
#         color: white;
#         font-size: 24px;
#         font-weight: bold;
#         padding: 20px;
#         border-radius: 15px;
#         border: none;
#         box-shadow: 0 8px 16px rgba(0,0,0,0.3);
#     }
#     .stButton>button:hover {
#         background: linear-gradient(90deg, #a8e063 0%, #56ab2f 100%);
#         transform: translateY(-2px);
#     }
#     .slot-container {
#         background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#         padding: 30px;
#         border-radius: 20px;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.5);
#         margin: 20px 0;
#     }
#     .reel {
#         background: white;
#         border-radius: 15px;
#         padding: 20px;
#         font-size: 60px;
#         text-align: center;
#         box-shadow: 0 5px 15px rgba(0,0,0,0.3);
#         border: 4px solid gold;
#         transition: transform 0.1s;
#     }
#     @keyframes spin {
#         0% { transform: translateY(0px); }
#         25% { transform: translateY(-10px); }
#         50% { transform: translateY(0px); }
#         75% { transform: translateY(10px); }
#         100% { transform: translateY(0px); }
#     }
#     .spinning {
#         animation: spin 0.15s infinite;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Title
# st.markdown("<h1 style='text-align: center; color: #ffd700; text-shadow: 2px 2px 4px #000000;'>🎰 MEGA SLOT MACHINE 🎰</h1>", unsafe_allow_html=True)

# # Rule Book Section
# with st.expander("📖 RULE BOOK - Click to Read", expanded=False):
#     st.markdown("""
#     ### 🎯 How to Play
#     1. **Set Your Bet**: Enter your desired bet amount (minimum $10)
#     2. **Spin the Reels**: Click the SPIN button to start
#     3. **Match Symbols**: Get 3, 4, or 5 matching symbols to win!
    
#     ### 💰 Payout Structure
    
#     #### Early Game (First 5 Spins)
#     - **Three of a Kind**: 2x your bet
#     - **Four of a Kind**: 4x your bet
#     - **Five of a Kind**: 8x your bet
#     - **Lucky Sevens (7️⃣7️⃣7️⃣7️⃣7️⃣)**: 10x your bet
#     - **Diamond Jackpot (💎💎💎💎💎)**: 20x your bet
    
#     #### Full Game (After 5 Spins)
#     - **Three of a Kind**: 5x your bet
#     - **Four of a Kind**: 15x your bet
#     - **Five of a Kind**: 30x your bet
#     - **Lucky Sevens (7️⃣7️⃣7️⃣7️⃣7️⃣)**: 50x your bet
#     - **Diamond Jackpot (💎💎💎💎💎)**: 100x your bet
    
#     ### 🎲 Game Mechanics
#     - Starting balance: **$1,000**
#     - Minimum bet: **$10**
#     - Win rate adjusts based on number of spins
#     - Your bet amount is saved between spins
#     - Use the RESET button to restart with $1,000
    
#     ### 🎰 Symbols
#     🍒 Cherry | 🍋 Lemon | 🍊 Orange | 🍇 Grape | ⭐ Star | 💎 Diamond | 7️⃣ Seven | 🔔 Bell
    
#     ### ⚠️ Important
#     - This is for entertainment purposes only
#     - Always gamble responsibly
#     - Set limits and stick to them
#     """)

# st.markdown("---")

# # Stats row
# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     st.metric("💰 Balance", f"${st.session_state.balance}")
# with col2:
#     st.metric("🎲 Total Spins", st.session_state.total_spins)
# with col3:
#     st.metric("🏆 Wins", st.session_state.total_wins)
# with col4:
#     if st.session_state.total_spins > 0:
#         win_rate = (st.session_state.total_wins / st.session_state.total_spins) * 100
#         st.metric("📊 Win Rate", f"{win_rate:.1f}%")
#     else:
#         st.metric("📊 Win Rate", "0%")

# # Bet input
# st.markdown("---")
# bet_amount = st.number_input(
#     "💵 Enter your bet amount:",
#     min_value=10,
#     max_value=st.session_state.balance if st.session_state.balance > 0 else 10,
#     value=st.session_state.bet_amount,
#     step=10,
#     key='bet_input'
# )

# # Update bet amount in session state
# st.session_state.bet_amount = bet_amount

# # Slot machine display
# st.markdown("<div class='slot-container'>", unsafe_allow_html=True)

# cols = st.columns(5)
# spin_class = "spinning" if st.session_state.spinning else ""
# for i, col in enumerate(cols):
#     with col:
#         st.markdown(f"<div class='reel {spin_class}'>{st.session_state.reels[i]}</div>", unsafe_allow_html=True)

# st.markdown("</div>", unsafe_allow_html=True)

# # Message display
# if st.session_state.last_win_amount > 0:
#     st.success(st.session_state.message, icon="🎉")
# else:
#     st.info(st.session_state.message)

# # Spin button
# st.markdown("---")
# col_spin, col_reset = st.columns([3, 1])

# with col_spin:
#     if st.button("🎰 SPIN 🎰", disabled=(st.session_state.balance < bet_amount)):
#         if st.session_state.balance >= bet_amount:
#             st.session_state.spinning = True
#             placeholder = st.empty()
            
#             # Spinning animation with multiple cycles
#             for cycle in range(10):
#                 temp_reels = [random.choice(SYMBOLS) for _ in range(5)]
#                 with placeholder.container():
#                     st.markdown("<div class='slot-container'>", unsafe_allow_html=True)
#                     cols = st.columns(5)
#                     for i, col in enumerate(cols):
#                         with col:
#                             st.markdown(f"<div class='reel spinning'>{temp_reels[i]}</div>", unsafe_allow_html=True)
#                     st.markdown("</div>", unsafe_allow_html=True)
#                 time.sleep(0.1)
            
#             # Final result
#             st.session_state.spinning = False
#             spin_slot(bet_amount)
#             placeholder.empty()
#             st.rerun()
#         else:
#             st.error("Insufficient balance!")

# with col_reset:
#     if st.button("🔄 RESET"):
#         st.session_state.balance = 1000
#         st.session_state.total_spins = 0
#         st.session_state.total_wins = 0
#         st.session_state.reels = ['🍒', '🍋', '🍊', '🍇', '⭐']
#         st.session_state.message = "Place your bet and spin!"
#         st.session_state.last_win_amount = 0
#         st.session_state.bet_amount = 50
#         st.session_state.spinning = False
#         st.rerun()

# # Warning message if balance is low
# if st.session_state.balance < bet_amount:
#     st.error("⚠️ Insufficient balance! Please reset the game or lower your bet.")

# # Payout table
# st.markdown("---")
# st.markdown("### 💰 PAYOUT TABLE")

# # Show different payouts based on game stage
# if st.session_state.total_spins <= INITIAL_WIN_SPINS:
#     st.info("🎮 Early Game Payouts (First 5 Spins)")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("""
#         - **💎💎💎💎💎** → 20x bet
#         - **7️⃣7️⃣7️⃣7️⃣7️⃣** → 10x bet
#         - **Any 5 of a kind** → 8x bet
#         """)
#     with col2:
#         st.markdown("""
#         - **Any 4 of a kind** → 4x bet
#         - **Any 3 of a kind** → 2x bet
#         """)
# else:
#     st.success("🔥 Full Payouts (After 5 Spins)")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("""
#         - **💎💎💎💎💎** → 100x bet
#         - **7️⃣7️⃣7️⃣7️⃣7️⃣** → 50x bet
#         - **Any 5 of a kind** → 30x bet
#         """)
#     with col2:
#         st.markdown("""
#         - **Any 4 of a kind** → 15x bet
#         - **Any 3 of a kind** → 5x bet
#         """)

# st.markdown("---")
# st.caption("⚠️ This is for entertainment purposes only. Always gamble responsibly!")

import streamlit as st
import random
import os

# Fallback word list
DEFAULT_WORDS = [
    "apple", "baker", "couch", "drink", "eagle", "flame", "giant", "habit", "ideal", "joker",
    "knife", "lemon", "magic", "night", "ocean", "piano", "queen", "robot", "shark", "tease",
    "union", "vivid", "whale", "xenon", "yacht", "zebra"
]

@st.cache_data
def load_word_list(filepath="words.txt"):
    if os.path.exists(filepath):
        with open(filepath) as f:
            words = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]
        if words:
            return words
    # fallback
    return DEFAULT_WORDS

def get_target_word(words):
    if "target_word" not in st.session_state:
        st.session_state.target_word = random.choice(words)
    return st.session_state.target_word

def check_guess(guess, target):
    feedback = ["gray"] * 5
    guess_used = [False] * 5
    target_used = [False] * 5
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = "green"
            guess_used[i] = True
            target_used[i] = True
    for i in range(5):
        if feedback[i] == "green":
            continue
        for j in range(5):
            if guess[i] == target[j] and not target_used[j] and not guess_used[i]:
                feedback[i] = "yellow"
                target_used[j] = True
                guess_used[i] = True
                break
    return feedback

def update_keyboard(guess, feedback):
    for i, letter in enumerate(guess):
        prev_color = st.session_state.keyboard.get(letter, None)
        color = feedback[i]
        if prev_color == "green":
            continue
        if prev_color == "yellow" and color == "gray":
            continue
        st.session_state.keyboard[letter] = color

COLOR_MAP = {
    "green": "#6aaa64",
    "yellow": "#c9b458",
    "gray": "#787c7e",
    "default": "#d3d6da"
}

def render_guesses():
    for guess, feedback in st.session_state.guesses:
        cols = st.columns(5)
        for i, letter in enumerate(guess):
            cols[i].markdown(
                f"<div style='background-color:{COLOR_MAP[feedback[i]]};border-radius:8px;text-align:center;padding:0.5em 0;font-size:1.5em;color:white;font-weight:bold;'>{letter.upper()}</div>",
                unsafe_allow_html=True
            )
    for _ in range(6 - len(st.session_state.guesses)):
        cols = st.columns(5)
        for i in range(5):
            cols[i].markdown(
                f"<div style='background-color:{COLOR_MAP['default']};border-radius:8px;text-align:center;padding:0.5em 0;font-size:1.5em;color:white;font-weight:bold;'>&nbsp;</div>",
                unsafe_allow_html=True
            )

def render_keyboard():
    layout = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row in layout:
        row_cols = st.columns(len(row))
        for i, letter in enumerate(row):
            color = COLOR_MAP[st.session_state.keyboard.get(letter, "default")]
            row_cols[i].markdown(
                f"<div style='background-color:{color};border-radius:5px;text-align:center;padding:0.7em 0;font-size:1.2em;color:white;font-weight:bold;margin:1px'>{letter.upper()}</div>",
                unsafe_allow_html=True
            )

def show_stats():
    wins = st.session_state.stats.get("wins", 0)
    losses = st.session_state.stats.get("losses", 0)
    st.markdown(f"**Games Won:** {wins} &nbsp;&nbsp;&nbsp; **Games Lost:** {losses}")

# --- Session state init ---
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "keyboard" not in st.session_state:
    st.session_state.keyboard = {}
if "stats" not in st.session_state:
    st.session_state.stats = {"wins": 0, "losses": 0}

words = load_word_list()

target_word = get_target_word(words)

st.title(":blue[Wordle] - Streamlit Edition")
show_stats()
st.divider()

render_guesses()
st.write("")
render_keyboard()
st.write("")

if not st.session_state.game_over:
    with st.form("guess_form"):
        guess_input = st.text_input(
            "Enter your guess:", max_chars=5, help="Type a 5-letter word", label_visibility="collapsed"
        )
        submitted = st.form_submit_button("Submit Guess")
        message = ""

        if submitted:
            guess = guess_input.strip().lower()
            if len(guess) != 5 or not guess.isalpha():
                message = "🚫 Enter a 5-letter word."
            elif guess not in words:
                message = "🚫 Not in word list."
            else:
                feedback = check_guess(guess, target_word)
                st.session_state.guesses.append((guess, feedback))
                update_keyboard(guess, feedback)

                if guess == target_word:
                    st.success(f"🎉 You guessed it! The word was **{target_word.upper()}**")
                    st.session_state.game_over = True
                    st.session_state.stats["wins"] += 1
                elif len(st.session_state.guesses) == 6:
                    st.error(f"😢 Game Over! The word was **{target_word.upper()}**")
                    st.session_state.game_over = True
                    st.session_state.stats["losses"] += 1
            if message:
                st.warning(message)

if st.session_state.game_over:
    st.divider()
    if st.button("Play Again"):
        st.session_state.guesses = []
        st.session_state.target_word = random.choice(words)
        st.session_state.keyboard = {}
        st.session_state.game_over = False
        st.experimental_rerun()
