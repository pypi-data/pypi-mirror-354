{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSEnv {
  name = "pipzone";
  targetPkgs = pkgs: (with pkgs; [
    python313
    python313Packages.pip
    python313Packages.virtualenv
    libgcc
    gcc14
  ]);
  runScript = "bash --init-file /etc/profile";
}).env