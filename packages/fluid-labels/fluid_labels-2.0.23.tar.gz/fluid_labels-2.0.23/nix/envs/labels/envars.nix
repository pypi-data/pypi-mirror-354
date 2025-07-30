{ pkgs, projectPath }:
let treeSitter = pkgs.callPackage ./tree-sitter.nix { };
in pkgs.writeShellApplication {
  bashOptions = [ ];
  name = "labels-envars";
  text = ''
    export BUGSNAG_API_KEY="82c9f090e2049a63c44a2045b029a7a8"
    export TREE_SITTER_PARSERS_DIR="${treeSitter}"
  '';
}
