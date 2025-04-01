{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        venv-dir = "fooocus_env";
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # For more packages/package search go to https://search.nixos.org/
            python310 # Adjust Python version as needed
            python310Packages.pip
            python310Packages.virtualenv
            pkg-config
            stdenv.cc.cc.lib
            cudatoolkit
            cudaPackages.cudnn
            cudaPackages.cuda_cudart
            gcc13
            zlib
          ];

          shellHook = ''
            export CUDA_PATH=${pkgs.cudatoolkit}
            export CC=${pkgs.gcc13}/bin/gcc
            export CXX=${pkgs.gcc13}/bin/g++
            export PATH=${pkgs.gcc13}/bin:$PATH

            export LD_LIBRARY_PATH=${
              pkgs.lib.makeLibraryPath [
                "/run/opengl-driver"
                pkgs.cudatoolkit
                pkgs.cudaPackages.cudnn
                pkgs.stdenv.cc.cc
              ]
            }:$LD_LIBRARY_PATH


            export LIBRARY_PATH=${
              pkgs.lib.makeLibraryPath [ pkgs.cudatoolkit ]
            }:$LIBRARY_PATH

            if [ ! -d ${venv-dir} ]; then
            echo "Creating virtual environment..."
              python3 -m venv ${venv-dir}
            fi

            echo "Activating virtual environment..."
            source ${venv-dir}/bin/activate
            pip install -r ./requirements_versions.txt
          '';
        };
      });
}
