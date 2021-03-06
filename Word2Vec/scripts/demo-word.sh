# ========================================================
#   Copyright (C) 2016 All rights reserved.
#   
#   filename : structureTest_OneDocTesting.py
#   author   : Google Inc.
#   feat     : okcd00 / chendian@baidu.com
#   date     : 2016-05-07
#   desc     : Select Input & Output by Shell
# ======================================================== 

DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src

TEXT_DATA=$DATA_DIR/CDCorpus
VECTOR_DATA=$DATA_DIR/CDVectors

pushd ${SRC_DIR} && make; popd

if [ ! -e $VECTOR_DATA ]; then
  
  if [ ! -e $TEXT_DATA ]; then
    wget http://mattmahoney.net/dc/text8.zip -O $DATA_DIR/text8.gz
    gzip -d $DATA_DIR/text8.gz -f
  fi
  echo -----------------------------------------------------------------------------------------------------
  echo -- Training vectors...
  time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 0
  
fi

echo -----------------------------------------------------------------------------------------------------
echo -- distance...

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA
