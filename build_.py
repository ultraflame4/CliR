import skbuild

def build(setup_kwargs):
    print("BUILDING C EXTENSIONS!")
    skbuild.setup(
        **setup_kwargs,
        script_args=["build_ext"],
        cmake_source_dir= "ext"
    )


if __name__ == "__main__":
    build({})