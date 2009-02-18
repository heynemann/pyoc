from test_resolve_with_file_config import B, C

def config(container):
    container.register("b", B)
    container.register("c", C)
    container.register("title", "any other title")