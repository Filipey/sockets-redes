import os
import sys


def main(argv = None):
  
  init = lambda service: os.system(f"python3 {service}.py")
  init_subprocess = lambda service: os.system(f"gnome-terminal -- python3 {service}.py ")

  if argv == '--logs':
    init_subprocess("server")
    init_subprocess("client")
  else:
    init("server")
    init("client")
    # inicializar GUI

if __name__ == "__main__":

  if len(sys.argv) > 1:
    main(sys.argv[1])
  else:
    main()
