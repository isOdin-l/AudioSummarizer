{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.poetry
    pkgs.python3Packages.pip  # если понадобится редкий пакет
  ];
}