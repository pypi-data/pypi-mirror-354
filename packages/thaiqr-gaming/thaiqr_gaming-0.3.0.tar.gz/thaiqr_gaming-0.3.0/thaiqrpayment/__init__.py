from io import BytesIO
import base64
import os
import re
from decimal import Decimal
import math

# Import dependencies with fallback for build environments
try:
    from PIL import Image, ImageDraw, ImageFont
    import qrcode
    import crc16
    _DEPENDENCIES_AVAILABLE = True
except ImportError:
    # Define placeholders for build environments
    Image = ImageDraw = ImageFont = qrcode = crc16 = None
    _DEPENDENCIES_AVAILABLE = False

def _check_dependencies():
    """Check if required dependencies are available."""
    if not _DEPENDENCIES_AVAILABLE:
        raise ImportError(
            "Required dependencies not available. "
            "Install with: pip install pillow qrcode crc16"
        )

__VERSION__ = "0.3.0"

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

ID_PAYLOAD_FORMAT = "00"
ID_POI_METHOD = "01"
ID_MERCHANT_INFORMATION_BOT = "29"
ID_TRANSACTION_CURRENCY = "53"
ID_TRANSACTION_AMOUNT = "54"
ID_COUNTRY_CODE = "58"
ID_CRC = "63"

PAYLOAD_FORMAT_EMV_QRCPS_MERCHANT_PRESENTED_MODE = "01"
POI_METHOD_STATIC = "11"
POI_METHOD_DYNAMIC = "12"
MERCHANT_INFORMATION_TEMPLATE_ID_GUID = "00"
BOT_ID_MERCHANT_PHONE_NUMBER = "01"
BOT_ID_MERCHANT_TAX_ID = "02"
BOT_ID_MERCHANT_EWALLET_ID = "03"
GUID_PROMPTPAY = "A000000677010111"
TRANSACTION_CURRENCY_THB = "764"
COUNTRY_CODE_TH = "TH"


def generate(code, insert_text=None):
    """Generate Thai QR Payment image"""
    _check_dependencies()

    # TODO: mode: color or black-white

    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1
    )
    qr.add_data(code)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.convert("RGB")

    # Add Logo
    logo_img = Image.open("{}/assets/logo.png".format(SCRIPT_PATH))
    template_img = Image.open("{}/assets/template.png".format(SCRIPT_PATH))

    # Logo image area should not more than 5% of qr code area
    qr_image_area = qr_img.size[0] * qr_img.size[1]
    logo_img_area = logo_img.size[0] * logo_img.size[1]
    pct_logo_area = math.ceil(logo_img_area / qr_image_area)

    if pct_logo_area > 0.05:
        # Resize logo
        ratio = (qr_image_area * 0.05) / logo_img_area
        logo_img = logo_img.resize(
            (
                round(logo_img.size[0] * ratio),
                round(logo_img.size[1] * ratio),
            )
        )

    # Center logo image
    pos = ((qr_img.size[0] - logo_img.size[0]) // 2, (qr_img.size[1] - logo_img.size[1]) // 2)
    qr_img.paste(logo_img, pos, mask=logo_img.split()[3])

    # Resize for template
    qr_img = qr_img.resize((750, 750))

    # paste qr image to template
    pos = (125, 407)
    template_img.paste(qr_img, pos)

    # Add custom text if provided - OVERLAY ON QR CODE for security
    if insert_text:
        draw = ImageDraw.Draw(template_img)
        try:
            # Use a bold font for better visibility on QR code
            font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 32)
        except (OSError, IOError):
            try:
                # Try regular Arial with larger size
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
            except (OSError, IOError):
                # Fallback to default font
                font = ImageFont.load_default()
        
        # Calculate text position (center on QR code area)
        text_bbox = draw.textbbox((0, 0), insert_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # QR code area: starts at (125, 407) with size 750x750
        qr_center_x = 125 + 750 // 2  # Center X of QR code
        qr_center_y = 407 + 750 // 2  # Center Y of QR code
        
        # Position text at the bottom area of QR code (still readable but secure)
        text_x = qr_center_x - text_width // 2
        text_y = qr_center_y + 200  # Lower part of QR code
        
        # Add semi-transparent background for better text visibility
        padding = 10
        bg_x1 = text_x - padding
        bg_y1 = text_y - padding
        bg_x2 = text_x + text_width + padding
        bg_y2 = text_y + text_height + padding
        
        # Draw semi-transparent white background
        draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(255, 255, 255, 200))
        
        # Add text with bold red color for security emphasis
        draw.text((text_x, text_y), insert_text, fill=(255, 0, 0), font=font)

    thaiqr_img = template_img.convert("RGB")
    return thaiqr_img


