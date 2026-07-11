#!/usr/bin/env bash

[ -z "$1" ] && echo "Usage: ./install.sh INSTALL_DIR" && exit 1

BASE_DIR=$PWD
INSTALL_DIR=$1

if [ ! -f "gitadd.py" ]; then
  echo "[!] install.sh must be ran from the directory where gitadd.py exists"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "[+] Creating venv"
  python3 -m venv .venv

  echo "[+] Installing requirements"
  source .venv/bin/activate
  pip3 install -r requirements.txt
fi

echo "[+] Installing git-add to $INSTALL_DIR from $BASE_DIR"
echo "[!] Don't move $BASE_DIR around, because shortcut scripts created by install.sh will break"


cat << EOF > $INSTALL_DIR/gita
#!/usr/bin/env bash
source $BASE_DIR/.venv/bin/activate
python3 $BASE_DIR/gitadd.py
EOF

chmod +x $INSTALL_DIR/gita

echo "[+] Created 'gita', a shorthand for 'python3 gitadd.py'"


cat << EOF > $INSTALL_DIR/gitc
#!/usr/bin/env bash
source $BASE_DIR/.venv/bin/activate
python3 $BASE_DIR/gitadd.py --commit
EOF

chmod +x $INSTALL_DIR/gitc

echo "[+] Created 'gitc', a shorthand for 'python3 gitadd.py --commit'"


cat << EOF > $INSTALL_DIR/gitp
#!/usr/bin/env bash
source $BASE_DIR/.venv/bin/activate
python3 $BASE_DIR/gitadd.py --commit --push
EOF

chmod +x $INSTALL_DIR/gitp

echo "[+] Created 'gitp', a shorthand for 'python3 gitadd.py --commit --push'"


cat << EOF > $INSTALL_DIR/gitpu
#!/usr/bin/env bash
source $BASE_DIR/.venv/bin/activate
python3 $BASE_DIR/gitadd.py --commit --push --upstream
EOF

chmod +x $INSTALL_DIR/gitpu

echo "[+] Created 'gitpu', a shorthand for 'python3 gitadd.py --commit --push --upstream'"
