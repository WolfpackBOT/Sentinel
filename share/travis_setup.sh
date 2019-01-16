#!/bin/bash
set -evx

mkdir ~/.wolfcoin

# safety check
if [ ! -f ~/.wolfcoin/.energi.conf ]; then
  cp share/wolfcoin.conf.example ~/.wolfcoin/dash.conf
fi
