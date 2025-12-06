import streamlit as st
import random
import time

# -------- SLOT SETTINGS -------- #
SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣', '🔔']
REELS = 5
START_BALANCE = 1000
INITIAL_WIN_SPINS = 5        # Player can only get "three of a kind" in first N spins
HOUSE_WIN_PROBABILITY = 0.75 # After N spins, lose probability is 75%

# -------- STATE INITIALIZATION -------- #
def init_session():
    if "balance" not in st.session_state:
        st.session_state.balance = START_BALANCE
    if "total_spins" not in st.session_state:
        st.session_state.total_spins = 0
    if "total_wins" not in st.session_state:
        st.session_state.total_wins = 0
    if "reels" not in st.session_state:
        st.session_state.reels = random.sample(SYMBOLS, REELS)
    if "message" not in st.session_state:
        st.session_state.message = "Place your bet and spin!"
    if "last_win_amount" not in st.session_state:
        st.session_state.last_win_amount = 0

# -------- SLOT ANIMATION & DISPLAY -------- #
def animate_spin(duration=1.2, frame_delay=0.13):
    anim_placeholder = st.empty()
    num_frames = int(duration / frame_delay)
    for frame in range(num_frames):
        cols = anim_placeholder.columns(REELS)
        for i, col in enumerate(cols):
            col.markdown(
                f"""<div style='background:white;border-radius:15px;padding:20px;
                font-size:60px;text-align:center;border:4px solid gold;min-width:70px;min-height:70px;
                display:flex;align-items:center;justify-content:center;'>
                {random.choice(SYMBOLS)}
                </div>""", unsafe_allow_html=True,
            )
        time.sleep(frame_delay)
    anim_placeholder.empty()

def slot_board_display():
    st.markdown(
        "<div style='background:linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);"
        "padding:30px;border-radius:20px;margin:20px 0;display: flex; justify-content: center;'>",
        unsafe_allow_html=True,
    )
    cols = st.columns(REELS)
    for i, col in enumerate(cols):
        col.markdown(
            f"""<div style='background:white;border-radius:15px;padding:20px;
            font-size:60px;text-align:center;border:4px solid gold;min-width:70px;min-height:70px;
            display:flex;align-items:center;justify-content:center;'>
            {st.session_state.reels[i]}
            </div>""", unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# -------- GAME LOGIC -------- #
def generate_winning_reels(allowed_types):
    win_type = random.choice(allowed_types)
    symbol = random.choice(SYMBOLS)
    if win_type == "three":
        others = random.sample([s for s in SYMBOLS if s != symbol], 2)
        reels = [symbol] * 3 + others
        random.shuffle(reels)
        return reels
    elif win_type == "four":
        other = random.choice([s for s in SYMBOLS if s != symbol])
        reels = [symbol] * 4 + [other]
        random.shuffle(reels)
        return reels
    else:  # "five"
        return [symbol] * REELS

def generate_losing_reels():
    for _ in range(100):
        reels = [random.choice(SYMBOLS) for _ in range(REELS)]
        if not check_win(reels)[0]:
            return reels
    # fallback; almost impossible, but covers edge case:
    return random.sample(SYMBOLS, REELS)

def check_win(reels):
    counts = {s: reels.count(s) for s in SYMBOLS}
    max_count = max(counts.values())
    # 5 of a kind
    if max_count == 5:
        symbol = [s for s, n in counts.items() if n == 5][0]
        if symbol == '💎':
            return True, 100, "💎 DIAMOND JACKPOT! 💎"
        if symbol == '7️⃣':
            return True, 50, "7️⃣ LUCKY SEVENS! 7️⃣"
        return True, 30, "🎰 FIVE OF A KIND! 🎰"
    elif max_count == 4:
        return True, 15, "✨ FOUR OF A KIND! ✨"
    elif max_count == 3:
        return True, 5, "🎉 THREE OF A KIND! 🎉"
    return False, 0, ""

def spin_slot(bet_amount):
    st.session_state.balance -= bet_amount
    st.session_state.total_spins += 1

    # Rigged: first N spins can win ONLY "three", after that, any win type.
    if st.session_state.total_spins <= INITIAL_WIN_SPINS:
        should_win = True
        allowed_win_types = ['three']
    else:
        should_win = random.random() > HOUSE_WIN_PROBABILITY
        allowed_win_types = ['three', 'four', 'five']
    
    if should_win:
        reels = generate_winning_reels(allowed_win_types)
    else:
        reels = generate_losing_reels()
    st.session_state.reels = reels

    is_win, multiplier, win_message = check_win(reels)
    if is_win:
        winnings = bet_amount * multiplier
        st.session_state.balance += winnings
        st.session_state.last_win_amount = winnings
        st.session_state.total_wins += 1
        st.session_state.message = f"{win_message} Won ${winnings}!"
    else:
        st.session_state.last_win_amount = 0
        st.session_state.message = "😔 No win this time. Try again!"

# -------- UI: METRICS, MSG, PAYOUT -------- #
def show_metrics():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Balance", f"${st.session_state.balance}")
    col2.metric("🎲 Total Spins", st.session_state.total_spins)
    col3.metric("🏆 Wins", st.session_state.total_wins)
    win_rate = (
        (st.session_state.total_wins / st.session_state.total_spins) * 100
        if st.session_state.total_spins > 0 else 0
    )
    col4.metric("📊 Win Rate", f"{win_rate:.1f}%")
def show_message():
    if st.session_state.last_win_amount > 0:
        st.success(st.session_state.message, icon="🎉")
    else:
        st.info(st.session_state.message)
def payout_table():
    st.markdown("---")
    st.markdown("### 💰 PAYOUT TABLE")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "- **💎💎💎💎💎** → 100x bet\n"
            "- **7️⃣7️⃣7️⃣7️⃣7️⃣** → 50x bet\n"
            "- **Any 5 of a kind** → 30x bet"
        )
    with col2:
        st.markdown(
            "- **Any 4 of a kind** → 15x bet\n"
            "- **Any 3 of a kind** → 5x bet"
        )

