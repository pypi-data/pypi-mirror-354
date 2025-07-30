{ pkgs }:
let
  grammarSwift = builtins.fetchTarball {
    url =
      "https://github.com/alex-pinkus/tree-sitter-swift/archive/57c1c6d6ffa1c44b330182d41717e6fe37430704.tar.gz";
    sha256 = "sha256:18z9rlycls841qvjgs376kqnwds71sm6lbafgjk8pxfqa7w6gwqn";
  };
  patchedBin = pkgs.python311Packages.tree-sitter.overridePythonAttrs
    (oldAttrs: {
      src = pkgs.fetchFromGitHub {
        owner = "tree-sitter";
        repo = "py-tree-sitter";
        rev = "refs/tags/v0.21.1";
        sha256 = "sha256-U4ZdU0lxjZO/y0q20bG5CLKipnfpaxzV3AFR6fGS7m4=";
        fetchSubmodules = true;
      };

      dependencies = [ pkgs.python311Packages.setuptools ];
    });
in pkgs.stdenv.mkDerivation {
  buildPhase = ''
    export grammarSwift="${grammarSwift}"

    python tree-sitter.py
  '';
  name = "labels-tree-sitter-patch";
  nativeBuildInputs = [ patchedBin ];
  src = ./.;
}
