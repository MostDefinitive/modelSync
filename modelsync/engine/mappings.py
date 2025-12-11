# Minimal demo mapping for the prototype — expand as you go.
ICD_TO_HCC_V24 = {
    "E119": "HCC18",   # Type 2 DM w/o complications
    "E1165": "HCC19",  # Type 2 DM w/ complications
    "I509": "HCC85",   # Heart failure
    "I119": "HCC34",   # Hypertensive heart disease w/o HF (placeholder HCC for demo)
    "N183": "HCC138",  # CKD stage 3
    "N184": "HCC137",  # CKD stage 4
}

# Very simple hierarchy examples for demo purposes
HIERARCHY_V24 = {
    "HCC137": ["HCC138"],  # CKD4 supersedes CKD3
    "HCC19": ["HCC18"],    # Diabetes w/ complications supersedes w/o
}
