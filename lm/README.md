# 语言模型

## 新词发现

### 安装编译kenlm

```sh
# Mac编译安装kenlm，依赖boost库
brew install boost
git clone https://github.com/kpu/kenlm
cd kenlm
mkdir build
cd build
cmake ..
make -j 4
# ./bin/count_ngrams
```

### 下载THUCNews中文文本数据集

* http://thuctc.thunlp.org/
* [download](https://thunlp.oss-cn-qingdao.aliyuncs.com/THUCNews.zip)

### 执行word-discovery

```sh
git clone https://github.com/bojone/word-discovery
cd word-discovery
cp ../kenlm/build/bin/count_ngrams ./
# modify the path for THUCNews数据地址 in word_discovery.py
python2 word_discovery.py
```

## 参考资料

* [KenLM: Faster and Smaller Language Model Queries](https://github.com/kpu/kenlm)

