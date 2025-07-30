from dynamic_file_importer import DynamicFileImporter as DPI


dpi = DPI(
    "",
    token="",
    preload=True,
)

print(dpi.get_file_content(""))
