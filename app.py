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

# # Symbols for the slot machine
# SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣', '🔔']

# # Strategic parameters
# INITIAL_WIN_SPINS = 5  # Let player win in first 5 spins to hook them
# HOUSE_ADVANTAGE_START = 6  # After spin 5, house advantage kicks in
# HOUSE_WIN_PROBABILITY = 0.75  # 75% lose rate after initial wins

# def check_win(reels):
#     """Check if reels result in a win and calculate payout multiplier"""
    
#     # Count occurrences of each symbol
#     symbol_counts = {}
#     for symbol in reels:
#         symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
#     max_count = max(symbol_counts.values())
    
#     # 5 of a kind - JACKPOT
#     if max_count == 5:
#         winning_symbol = [s for s, c in symbol_counts.items() if c == 5][0]
#         if winning_symbol == '💎':
#             return True, 100, "💎 DIAMOND JACKPOT! 💎"
#         elif winning_symbol == '7️⃣':
#             return True, 50, "7️⃣ LUCKY SEVENS! 7️⃣"
#         else:
#             return True, 30, "🎰 FIVE OF A KIND! 🎰"
    
#     # 4 of a kind
#     elif max_count == 4:
#         return True, 15, "✨ FOUR OF A KIND! ✨"
    
#     # 3 of a kind
#     elif max_count == 3:
#         return True, 5, "🎉 THREE OF A KIND! 🎉"
    
#     # No win
#     return False, 0, ""

# def generate_winning_reels():
#     """Generate reels that will result in a win"""
#     win_type = random.choice(['three', 'four', 'five'])
    
#     if win_type == 'five':
#         # 5 of a kind
#         symbol = random.choice(SYMBOLS)
#         return [symbol] * 5
    
#     elif win_type == 'four':
#         # 4 of a kind
#         symbol = random.choice(SYMBOLS)
#         other = random.choice([s for s in SYMBOLS if s != symbol])
#         result = [symbol] * 4 + [other]
#         random.shuffle(result)
#         return result
    
#     else:
#         # 3 of a kind
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
    
#     # Fallback: force a losing combination
#     return [SYMBOLS[0], SYMBOLS[1], SYMBOLS[2], SYMBOLS[3], SYMBOLS[4]]

# def spin_slot(bet_amount):
#     """Main slot machine logic with rigging"""
    
#     # Deduct bet
#     st.session_state.balance -= bet_amount
#     st.session_state.total_spins += 1
    
#     # Strategic rigging logic
#     should_win = False
    
#     if st.session_state.total_spins <= INITIAL_WIN_SPINS:
#         # Let them win in first few spins to hook them
#         should_win = True
#     else:
#         # After initial wins, house advantage kicks in
#         should_win = random.random() > HOUSE_WIN_PROBABILITY
    
#     # Generate reels based on strategy
#     if should_win:
#         new_reels = generate_winning_reels()
#     else:
#         new_reels = generate_losing_reels()
    
#     st.session_state.reels = new_reels
    
#     # Check result
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
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Title
# st.markdown("<h1 style='text-align: center; color: #ffd700; text-shadow: 2px 2px 4px #000000;'>🎰 MEGA SLOT MACHINE 🎰</h1>", unsafe_allow_html=True)

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
#     value=min(50, st.session_state.balance) if st.session_state.balance > 0 else 10,
#     step=10
# )

# # Slot machine display
# st.markdown("<div class='slot-container'>", unsafe_allow_html=True)

# cols = st.columns(5)
# for i, col in enumerate(cols):
#     with col:
#         st.markdown(f"<div class='reel'>{st.session_state.reels[i]}</div>", unsafe_allow_html=True)

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
#             # Show spinning animation
#             placeholder = st.empty()
#             for _ in range(3):
#                 temp_reels = [random.choice(SYMBOLS) for _ in range(5)]
#                 with placeholder.container():
#                     cols = st.columns(5)
#                     for i, col in enumerate(cols):
#                         with col:
#                             st.markdown(f"<div class='reel'>{temp_reels[i]}</div>", unsafe_allow_html=True)
#                 time.sleep(0.2)
            
#             # Final result
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
#         st.rerun()

# # Warning message if balance is low
# if st.session_state.balance < bet_amount:
#     st.error("⚠️ Insufficient balance! Please reset the game or lower your bet.")

# # Payout table
# st.markdown("---")
# st.markdown("### 💰 PAYOUT TABLE")
# col1, col2 = st.columns(2)
# with col1:
#     st.markdown("""
#     - **💎💎💎💎💎** → 100x bet
#     - **7️⃣7️⃣7️⃣7️⃣7️⃣** → 50x bet
#     - **Any 5 of a kind** → 30x bet
#     """)
# with col2:
#     st.markdown("""
#     - **Any 4 of a kind** → 15x bet
#     - **Any 3 of a kind** → 5x bet
#     """)

# st.markdown("---")
# st.caption("⚠️ This is for entertainment purposes only. Always gamble responsibly!")

import streamlit as st
import random

# Constants
REELS = 5
SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎"]  # Example slot symbols

# Session state
if "balance" not in st.session_state:
    st.session_state.balance = 1000  # Starting balance
if "round" not in st.session_state:
    st.session_state.round = 0

st.title("🎰 Slot Machine Game")

# Input bet
bet = st.number_input("Enter your bet amount:", min_value=1, max_value=st.session_state.balance, value=10)

spin = st.button("Spin!")

def spin_reels(forced_win=False):
    if forced_win:
        # Guarantee at least a 3-reel match for a win
        match_symbol = random.choice(SYMBOLS)
        reels = [match_symbol] * 3 + random.choices(SYMBOLS, k=REELS - 3)
        random.shuffle(reels)
    else:
        # Random, normal spin
        reels = random.choices(SYMBOLS, k=REELS)
    return reels

def calculate_win(reels, bet):
    # Count longest streak of same symbol
    max_count = max(reels.count(s) for s in SYMBOLS)
    if max_count >= 3:
        # Win: payout scales with streak and bet
        payout = bet * max_count
        return payout, True
    return 0, False

if spin:
    st.session_state.round += 1
    forced_win = False

    # Win the first 2 rounds
    if st.session_state.round in [1, 2]:  
        forced_win = True
    # After that, player wins with lower probability (25%)
    elif st.session_state.round > 2 and random.random() < 0.25:
        forced_win = True

    reels = spin_reels(forced_win=forced_win)
    payout, win = calculate_win(reels, bet)
    
    st.write(' | '.join(reels))
    if win:
        st.success(f"You won! 🎉 Payout: {payout}")
        st.session_state.balance += payout
    else:
        st.warning(f"You lost! Lost bet: {bet}")
        st.session_state.balance -= bet
    
    st.write(f"Balance: {st.session_state.balance}")

    if st.session_state.balance <= 0:
        st.error("Game Over! You're out of balance. Please reload the page.")
else:
    st.write(f"Balance: {st.session_state.balance}")

st.markdown("Made with Streamlit. [View on GitHub](https://github.com)")  # Replace with your repo URL
