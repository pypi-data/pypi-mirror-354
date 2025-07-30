from dynamic_prompt_importer import DynamicPromptImporter as DPI


dpi = DPI(
    "",
    token="",
    preload=True,
)

print(dpi.get_file_content(""))
