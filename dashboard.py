"""Volunteer dashboard: see overdue loans on one screen.

Usage:
    streamlit run dashboard.py

This page only reads data. It never sends emails.
"""

from datetime import date

import streamlit as st

from notifier.loans import find_overdue, read_loans_from_csv

# For now, the made-up sample file. Later, the loans exported from Handy Library.
LOANS_PATH = "data/sample_loans.csv"

st.title("교회 도서부 대시보드")

today = st.date_input("기준 날짜", value=date.today())

loans, problems = read_loans_from_csv(LOANS_PATH)
overdue = find_overdue(loans, today)

st.subheader(f"연체 도서 ({len(overdue)}권)")
st.dataframe(
    [
        {
            "이름": loan.member_name,
            "이메일": loan.email or "(없음)",
            "책 제목": loan.book_title,
            "반납 예정일": loan.due_date,
            "지난 날수": (today - loan.due_date).days,
        }
        for loan in sorted(overdue, key=lambda l: l.due_date)
    ],
    hide_index=True,
)

# Rows that could not be read, so a volunteer can fix them in the export
if problems:
    st.warning("읽지 못한 줄이 있어요:\n\n" + "\n".join(f"- {p}" for p in problems))
