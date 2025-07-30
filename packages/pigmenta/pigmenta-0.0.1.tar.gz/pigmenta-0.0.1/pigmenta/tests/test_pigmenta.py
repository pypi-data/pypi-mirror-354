

class TestPigmenta:
    def test_palettes(self):
        from pigmenta import PALETTES
        assert isinstance(PALETTES, object)

    def test_colors_type(self):
        from pigmenta import PALETTES
        assert isinstance(PALETTES.coffee, list)

    def test_colors_hex(self):
        from pigmenta import PALETTES
        assert isinstance(PALETTES.coffee[0], str)
        assert PALETTES.coffee[0].startswith("#")
