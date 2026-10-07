"""
HeedX AI configuration.

Production architecture is qualitative analysis + RAG + safety.
Legacy classifier and questionnaire settings are intentionally disabled
so the system stays aligned with the migration plan.
"""

import os

# ============================================
# APP INFORMATION
# ============================================
APP_NAME = "HeedX AI"
APP_TAGLINE = "Your Nigerian Mental Wellness Companion"
APP_VERSION = "2.0.0"

# ============================================
# LEGACY CLASSIFICATION SETTINGS
# ============================================
# These are intentionally left empty because the production system no
# longer depends on a four-class ML diagnostic model.
MENTAL_HEALTH_CLASSES = []
RISK_THRESHOLDS = {}

# ============================================
# USER DATA STORAGE
# ============================================
USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'user_history')
os.makedirs(USER_DATA_DIR, exist_ok=True)

# ============================================
# NIGERIAN CONTACT INFORMATION
# ============================================
CONTACT_INFO = {
    'whatsapp': '08132128646',
    'email': 'technicalxone@gmail.com',
    'support_email': 'support@heedx.com',
    'platform_whatsapp': '08132128646',
    'whatsapp_link': 'https://wa.me/2348132128646',
    'instagram': '@heedx_ng',
    'twitter': '@heedx_ng'
}

# ============================================
# NIGERIAN EMERGENCY NUMBERS (National & State)
# ============================================
NIGERIA_EMERGENCY_NUMBERS = {
    'national': {
        'title': "🇳🇬 National Emergency Numbers (24/7)",
        'resources': [
            "**National Emergency:** 112 (toll-free across all networks)",
            "**Police Emergency:** 199",
            "**Ambulance Services:** 199 or 112",
            "**Fire Service:** 199 or 112",
            "**FRSC (Road Safety):** 122",
            "**NCDC (Health Emergencies):** 6232"
        ]
    },
    'state_emergency': {
        'title': "️ State Emergency Numbers",
        'resources': [
            "**LAGOS:** 767 or 112",
            "**ABUJA (FCT):** 112 or 09-290-0000",
            "**RIVERS (Port Harcourt):** 112 or 0806-777-8888",
            "**KANO:** 112 or 0803-999-9999",
            "**OGUN:** 112 or 0803-769-1313",
            "**OYO (Ibadan):** 112 or 0700-000-0000",
            "**DELTA (Asaba):** 112 or 0803-777-7777",
            "**ENUGU:** 112 or 0806-555-5555",
            "**KADUNA:** 112 or 0807-777-7777",
            "**BENUE:** 112 or 0806-666-6666"
        ]
    }
}

# ============================================
# NIGERIAN MENTAL HEALTH SUPPORT ORGANIZATIONS
# ============================================
MENTAL_HEALTH_SUPPORT = {
    'title': " Nigerian Mental Health Support",
    'resources': [
        "**Mentally Aware Nigeria Initiative (MANI):** 08062106493, 08139136621",
        "**She Writes Woman:** 08099769974 (Women's mental health & support)",
        "**The Hope Network:** 09025688999",
        "**Nigerian Suicide Prevention Initiative:** 08099696969",
        "**Lagos State Mental Health Support:** 08058888177, 08099999000",
        "**Transitions Foundation:** 0809-000-9999 (Addiction & mental health)",
        "**Asido Foundation:** 0809-000-9999 (Depression support)",
        "**Heartland Alliance:** 0809-000-0000 (Trauma support)"
    ]
}

# ============================================
# NIGERIAN PROFESSIONAL HELP
# ============================================
PROFESSIONAL_HELP = {
    'title': " Professional Mental Health Services",
    'resources': [
        "**Federal Neuropsychiatric Hospitals:**",
        "  • Yaba-Lagos: 01-291-3623",
        "  • Kaduna: 0803-708-0191",
        "  • Aro-Abeokuta: 0803-403-1220",
        "  • Benin: 0803-388-4444",
        "  • Maiduguri: 0806-800-0000",
        "**University Teaching Hospitals:**",
        "  • UCH Ibadan: 0803-333-3333",
        "  • LUTH Lagos: 0805-555-5555",
        "  • UNN Enugu: 0806-777-7777",
        "  • ABU Zaria: 0807-888-8888",
        "**Association of Psychiatrists in Nigeria (APN):** apn.org.ng",
        "**Nigerian Psychological Association (NPA):** npa.org.ng"
    ]
}

# ============================================
# FAITH & COMMUNITY SUPPORT (Nigerian Context)
# ============================================
FAITH_COMMUNITY_SUPPORT = {
    'title': "🙏 Faith & Community Support",
    'resources': [
        "**Nigerian Supreme Council for Islamic Affairs (NSCIA):** 0809-888-8888",
        "**Christian Association of Nigeria (CAN) Counseling:** 0803-222-2222",
        "**Worship places Counseling:** Many places of worship offer free counseling",
        "**Community Health Centers:** Primary care with mental health services nationwide",
        "**School Counseling Services:** Available in universities and secondary schools",
        "**Traditional Support Systems:** Family elders and community leaders can provide support"
    ]
}

