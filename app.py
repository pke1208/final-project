import streamlit as st
import random
import time

# Page config
st.set_page_config(page_title="Slot Machine", page_icon="🎰", layout="centered")

# Initialize session state
if 'balance' not in st.session_state:
    st.session_state.balance = 1000
if 'total_spins' not in st.session_state:
    st.session_state.total_spins = 0
if 'total_wins' not in st.session_state:
    st.session_state.total_wins = 0
if 'reels' not in st.session_state:
    st.session_state.reels = ['🍒', '🍋', '🍊', '🍇', '⭐']
if 'message' not in st.session_state:
    st.session_state.message = "Place your bet and spin!"
if 'last_win_amount' not in st.session_state:
    st.session_state.last_win_amount = 0

# Symbols for the slot machine
SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣', '🔔']

# Strategic parameters
INITIAL_WIN_SPINS = 5  # First 5 spins have special win rate
INITIAL_WIN_RATE = 0.60  # 60% win rate in first 5 spins (hook them but not too obvious)
HOUSE_ADVANTAGE_START = 6  # After spin 5, house advantage kicks in
HOUSE_WIN_PROBABILITY = 0.75  # 75% lose rate after initial wins

def check_win(reels):
    """Check if reels result in a win and calculate payout multiplier"""
    
    # Count occurrences of each symbol
    symbol_counts = {}
    for symbol in reels:
        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
    max_count = max(symbol_counts.values())
    
    # 5 of a kind - JACKPOT
    if max_count == 5:
        winning_symbol = [s for s, c in symbol_counts.items() if c == 5][0]
        if winning_symbol == '💎':
            return True, 100, "💎 DIAMOND JACKPOT! 💎"
        elif winning_symbol == '7️⃣':
            return True, 50, "7️⃣ LUCKY SEVENS! 7️⃣"
        else:
            return True, 30, "🎰 FIVE OF A KIND! 🎰"
    
    # 4 of a kind
    elif max_count == 4:
        return True, 15, "✨ FOUR OF A KIND! ✨"
    
    # 3 of a kind
    elif max_count == 3:
        return True, 5, "🎉 THREE OF A KIND! 🎉"
    
    # No win
    return False, 0, ""

def generate_winning_reels():
    """Generate reels that will result in a win"""
    win_type = random.choice(['three', 'four', 'five'])
    
    if win_type == 'five':
        # 5 of a kind
        symbol = random.choice(SYMBOLS)
        return [symbol] * 5
    
    elif win_type == 'four':
        # 4 of a kind
        symbol = random.choice(SYMBOLS)
        other = random.choice([s for s in SYMBOLS if s != sy
