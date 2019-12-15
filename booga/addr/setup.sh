if [ ! -f 2018_addr.tsv.gz ];
then
    wget https://github.com/liuzl/china-address-code/raw/master/2018_addr.tsv.gz
fi

if [ ! -f 2018_addr_dict.txt.gz ];
then
    python addrname.py 2018_addr.tsv.gz > 2018_addr_dict.txt
    gzip 2018_addr_dict.txt
fi

if [ ! -d addrdb ];
then
    python to_dict.py 2018_addr_dict.txt.gz
fi
