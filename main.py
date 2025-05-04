import numpy as np
import os
import pandas as pd
import sys
import requests
from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode

# Importação de módulo próprio
sys.path.append(os.getcwd())
from classes.class_image_creation import ImageCreation

semana = "semana6"
alunos = pd.read_excel("alunos.xlsx")

# Removendo acentos e caracteres especiais
alunos["Nome completo\n"] = (
    alunos["Nome completo\n"].apply(lambda x: unidecode(x)).str.strip()
)
alunos["Nome para o Cartão de Conquistas"] = (
    alunos["Nome para o Cartão de Conquistas"].apply(lambda x: unidecode(x)).str.strip()
)

# Padronizando colunas de flag
atividade_columns = ["Atvd. 1", "Atvd. 2", "Atvd. 3", "Atvd. 4", "Atvd. 5"]
for column in atividade_columns:
    alunos[column] = alunos[column].astype(str).str.upper().str.strip()
    # Transformando NAN em NÃO
    alunos[column] = np.where(alunos[column] == "NAN", "NÃO", alunos[column])

# Criando uma coluna padronizada de flag
alunos["flag"] = (
    alunos["Atvd. 1"]
    + alunos["Atvd. 2"]
    + alunos["Atvd. 3"]
    + alunos["Atvd. 4"]
    + alunos["Atvd. 5"]
)


# Convert "open" links to "uc" links for direct download
alunos["Foto para o Cartão de Conquistas"] = alunos[
    "Foto para o Cartão de Conquistas"
].str.replace("open", "uc")
alunos["Foto para o Cartão de Conquistas"] = (
    alunos["Foto para o Cartão de Conquistas"] + "&export=download"
)


# Process each student
for email in alunos["E-mail"].unique():
    try:
        nome = alunos[alunos["E-mail"] == email][
            "Nome para o Cartão de Conquistas"
        ].values[0]
        nome_completo = alunos[alunos["E-mail"] == email]["Nome completo\n"].values[0]
        nome_completo = nome_completo.split(" ")[0] + " " + nome_completo.split(" ")[-1]
        foto = alunos[alunos["E-mail"] == email][
            "Foto para o Cartão de Conquistas"
        ].values[0]
        total_palavras = alunos[alunos["E-mail"] == email]["TOTAL DE PALAVRAS"].values[
            0
        ]
        flg = alunos[alunos["E-mail"] == email]["flag"].values[0]
        flg_1 = alunos[alunos["E-mail"] == email]["Atvd. 1"].values[0]
        flg_2 = alunos[alunos["E-mail"] == email]["Atvd. 2"].values[0]
        flg_3 = alunos[alunos["E-mail"] == email]["Atvd. 3"].values[0]
        flg_4 = alunos[alunos["E-mail"] == email]["Atvd. 4"].values[0]
        flg_5 = alunos[alunos["E-mail"] == email]["Atvd. 5"].values[0]

        list_flg = []
        list_flg.append(flg_1)
        list_flg.append(flg_2)
        list_flg.append(flg_3)
        list_flg.append(flg_4)
        list_flg.append(flg_5)
        atividades_feitas = list_flg.count("SIM")

        # Download the photo
        response = requests.get(foto)
        if response.status_code == 200:
            with open("downloaded_image.png", "wb") as file:
                file.write(response.content)

        # Open and process the image
        image = Image.open("downloaded_image.png").convert("RGBA")

        # Resize the image to the target size
        size = (300, 300)
        image = image.resize(size, Image.Resampling.LANCZOS)

        # Create a circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)

        # Create a new RGBA image for the circular crop
        circular_image = Image.new("RGBA", size)
        circular_image.paste(image, (0, 0), mask=mask)

        # Get background
        if flg == "NÃONÃONÃONÃONÃO":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_naonaonaonaonao.jpeg"
            )
        elif flg == "SIMSIMSIMSIMSIM":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimsimsimsim.jpeg"
            )
        elif flg == "SIMSIMSIMSIMNÃO":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimsimsimnao.jpeg"
            )
        elif flg == "SIMSIMSIMNÃONÃO":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimsimnaonao.jpeg"
            )
        elif flg == "SIMSIMNÃOSIMSIM":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimnaosimsim.jpeg"
            )
        elif flg == "SIMNÃONÃONÃOSIM":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simnaonaonaosim.jpeg"
            )
        elif flg == "SIMSIMNÃONÃONÃO":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimnaonaonao.jpeg"
            )
        elif flg == "SIMNAONÃONÃONÃO":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simnaonaonaonao.jpeg"
            )
        elif flg == "SIMSIMNÃONÃOSIM":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimnaonaosim.jpeg"
            )
        elif flg == "SIMNÃOSIMNÃOSIM":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simnaosimnaosim.jpeg"
            )
        elif flg == "SIMSIMSIMNÃOSIM":
            background = ImageCreation().get_background(
                rf"fundos/{semana}_simsimsimnaosim.jpeg"
            )

        # Paste the circular image onto the background
        background.paste(circular_image, (20, 80), circular_image)

        # Set font
        font_path = (
            r"Recoleta-RegularDEMO.otf"  # Replace with the correct path to the font
        )
        font_size = 60  # Adjust the size as needed
        font = ImageFont.truetype(font_path, font_size)

        # Calculate text width and position for the name (top-right)
        draw = ImageDraw.Draw(background)
        bbox = draw.textbbox((0, 0), nome, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = background.width - text_width - 20  # Top-right position
        text_y = 120  # Lower position for the name text
        background = ImageCreation().insert_text(
            background, nome, (text_x, text_y), font
        )

        # Insert additional texts below the name
        text_1 = f"{total_palavras} palavras escritas"
        if atividades_feitas > 0:
            if atividades_feitas == 1:
                text_2 = "1 desafio completo"
            else:
                text_2 = f"{atividades_feitas} desafios completos"

        # Adjust font size for the additional texts
        font_size_small = 40
        font_small = ImageCreation().get_font(font_path, font_size_small)

        # Calculate positions for the additional texts
        text_1_bbox = draw.textbbox((0, 0), text_1, font=font_small)
        if atividades_feitas > 0:
            text_2_bbox = draw.textbbox((0, 0), text_2, font=font_small)

        text_1_width = text_1_bbox[2] - text_1_bbox[0]
        if atividades_feitas > 0:
            text_2_width = text_2_bbox[2] - text_2_bbox[0]

        # Insert additional text below the name
        background = ImageCreation().insert_text(
            background,
            text_1,
            (background.width - text_1_width - 20, text_y + 70),
            font_small,
        )
        if atividades_feitas > 0:
            background = ImageCreation().insert_text(
                background,
                text_2,
                (background.width - text_2_width - 20, text_y + 110),
                font_small,
            )

        # Convert the image to RGB mode before saving as JPEG
        background = background.convert("RGB")

        # Save the final image
        output_path = rf"{semana}/{nome}.jpeg"
        background.save(output_path, format="JPEG")
        # print(f"Image saved for {nome}: {output_path}")

    except Exception as err:
        print(nome, err)
