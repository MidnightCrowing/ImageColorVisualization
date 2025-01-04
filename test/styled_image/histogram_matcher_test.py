from src.styled_image import HistogramMatcher

matcher = HistogramMatcher(temp_dir=r"result")
matcher.script(r"..\images\content.png", r"..\images\style.png")
