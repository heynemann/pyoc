from test_resolve_with_file_config import E, F

def config(container):
    container.register("e", E)
    container.register("f", F)
    container.register("title", "Test Title")