import streamlit as st
from datetime import datetime, timedelta
import calendar

def display_streak_calendar(submitted_dates):
    submitted_dates = set(submitted_dates)
    today = datetime.now().date()
    start_date = today - timedelta(days=180)

    # Create a list of weeks, each week is 7 squares
    grid_html = "<div style='display: flex; gap: 4px;'>"
    for week in range(27):  # approx 6 months
        week_html = "<div style='display: flex; flex-direction: column; gap: 4px;'>"
        for day in range(7):
            current = start_date + timedelta(days=week * 7 + day)
            color = "#4CAF50" if current.strftime("%Y-%m-%d") in submitted_dates else "#2d2f31"
            week_html += f"<div style='width: 14px; height: 14px; background: {color}; border-radius: 2px;'></div>"
        week_html += "</div>"
        grid_html += week_html
    grid_html += "</div>"

    st.markdown("#### 🗓️ Submission Calendar")
    st.markdown(grid_html, unsafe_allow_html=True)


def get_streak_badge(submitted_dates):
    streak = 0
    today = datetime.now().date()
    for i in range(30):
        day = today - timedelta(days=i)
        if day.strftime("%Y-%m-%d") in submitted_dates:
            streak += 1
        else:
            break
    if streak >= 15:
        return "🏆 15-Day Streak Badge!"
    elif streak >= 7:
        return "🥇 7-Day Streak Badge!"
    elif streak >= 3:
        return "🎖 3-Day Streak Badge!"
    else:
        return None
