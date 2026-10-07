---
title: HeedX AI
emoji: 🧠
colorFrom: green
colorTo: gray
sdk: streamlit
sdk_version: 1.31.0
app_file: mental_app.py
pinned: false
---

# 🧠 AI Mental Health Decision Support System

## Overview
A Streamlit-based application that uses a pre-trained machine learning pipeline to analyze text responses and provide insights about mental health indicators.

## Features
- **Sentence-level analysis** - Each sentence analyzed independently
- **Multi-class prediction** - Anxiety, Depression, Suicidal, Normal
- **Aggregation logic** - Combines all predictions for overall assessment
- **Risk level classification** - Low, Mild, Moderate, Moderate-High, High
- **Recommendation engine** - Tailored guidance based on results
- **Crisis resources** - Immediate support information for high-risk cases
