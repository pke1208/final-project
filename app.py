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
if 'bet_amount' not in st.session_state:
    st.session_state.bet_amount = 50
if 'spinning' not in st.session_state:
    st.session_state.spinning = False

# Symbols for the slot machine
SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣', '🔔']

# Strategic parameters
INITIAL_WIN_SPINS = 10
INITIAL_WIN_RATE = 0.40
HOUSE_ADVANTAGE_START = 11
HOUSE_WIN_PROBABILITY = 0.85

def check_win(reels):
    """Check if reels result in a win and calculate payout multiplier"""
    symbol_counts = {}
    for symbol in reels:
        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
    max_count = max(symbol_counts.values())
    
    # Adjust multipliers based on spin count (lower payouts in first 10 spins)
    is_early_game = st.session_state.total_spins <= INITIAL_WIN_SPINS
    
    if max_count == 5:
        winning_symbol = [s for s, c in symbol_counts.items() if c == 5][0]
        if winning_symbol == '💎':
            multiplier = 20 if is_early_game else 100
            return True, multiplier, "💎 DIAMOND JACKPOT! 💎"
        elif winning_symbol == '7️⃣':
            multiplier = 10 if is_early_game else 50
            return True, multiplier, "7️⃣ LUCKY SEVENS! 7️⃣"
        else:
            multiplier = 8 if is_early_game else 30
            return True, multiplier, "🎰 FIVE OF A KIND! 🎰"
    elif max_count == 4:
        multiplier = 4 if is_early_game else 15
        return True, multiplier, "✨ FOUR OF A KIND! ✨"
    elif max_count == 3:
        multiplier = 2 if is_early_game else 5
        return True, multiplier, "🎉 THREE OF A KIND! 🎉"
    
    return False, 0, ""

def generate_winning_reels():
    """Generate reels that will result in a win"""
    win_type = random.choice(['three', 'four', 'five'])
    
    if win_type == 'five':
        symbol = random.choice(SYMBOLS)
        return [symbol] * 5
    elif win_type == 'four':
        symbol = random.choice(SYMBOLS)
        other = random.choice([s for s in SYMBOLS if s != symbol])
        result = [symbol] * 4 + [other]
        random.shuffle(result)
        return result
    else:
        symbol = random.choice(SYMBOLS)
        others = random.sample([s for s in SYMBOLS if s != symbol], 2)
        result = [symbol] * 3 + others
        random.shuffle(result)
        return result

def generate_losing_reels():
    """Generate reels that will result in a loss"""
    attempts = 0
    while attempts < 100:
        result = [random.choice(SYMBOLS) for _ in range(5)]
        is_win, _, _ = check_win(result)
        if not is_win:
            return result
        attempts += 1
    
    return [SYMBOLS[0], SYMBOLS[1], SYMBOLS[2], SYMBOLS[3], SYMBOLS[4]]