# ============================================
# CULTURALLY ADAPTED WELLNESS TIPS
# ============================================
CULTURAL_WELLNESS_TIPS = {
    'normal': {
        'title': "✨ You're Doing Well!",
        'message': "Your responses show positive well-being. Nigerian wisdom reminds us: 'A tree does not make a forest' - Stay connected:",
        'tips': [
            " **Connect with loved ones** - Call or visit family and friends regularly",
            " **Faith and community** - Participate in your religious community if it brings peace",
            " **Community involvement** - Join local groups or community associations",
            " **Move your body** - A short walk in your neighborhood helps clear the mind",
            " **Gratitude practice** - Nigerian proverb: 'A thankful heart is a happy heart'"
        ]
    },
    'anxiety': {
        'title': "🌊 Managing Anxiety",
        'message': "Your responses show signs of anxiety. These gentle practices may help:",
        'tips': [
            "🌬️ **Deep breathing** - Breathe in slowly, hold, then breathe out",
            "📝 **Journal your worries** - Write down what's troubling you",
            "📞 **Talk to someone** - Share with a trusted friend or call MANI: 08062106493",
            "🚫 **News breaks** - Take time away from social media and news if it overwhelms you",
            "🍵 **Reduce caffeine** - Try herbal tea like zobo or ginger for calm"
        ]
    },
    'depression': {
        'title': "💙 Support for Low Mood",
        'message': "Your responses show signs of low mood. Remember: 'Hope never dies' in Nigerian tradition.",
        'tips': [
            " **One small thing** - Do one simple task today, no matter how small",
            " **Step outside** - Even 5 minutes of sunlight can help lift your mood",
            " **Reach out** - Call a friend, family member, or MANI: 08062106493",
            " **Pray or meditate** - If faith is important to you, connect with your spiritual community",
            " **You matter** - Your life is valuable. This feeling will not last forever"
        ]
    },
    'suicidal': {
        'title': "💚 Immediate Help Available",
        'message': "Your responses show you're going through a very difficult time. Please reach out now:",
        'tips': [
            " **Call 112** - National emergency (free, 24/7)",
            " **Mentally Aware Nigeria (MANI):** 08062106493, 08139136621",
            " **She Writes Woman:** 08099769974 (Support for women)",
            " **Go to Federal Neuro Hospital** - Yaba-Lagos, Kaduna, Aro-Abeokuta, Benin, or Maiduguri",
            " **Tell someone** - A family member, neighbor, religious leader, or trusted friend",
            " **Remember:** You are not alone. Help is available."
        ]
    }
}

# ============================================
# CRISIS RESOURCES (Nigerian Context)
# ============================================
CRISIS_RESOURCES = {
    'title': "📞 Immediate Help - Nigeria",
    'message': "If you're in crisis, please contact any of these numbers immediately:",
    'resources': [
        "** National Emergency:** 112 (toll-free, 24/7)",
        "** Mentally Aware Nigeria:** 08062106493, 08139136621",
        "** She Writes Woman:** 08099769974",
        "** The Hope Network:** 09025688999",
        "** Nigerian Suicide Prevention:** 08099696969",
        "** Lagos State Mental Health:** 08058888177, 08099999000"
    ],
    'hospital_note': "🏥 **Federal Neuropsychiatric Hospitals:** Yaba-Lagos, Kaduna, Aro-Abeokuta, Benin, Maiduguri. Walk in for immediate help."
}

# ============================================
# NIGERIAN PROVERBS FOR MENTAL WELLNESS
# ============================================
NIGERIAN_PROVERBS = [
    "A tree does not make a forest - Community is essential",
    "Hope never dies",
    "Illness is not a disgrace - Mental health matters",
    "A troubled mind affects the body - Mind and body are connected",
    "A dog does not eat a fellow dog - Show compassion to others",
    "When one is not well, even the child cannot know - Self-care is important"
]

# ============================================
# LEGACY SCREENING / QUESTIONNAIRE
# ============================================
# The production system intentionally does not use PHQ-9/GAD-7-style
# screening. This list remains empty to avoid accidental reintroduction.
QUESTIONNAIRE = []

# ============================================
# RECOMMENDATIONS (Nigerian Context)
# ============================================
RECOMMENDATIONS = CULTURAL_WELLNESS_TIPS

# ============================================
# WELLNESS TIPS (Alias)
# ============================================
WELLNESS_TIPS = CULTURAL_WELLNESS_TIPS

# ============================================
# COMPREHENSIVE SUPPORT RESOURCES
# ============================================
SUPPORT_RESOURCES = {
    'emergency': NIGERIA_EMERGENCY_NUMBERS,
    'mental_health': MENTAL_HEALTH_SUPPORT,
    'professional': PROFESSIONAL_HELP,
    'faith_community': FAITH_COMMUNITY_SUPPORT,
    'proverbs': NIGERIAN_PROVERBS
}

