import streamlit as st
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import HRFlowable
from reportlab.platypus import Frame, PageTemplate
from reportlab.platypus import BaseDocTemplate
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


def create_radar_chart_personality_traits(user_data):
    labels = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    values = [
        user_data["user_personality"]["openness"],
        user_data["user_personality"]["conscientiousness"],
        user_data["user_personality"]["extraversion"],
        user_data["user_personality"]["agreeableness"],
        user_data["user_personality"]["neuroticism"]
    ]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    chart_color = "#3C685B"
    ax.plot(angles, values, color=chart_color, linewidth=2)
    ax.fill(angles, values, color=chart_color, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    return buffer


def generate_pdf_profile(user_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CenteredTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
    )

    header_image_path = Path(__file__).resolve().parent.parent / "images" / "header-option2.jpeg"
    if header_image_path.exists():
        img_width, img_height = ImageReader(str(header_image_path)).getSize()
        header = Image(str(header_image_path))
        header.drawWidth = doc.width
        header.drawHeight = doc.width * (img_height / img_width)
        elements.append(header)
        elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Your Glasshome User Profile", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"<b>Name:</b> {user_data['name']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Email:</b> {user_data['email']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Resident Type:</b> {user_data['resident_type']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Household Composition:</b> {user_data['householdcomposition']}", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    # Your Practical Requirements
    elements.append(Paragraph("<b>Your Practical Requirements</b>", styles["Heading2"]))
    practical_labels = {
        "desired_location": "Desired location",
        "physical_environment": "Physical environment",
        "size_of_community": "Size of community",
        "regime_of_sharing": "Shared areas",
        "private_dwelling": "Private dwelling features",
        "daily_management": "Daily management",
        "quiet_hours_importance": "Quiet hours importance",
        "guest_policy_importance": "Guest policy importance",
        "legal_structure": "Legal structure",
        "budget_currency": "Budget currency",
        "monthly_budget_rent": "Monthly rent budget",
        "available_budget_purchase": "Available budget for purchase",
        "other_practical_requirements": "Other practical requirements",
    }

    practical_results = []
    for key, label in practical_labels.items():
        value = user_data["user_requirements"].get(key)
        if value in (None, "", [], {}):
            continue
        if isinstance(value, list):
            value_text = ", ".join(str(item) for item in value)
        else:
            value_text = str(value)
        practical_results.append(Paragraph(f"<b>{label}:</b> {value_text}", styles["Normal"]))

    if practical_results:
        elements.append(ListFlowable(practical_results, bulletType="bullet"))
    else:
        elements.append(Paragraph("No practical requirements provided.", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Your Lifestyle Preferences
    elements.append(Paragraph("<b>Your Lifestyle Preferences</b>", styles["Heading2"]))
    lifestyle_labels = {
        "contact_with_neighbours": "Contact with neighbors importance",
        "mix_of_household": "Mix of household importance",
        "degree_shared_responsibility": "Degree of shared responsibility",
        "frequency_shared_activities": "Frequency of shared activities",
        "communal_activities": "Communal activities",
        "desired_animals": "Desired animals",
        "forbidden_animals": "Forbidden animals",
        "dietary_restrictions": "Dietary restrictions",
        "smoking_tolerance": "Smoking tolerance",
        "hobbies": "Hobbies",
        "other_requirements": "Other requirements"
    }

    lifestyle_results = []
    for key, label in lifestyle_labels.items():
        value = user_data["user_requirements"].get(key)
        if value in (None, "", [], {}):
            continue
        if isinstance(value, list):
            value_text = ", ".join(str(item) for item in value)
        else:
            value_text = str(value)
        lifestyle_results.append(Paragraph(f"<b>{label}:</b> {value_text}", styles["Normal"]))

    if lifestyle_results:
        elements.append(ListFlowable(lifestyle_results, bulletType="bullet"))
    else:
        elements.append(Paragraph("No lifestyle preferences provided.", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Radar Chart for Personality Traits
    elements.append(Paragraph("<b>Your Personality Traits</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    big_five_text = """Your personality traits are based on the Big Five model, which includes Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism."""
    elements.append(Paragraph(big_five_text, styles["Normal"]))
    chart_buffer = create_radar_chart_personality_traits(user_data)
    elements.append(Image(chart_buffer, width=4*inch, height=4*inch))
    elements.append(Spacer(1, 0.3 * inch))

    # Your values
    elements.append(Paragraph("<b>Your Values</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    values_text = """You are highly community-oriented, valuing shared rituals and sustainability. You prefer structured co-living environments with clear agreements and active social engagement."""
    elements.append(Paragraph(values_text, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_pdf_matches(user_data, matches):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CenteredTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
    )

    header_image_path = Path(__file__).resolve().parent.parent / "images" / "header-option2.jpeg"
    if header_image_path.exists():
        img_width, img_height = ImageReader(str(header_image_path)).getSize()
        header = Image(str(header_image_path))
        header.drawWidth = doc.width
        header.drawHeight = doc.width * (img_height / img_width)
        elements.append(header)
        elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Your Glasshome Matches", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"<b>Name:</b> {user_data['name']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Email:</b> {user_data['email']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Resident Type:</b> {user_data['resident_type']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Household Composition:</b> {user_data['householdcomposition']}", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    # Your Top Matches
    elements.append(Paragraph("<b>Your Top Compatibility Matches</b>", styles["Heading2"]))
    if matches.empty:
        elements.append(Paragraph("No matches found based on your profile.", styles["Normal"]))
    else:
        for index, row in matches.iterrows():
            match_info = f"""
            <b>Match {index + 1}:</b><br/>
            Name: {row['name']}<br/>
            Email: {row['email']}<br/>
            Compatibility Score: {row['compatibility_score']:.2f}
            """
            elements.append(Paragraph(match_info, styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer
