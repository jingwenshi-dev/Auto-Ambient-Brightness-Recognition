# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    opencv4
    pyqt6
    gnureadline
    debugpy
    
    (
      buildPythonPackage rec {
        pname = "screen_brightness_control";
        version = "0.20.0";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-icBFAD0lTsuKY7LP5HOuLb10v5337A9b+WANBzLxNu0=";
        };
        doCheck = false;
      }
    )
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
