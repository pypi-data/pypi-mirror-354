import os

import tree_sitter

GRAMMARS: dict[str, str] = {
    # Grammars required because not available on pypi as of 12/24
    "swift": os.environ["grammarSwift"],
}


def main() -> None:
    out: str = os.environ["out"]
    os.makedirs(out)

    for grammar, src in GRAMMARS.items():
        path = os.path.join(out, f"{grammar}.so")
        tree_sitter.Language.build_library(path, [src])


if __name__ == "__main__":
    main()
