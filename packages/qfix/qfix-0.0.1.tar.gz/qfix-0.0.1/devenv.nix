{ ... }: {
  # To configure these options use `devenv.local.nix`: https://devenv.sh/files-and-variables/#devenvlocalnix
  # e.g.:
  # {
  #   guppy-integration.build-eldarion.enable = true;
  # }

  languages.python = {
    enable = true;
    venv.enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
  };
}
