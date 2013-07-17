{ }:

let
    pkgs = import <nixpkgs> { };
in

with pkgs;

buildEnv {
  name = "deco-env";
  paths = [
    python27
    python27Packages.distribute
    python27Packages.recursivePthLoader
    python27Packages.virtualenv
    python27Packages.zc_buildout
    plone43Packages.pillow
    plone43Packages.lxml
    plone43Packages.python_dateutil
  ] ++ lib.attrValues python27.modules;
}