def save(code, path, insert_text=None):
    """Save Thai QR Payment to file"""
    _check_dependencies()
    img = generate(code, insert_text)
    img.save(path)


def to_base64(code, insert_text=None, include_uri=False):
    """Generate Thai QR Payment as base64 string"""
    _check_dependencies()
    img = generate(code, insert_text)

    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if include_uri:
        return "data:image/png;base64," + img_str

    return img_str


def generate_gaming_qr(code):
    """Generate QR code with 'Online Gaming Only' text"""
    return generate(code, insert_text="Online Gaming Only")


def save_gaming_qr(code, path):
    """Save QR code with 'Online Gaming Only' text"""
    return save(code, path, insert_text="Online Gaming Only")


def gaming_qr_to_base64(code, include_uri=False):
    """Generate base64 QR code with 'Online Gaming Only' text"""
    return to_base64(code, insert_text="Online Gaming Only", include_uri=include_uri)


def generate_code_from_mobile(number, amount):
    """Generate QR code from mobile number and amount"""
    _check_dependencies()

    sanitized_number = sanitize_input(number)
    pp_type = (
        BOT_ID_MERCHANT_EWALLET_ID
        if len(sanitized_number) >= 15
        else BOT_ID_MERCHANT_TAX_ID
        if len(sanitized_number) >= 13
        else BOT_ID_MERCHANT_PHONE_NUMBER
    )

    pp_payload = generate_txt(ID_PAYLOAD_FORMAT, PAYLOAD_FORMAT_EMV_QRCPS_MERCHANT_PRESENTED_MODE)
    pp_amount_type = generate_txt(
        ID_POI_METHOD, POI_METHOD_DYNAMIC if amount else POI_METHOD_STATIC
    )

    pp_merchant_info = generate_txt(
        ID_MERCHANT_INFORMATION_BOT,
        generate_txt(MERCHANT_INFORMATION_TEMPLATE_ID_GUID, GUID_PROMPTPAY)
        + generate_txt(pp_type, format_input(sanitized_number)),
    )

    pp_country_code = generate_txt(ID_COUNTRY_CODE, COUNTRY_CODE_TH)
    pp_currency = generate_txt(ID_TRANSACTION_CURRENCY, TRANSACTION_CURRENCY_THB)
    pp_decimal_value = (amount if is_positive_decimal(amount) else 0) and generate_txt(
        ID_TRANSACTION_AMOUNT, format_amount(amount)
    )

    raw_data = (
        pp_payload
        + pp_amount_type
        + pp_merchant_info
        + pp_country_code
        + pp_currency
        + pp_decimal_value
        + ID_CRC
        + "04"
    )

    return raw_data + str.upper(
        hex(crc16.crc16xmodem(raw_data.encode("ascii"), 0xFFFF)).replace("0x", "")
    )


def sanitize_input(input):
    return re.sub(r"(\D.*?)", "", input)


def generate_txt(id, value):
    return id + str(len(value)).zfill(2) + value


def format_input(id):
    numbers = sanitize_input(id)
    if len(numbers) >= 13:
        return numbers
    return (re.sub(r"^0", "66", numbers)).zfill(13)


def format_amount(amount):
    TWOPLACES = Decimal(10) ** -2
    return str(Decimal(amount).quantize(TWOPLACES))


def is_positive_decimal(n):
    try:
        a = float(n)
    except ValueError:
        return False
    else:
        return True if a > 0 else False


