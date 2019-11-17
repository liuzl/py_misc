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

## 参考资料

* [KenLM: Faster and Smaller Language Model Queries](https://github.com/kpu/kenlm)
