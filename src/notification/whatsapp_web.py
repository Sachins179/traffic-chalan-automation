"""
WhatsApp Web manual launcher.
Builds a wa.me link with a pre-filled multi-violation chalan message.
"""
import urllib.parse


def build_whatsapp_link(
    to_mobile: str,
    name: str,
    violation_names: list[str],
    total_fine: int,
    vehicle_number: str,
) -> str:
    """
    Build a wa.me link with a pre-filled message.

    Args:
        to_mobile: Recipient mobile number.
        name: Recipient name.
        violation_names: List of violation names.
        total_fine: Total fine amount in INR.
        vehicle_number: Vehicle registration number.

    Returns:
        A URL of the form https://wa.me/<number>?text=<encoded-message>
    """
    number = (
        to_mobile.strip()
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
    )
    if len(number) == 10:
        number = "91" + number

    violations_str = "\n".join(f"  • {v}" for v in violation_names)

    message = (
        f"🚦 *Traffic Chalan Notice*\n\n"
        f"Dear {name},\n\n"
        f"Your vehicle *{vehicle_number}* was detected with "
        f"the following violations:\n\n"
        f"{violations_str}\n\n"
        f"💰 *Total Fine:* Rs. {total_fine}\n\n"
        f"Please pay within 15 days to avoid additional penalties.\n\n"
        f"— Traffic Police Dept."
    )

    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{number}?text={encoded}"