def generate_secure_qr(code, watermark_text="GAMING ONLY"):
    """Generate QR code with security watermark directly on the QR pattern"""
    _check_dependencies()
    # Generate QR with basic text overlay first
    qr_img = generate(code, insert_text=watermark_text)
    
    # Add additional security watermark directly on QR pattern
    draw = ImageDraw.Draw(qr_img)
    try:
        # Small font for QR pattern overlay
        font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 16)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        except (OSError, IOError):
            font = ImageFont.load_default()
    
    # Add multiple small watermarks across the QR code area for security
    qr_start_x = 125
    qr_start_y = 407
    qr_size = 750
    
    # Add watermarks at strategic positions
    positions = [
        (qr_start_x + 50, qr_start_y + 50),   # Top-left
        (qr_start_x + qr_size - 150, qr_start_y + 50),  # Top-right
        (qr_start_x + 50, qr_start_y + qr_size - 100),  # Bottom-left
        (qr_start_x + qr_size - 150, qr_start_y + qr_size - 100)  # Bottom-right
    ]
    
    for x, y in positions:
        # Add semi-transparent background
        text_bbox = draw.textbbox((0, 0), "GAMING", font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Draw background rectangle
        draw.rectangle([x-5, y-5, x+text_width+5, y+text_height+5], 
                      fill=(255, 255, 255, 180))
        
        # Draw text
        draw.text((x, y), "GAMING", fill=(255, 0, 0), font=font)
    
    return qr_img


def save_secure_gaming_qr(code, path):
    """Save QR code with secure gaming watermarks that cannot be easily removed"""
    img = generate_secure_qr(code, "ONLINE GAMING ONLY")
    img.save(path)


def secure_gaming_qr_to_base64(code, include_uri=False):
    """Generate base64 QR code with secure gaming watermarks"""
    img = generate_secure_qr(code, "ONLINE GAMING ONLY")
    
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if include_uri:
        return "data:image/png;base64," + img_str

    return img_str


def generate_embedded_watermark_qr(code, watermark_text="GAMING USE ONLY"):
    """Generate QR code with watermark embedded directly into the QR pattern before template application"""
    _check_dependencies()
    
    # Generate base QR code
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=1
    )
    qr.add_data(code)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.convert("RGB")
    
    # Add watermark directly to raw QR code before applying template
    draw = ImageDraw.Draw(qr_img)
    try:
        # Calculate font size based on QR code size
        qr_width = qr_img.size[0]
        font_size = max(12, qr_width // 25)
        font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", font_size)
    except (OSError, IOError):
        try:
            font_size = max(14, qr_width // 20)
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()
    
    # Position watermark in center of QR code
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (qr_img.width - text_width) // 2
    text_y = (qr_img.height - text_height) // 2
    
    # Add white background with some transparency
    padding = 8
    bg_x1 = text_x - padding
    bg_y1 = text_y - padding
    bg_x2 = text_x + text_width + padding
    bg_y2 = text_y + text_height + padding
    
    # Create a semi-transparent overlay
    overlay = Image.new('RGBA', qr_img.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Draw semi-transparent white background
    overlay_draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(255, 255, 255, 220))
    
    # Draw the text on overlay
    overlay_draw.text((text_x, text_y), watermark_text, fill=(255, 0, 0, 255), font=font)
    
    # Composite the overlay onto the QR code
    qr_img = Image.alpha_composite(qr_img.convert('RGBA'), overlay).convert('RGB')

    # Continue with normal template processing
    logo_img = Image.open("{}/assets/logo.png".format(SCRIPT_PATH))
    template_img = Image.open("{}/assets/template.png".format(SCRIPT_PATH))

    # Logo image area should not more than 5% of qr code area
    qr_image_area = qr_img.size[0] * qr_img.size[1]
    logo_img_area = logo_img.size[0] * logo_img.size[1]
    pct_logo_area = math.ceil(logo_img_area / qr_image_area)

    if pct_logo_area > 0.05:
        # Resize logo
        ratio = (qr_image_area * 0.05) / logo_img_area
        logo_img = logo_img.resize(
            (
                round(logo_img.size[0] * ratio),
                round(logo_img.size[1] * ratio),
            )
        )

    # Center logo image
    pos = ((qr_img.size[0] - logo_img.size[0]) // 2, (qr_img.size[1] - logo_img.size[1]) // 2)
    qr_img.paste(logo_img, pos, mask=logo_img.split()[3])

    # Resize for template
    qr_img = qr_img.resize((750, 750))

    # paste qr image to template
    pos = (125, 407)
    template_img.paste(qr_img, pos)

    thaiqr_img = template_img.convert("RGB")
    return thaiqr_img


def save_embedded_gaming_qr(code, path):
    """Save QR code with watermark embedded into the QR pattern itself"""
    img = generate_embedded_watermark_qr(code, "GAMING USE ONLY")
    img.save(path)


def embedded_gaming_qr_to_base64(code, include_uri=False):
    """Generate base64 QR code with embedded watermark"""
    img = generate_embedded_watermark_qr(code, "GAMING USE ONLY")
    
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if include_uri:
        return "data:image/png;base64," + img_str

    return img_str