# -------- MAIN APP -------- #
def main():
    st.set_page_config(page_title="Slot Machine", page_icon="🎰", layout="centered")
    st.markdown("""
        <style>
        .stButton>button { background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%);
            color: white; font-size: 24px; font-weight: bold; padding: 20px;
            border-radius: 15px; border: none; box-shadow: 0 8px 16px rgba(0,0,0,0.3);}
        .stButton>button:hover {
            background: linear-gradient(90deg, #a8e063 0%, #56ab2f 100%);
            transform: translateY(-2px);}
        </style>
    """, unsafe_allow_html=True)

    init_session()
    st.markdown("<h1 style='text-align:center; color:#ffd700; text-shadow:2px 2px 4px #000000;'>🎰 MEGA SLOT MACHINE 🎰</h1>", unsafe_allow_html=True)
    show_metrics()
    st.markdown("---")
    bet_amount = st.number_input(
        "💵 Enter your bet amount:",
        min_value=10,
        max_value=st.session_state.balance if st.session_state.balance > 0 else 10,
        value=min(50, st.session_state.balance) if st.session_state.balance > 0 else 10,
        step=10
    )
    slot_board_display()
    show_message()

    st.markdown("---")
    col_spin, col_reset = st.columns([3, 1])
    with col_spin:
        if st.button("🎰 SPIN 🎰", disabled=(st.session_state.balance < bet_amount)):
            if st.session_state.balance >= bet_amount:
                animate_spin()
                spin_slot(bet_amount)
                st.rerun()
            else:
                st.error("Insufficient balance!")
    with col_reset:
        if st.button("🔄 RESET"):
            for key in ["balance", "total_spins", "total_wins", "reels", "message", "last_win_amount"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    if st.session_state.balance < bet_amount:
        st.error("⚠️ Insufficient balance! Please reset the game or lower your bet.")

    payout_table()
    st.markdown("---")
    st.caption("⚠️ This is for entertainment purposes only. Always gamble responsibly!")

if __name__ == "__main__":
    main()
