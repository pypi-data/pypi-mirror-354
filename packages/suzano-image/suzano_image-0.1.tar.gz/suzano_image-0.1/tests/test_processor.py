from suzano_image import processor

def test_redimensionar():
    img = processor.carregar_imagem("tests/exemplo.jpg")
    img_redim = processor.redimensionar(img, 100, 100)
    assert img_redim.shape[0] == 100
    assert img_redim.shape[1] == 100
