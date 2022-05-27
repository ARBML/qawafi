#!/bin/bash
cd /content/shakkelha;
python predict.py --input-file-path /content/qawafi/demo/baits_input.txt \
                  --model-type rnn \
                  --model-number 3 \
                  --model-size big \
                  --model-average 20 \
                  --output-file-path /content/qawafi/demo/baits_output.txt;
cd -;