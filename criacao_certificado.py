import numpy as np
import pandas as pd
from classes.class_image_creation import ImageCreation
from PIL import ImageDraw, ImageFont

alunos = pd.read_excel("alunos.xlsx")[["Nome completo\n"]]
alunos["Nome completo\n"] = alunos["Nome completo\n"].str.strip()
alunos["Nome completo\n"] = np.where(
    alunos["Nome completo\n"] == "Jonnie Dantas (Fernanda Borges P da Silva)",
    "Fernanda Borges P da Silva",
    alunos["Nome completo\n"],
)
nomes = alunos["Nome completo\n"].tolist()

for nome in nomes:
    nome_sem_espaco = nome.replace(" ", "")

    background = ImageCreation().get_background(r"fundos/certificado.jpg")
    font_path = r"kingred.otf"
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(background)
    bbox = draw.textbbox((0, 0), nome, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = 160
    text_y = 700
    background = ImageCreation().insert_text(
        background, nome, (text_x, text_y), font, color="black"
    )

    background = background.convert("RGB")
    output_path = rf"certificados/{nome_sem_espaco}.jpeg"
    background.save(output_path, format="JPEG")
