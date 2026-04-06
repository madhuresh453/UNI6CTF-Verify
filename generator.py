from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import qrcode

from utils import generate_cert_id
from config import BASE_URL
import hashlib

# ===============================
# 📂 LOAD DATA
# ===============================
df = pd.read_csv("data/participants.csv")
df.columns = df.columns.str.strip()

template_path = "templates/certificate.png"
font_path = "fonts/arial.ttf"

os.makedirs("output/certificates", exist_ok=True)

# ===============================
# 🔢 LOAD LAST CERT ID (SAFE)
# ===============================
start_index = 1

if os.path.exists("output/final_data.csv") and os.path.getsize("output/final_data.csv") > 0:
    old_df = pd.read_csv("output/final_data.csv")
    old_df.columns = old_df.columns.str.strip()

    if 'Certificate ID' in old_df.columns:
        last_ids = old_df['Certificate ID'].dropna()

        if len(last_ids) > 0:
            last_num = max([
                int(str(x).split("-")[-1]) for x in last_ids
            ])
            start_index = last_num + 1

# ===============================
# 🔁 LOOP THROUGH USERS
# ===============================
for i, row in df.iterrows():

    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # ✅ UNIQUE CERT ID
    cert_id = generate_cert_id(start_index + i)
    verify_link = BASE_URL + cert_id
    hash_value = hashlib.sha256(cert_id.encode()).hexdigest()
    df.loc[i, 'Hash'] = hash_value

    username = str(row['Username'])
    team = str(row['Team Name'])
    rank = str(row['Rank'])
    points = str(row['Points'])
    full_name = str(row['Full Name'])

    white = (255, 255, 255)

    # ===============================
    # 👤 FULL NAME (AUTO FIT)
    # ===============================
    font_size = 50
    min_font_size = 30

    while font_size >= min_font_size:
        font_name = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), full_name, font=font_name)
        text_width = bbox[2] - bbox[0]

        if text_width <= img.width - 200:
            break
        font_size -= 2

    draw.text((img.width // 2, 275), full_name, font=font_name, fill=white, anchor="mm")

    # ===============================
    # 🟡 CERTIFICATE ID (TOP CENTER)
    # ===============================
    font_id = ImageFont.truetype(font_path, 18)
    text = cert_id
    spacing = 5

    total_width = 0
    for char in text:
        total_width += draw.textbbox((0, 0), char, font=font_id)[2] + spacing
    total_width -= spacing

    x = (img.width - total_width) / 2
    y = 3

    current_x = x
    for char in text:
        draw.text((current_x, y), char, font=font_id, fill=white)
        char_width = draw.textbbox((0, 0), char, font=font_id)[2]
        current_x += char_width + spacing

    # ===============================
    # 👤 USERNAME
    # ===============================
    font_small = ImageFont.truetype(font_path, 32)
    font_main = ImageFont.truetype(font_path, 22)

    label_x = 195
    label_y = 328

    label_text = "Username:"
    label_width = draw.textbbox((0, 0), label_text, font=font_small)[2]

    username_x = label_x + label_width + 15
    draw.text((username_x, label_y), username, font=font_main, fill=white)

    # ===============================
    # 👥 TEAM
    # ===============================
    draw.text((635, 328), team, font=font_main, fill=white)

    # ===============================
    # 🏆 RANK & 🔥 POINTS
    # ===============================
    draw.text((428, 461), rank, font=font_main, fill=white)
    draw.text((700, 461), points, font=font_main, fill=white)

    # ===============================
    # 🔗 QR CODE
    # ===============================
    qr = qrcode.make(verify_link).resize((140, 140))
    img.paste(qr, (91, 63))

    # ===============================
    # 💾 SAVE FILE (INSIDE LOOP ✅)
    # ===============================
    filename = f"output/certificates/{username}.png"
    img.save(filename)

    # ✅ UPDATE DF (INSIDE LOOP)
    df.loc[i, 'Certificate ID'] = cert_id
    df.loc[i, 'File'] = filename

    print(f"✅ Generated: {username}")

# ===============================
# 💾 SAVE CSV (ONCE)
# ===============================
output_file = "output/final_data.csv"

columns = ['Full Name', 'Username', 'Team Name', 'Rank', 'Points', 'Email', 'Certificate ID', 'File']
df = df[columns]

if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
    old_df = pd.read_csv(output_file)
    old_df.columns = old_df.columns.str.strip()

    final_df = pd.concat([old_df, df], ignore_index=True)
    final_df = final_df.drop_duplicates(subset=['Certificate ID'], keep='last')

    final_df.to_csv(output_file, index=False)
else:
    df.to_csv(output_file, index=False)

print("🎉 All Certificates Generated Successfully!")