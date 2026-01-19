import streamlit as st
import random
import time

st.set_page_config(page_title="Guess the Number", page_icon="🎯", layout="centered")

st.title("🎯 Guess The Number – Car Race Edition 🚗")
st.markdown("---")

# ------------------ Difficulty Selection ------------------
level = st.selectbox("Choose Difficulty", ["Easy", "Medium", "Hard"], key="difficulty")

# Set difficulty parameters
if level == "Easy":
    max_num = 50
    max_tries = 10 
elif level == "Medium":
    max_num = 100
    max_tries = 7
else:
    max_num = 500
    max_tries = 5

# ------------------ Session State Initialization ------------------
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, max_num)
    st.session_state.tries = 0
    st.session_state.win = False
    st.session_state.game_over = False
    st.session_state.current_level = level
    st.session_state.guesses = []
    st.session_state.animation_shown = False

# Reset game if difficulty changed
if st.session_state.current_level != level:
    st.session_state.number = random.randint(1, max_num)
    st.session_state.tries = 0
    st.session_state.win = False
    st.session_state.game_over = False
    st.session_state.current_level = level
    st.session_state.guesses = []
    st.session_state.animation_shown = False

# ------------------ Game UI ------------------
st.markdown(f"### 📊 Game Info")
st.info(f"**Range:** 1 to {max_num} | **Attempts:** {max_tries}")

if not st.session_state.game_over:
    attempts_left = max_tries - st.session_state.tries
    if attempts_left > 0:
        st.write(f"**Attempts left:** *{attempts_left}*")
    else:
        st.write(f"**Attempts left:** *0*")

# Show previous guesses
if st.session_state.guesses:
    st.markdown("### 📝 Your Guesses")
    for idx, (g, hint) in enumerate(st.session_state.guesses, 1):
        if hint == "Correct":
            st.success(f"Attempt {idx}: {g} ✅")
        elif hint == "Higher":
            st.warning(f"Attempt {idx}: {g} ⬆️ (Low)")
        else:
            st.warning(f"Attempt {idx}: {g} ⬇️ (High)")

# ------------------ Input and Submit ------------------
if st.session_state.game_over:
    if st.session_state.win:
        st.info("🎮 Game finished! Click 'Restart Game' to play again.")
    else:
        st.info("🎮 Game over! Click 'Restart Game' to try again.")
else:
    guess = st.number_input("Enter your guess", min_value=1, max_value=max_num, step=1, key="guess_input")
    
    if st.button("Submit Guess", type="primary"):
        if guess < 1 or guess > max_num:
            st.error(f"Please enter a number between 1 and {max_num}")
        else:
            st.session_state.tries += 1

            if guess == st.session_state.number:
                st.session_state.win = True
                st.session_state.game_over = True
                st.session_state.guesses.append((guess, "Correct"))
                st.balloons()
                st.success(f"🎉 Congratulations! You won in {st.session_state.tries} tries!")

            elif st.session_state.tries >= max_tries:
                st.error("😢 Game Over! You ran out of attempts!")
                st.write(f"**The correct number was:** *{st.session_state.number}*")
                st.session_state.game_over = True
                if guess < st.session_state.number:
                    st.session_state.guesses.append((guess, "Higher"))
                else:
                    st.session_state.guesses.append((guess, "Lower"))

            else:
                if guess < st.session_state.number:
                    st.warning("⬆️ Go higher!")
                    st.session_state.guesses.append((guess, "Higher"))
                else:
                    st.warning("⬇️ Go lower!")
                    st.session_state.guesses.append((guess, "Lower"))
            st.rerun()

# ------------------ Car Animation (Improved) ------------------
if st.session_state.win and not st.session_state.animation_shown:
    st.markdown("---")
    st.subheader("🏁 Car Race Animation")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Calculate score
    base_score = 100
    penalty = st.session_state.tries * 5
    score = max(0, base_score - penalty)
    
    # Animate progress
    for i in range(101):
        progress_bar.progress(i / 100)
        if i < 30:
            status_text.text(f"🚗 Starting... {i}%")
        elif i < 60:
            status_text.text(f"🚗 Racing... {i}%")
        elif i < 90:
            status_text.text(f"🚗 Almost there... {i}%")
        else:
            status_text.text(f"🚗 Finishing... {i}%")
        time.sleep(0.03)
    
    status_text.empty()
    progress_bar.empty()
    st.success(f"🚗💨 **Race Finished!** Your Score: **{score}** points!")
    st.balloons()
    st.session_state.animation_shown = True

# ------------------ Restart Button ------------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Restart Game", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()