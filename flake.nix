{
  description = "Base Flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs @ {flake-parts, ...}:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux" "aarch64-linux" "aarch64-darwin"];

      perSystem = {
        pkgs,
        system,
        ...
      }: let
        inherit (pkgs) mkShell;
      in {
        devShells = {
          default = mkShell {
            buildInputs = with pkgs; [
              python3
              pyright
              ruff
              python312Packages.pydantic
              python312Packages.pyyaml
            ];
          };
        };
      };
    };
}