def spin_slot(bet_amount):
    """Main slot machine logic with rigging"""
    st.session_state.balance -= bet_amount
    st.session_state.total_spins += 1
    
    should_win = False
    
    if st.session_state.total_spins <= INITIAL_WIN_SPINS:
        should_win = random.random() < INITIAL_WIN_RATE
    else:
        should_win = random.random() > HOUSE_WIN_PROBABILITY
    
    if should_win:
        new_reels = generate_winning_reels()
    else:
        new_reels = generate_losing_reels()
    
    st.session_state.reels = new_reels
    
    is_win, multiplier, win_message = check_win(new_reels)
    
    if is_win:
        winnings = bet_amount * multiplier
        st.session_state.balance += winnings
        st.session_state.total_wins += 1
        st.session_state.last_win_amount = winnings
        st.session_state.message = f"{win_message} Won ${winnings}!"
        return True
    else:
        st.session_state.last_win_amount = 0
        st.session_state.message = "😔 No win this time. Try again!"
        return False

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%);
        color: white;
        font-size: 24px;
        font-weight: bold;
        padding: 20px;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #a8e063 0%, #56ab2f 100%);
        transform: translateY(-2px);
    }
    .slot-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin: 20px 0;
    }
    .reel {
        background: white;
        border-radius: 15px;
        padding: 20px;
        font-size: 60px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border: 4px solid gold;
        transition: transform 0.1s;
    }
    @keyframes spin {
        0% { transform: translateY(0px); }
        25% { transform: translateY(-10px); }
        50% { transform: translateY(0px); }
        75% { transform: translateY(10px); }
        100% { transform: translateY(0px); }
    }
    .spinning {
        animation: spin 0.15s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #ffd700; text-shadow: 2px 2px 4px #000000;'>🎰 MEGA SLOT MACHINE 🎰</h1>", unsafe_allow_html=True)

# Stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Balance", f"${st.session_state.balance}")
with col2:
    st.metric("🎲 Total Spins", st.session_state.total_spins)
with col3:
    st.metric("🏆 Wins", st.session_state.total_wins)
with col4:
    if st.session_state.total_spins > 0:
        win_rate = (st.session_state.total_wins / st.session_state.total_spins) * 100
        st.metric("📊 Win Rate", f"{win_rate:.1f}%")
    else:
        st.metric("📊 Win Rate", "0%")

# Bet input
st.markdown("---")
bet_amount = st.number_input(
    "💵 Enter your bet amount:",
    min_value=10,
    max_value=st.session_state.balance if st.session_state.balance > 0 else 10,
    value=st.session_state.bet_amount,
    step=10,
    key='bet_input'
)

# Update bet amount in session state
st.session_state.bet_amount = bet_amount

# Slot machine display
st.markdown("<div class='slot-container'>", unsafe_allow_html=True)

cols = st.columns(5)
spin_class = "spinning" if st.session_state.spinning else ""
for i, col in enumerate(cols):
    with col:
        st.markdown(f"<div class='reel {spin_class}'>{st.session_state.reels[i]}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Message display
if st.session_state.last_win_amount > 0:
    st.success(st.session_state.message, icon="🎉")
else:
    st.info(st.session_state.message)

# Spin button
st.markdown("---")
col_spin, col_reset = st.columns([3, 1])

with col_spin:
    if st.button("🎰 SPIN 🎰", disabled=(st.session_state.balance < bet_amount)):
        if st.session_state.balance >= bet_amount:
            st.session_state.spinning = True
            placeholder = st.empty()
            
            # Spinning animation with multiple cycles
            for cycle in range(10):
                temp_reels = [random.choice(SYMBOLS) for _ in range(5)]
                with placeholder.container():
                    st.markdown("<div class='slot-container'>", unsafe_allow_html=True)
                    cols = st.columns(5)
                    for i, col in enumerate(cols):
                        with col:
                            st.markdown(f"<div class='reel spinning'>{temp_reels[i]}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            # Final result
            st.session_state.spinning = False
            spin_slot(bet_amount)
            placeholder.empty()
            st.rerun()
        else:
            st.error("Insufficient balance!")

with col_reset:
    if st.button("🔄 RESET"):
        st.session_state.balance = 1000
        st.session_state.total_spins = 0
        st.session_state.total_wins = 0
        st.session_state.reels = ['🍒', '🍋', '🍊', '🍇', '⭐']
        st.session_state.message = "Place your bet and spin!"
        st.session_state.last_win_amount = 0
        st.session_state.bet_amount = 50
        st.session_state.spinning = False
        st.rerun()

# Warning message if balance is low
if st.session_state.balance < bet_amount:
    st.error("⚠️ Insufficient balance! Please reset the game or lower your bet.")

# Payout table
st.markdown("---")
st.markdown("### 💰 PAYOUT TABLE")

# Show different payouts based on game stage
if st.session_state.total_spins <= INITIAL_WIN_SPINS:
    st.info("🎮 Early Game Payouts (First 10 Spins)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **💎💎💎💎💎** → 20x bet
        - **7️⃣7️⃣7️⃣7️⃣7️⃣** → 10x bet
        - **Any 5 of a kind** → 8x bet
        """)
    with col2:
        st.markdown("""
        - **Any 4 of a kind** → 4x bet
        - **Any 3 of a kind** → 2x bet
        """)
else:
    st.success("🔥 Full Payouts (After 10 Spins)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **💎💎💎💎💎** → 100x bet
        - **7️⃣7️⃣7️⃣7️⃣7️⃣** → 50x bet
        - **Any 5 of a kind** → 30x bet
        """)
    with col2:
        st.markdown("""
        - **Any 4 of a kind** → 15x bet
        - **Any 3 of a kind** → 5x bet
        """)

st.markdown("---")
st.caption("⚠️ This is for entertainment purposes only. Always gamble responsibly!")
