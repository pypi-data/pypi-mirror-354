dict_of_images = {
    "https://github.com/kamangir/assets/blob/main/bluer-ugv/bluer-light.png?raw=true": "",
    "../../diagrams/bluer-swallow/3d-design.png": "../../diagrams/bluer-swallow/3d-design.stl",
    "https://github.com/kamangir/assets2/blob/main/bluer-swallow/20250605_180136.jpg?raw=true": "",
    "https://github.com/kamangir/assets2/blob/main/bluer-swallow/20250608_144453.jpg?raw=true": "",
    "https://github.com/kamangir/assets2/blob/main/bluer-swallow/20250609_164433.jpg?raw=true": "",
}

items = [
    "[![image]({})]({})".format(image, url if url else image)
    for image, url in dict_of_images.items()
]
