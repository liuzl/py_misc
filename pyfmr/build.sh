#CC="clang" && CXX="clang++"
#echo $CC
go build -buildmode=c-shared -o fmr.so main.go
gcc -Wall -o main main.cc ./fmr.so
./main sf.grammar cities "直辖市：北京、上海、天津"
