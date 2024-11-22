with import <nixpkgs> {};
mkShell {
    buildInputs = [ gcc python3 sage ];
}
