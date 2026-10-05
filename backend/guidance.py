
def get_guidance(density, zone):
    return {
        "observed_condition":"Dense floating aquatic vegetation",
        "zone":zone,
        "severity":density,
        "potential_concerns":[
            "Reduced usable surface area",
            "Possible access or intake obstruction",
            "Increased maintenance burden"
        ],
        "suggested_category":"Targeted mechanical / physical surface removal where appropriate",
        "protocol_safeguard":"Verify species, site conditions, and local environmental requirements before treatment decisions.",
        "note":"Prototype decision support; human/site verification remains required."
    }
