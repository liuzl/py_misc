#CC="clang" && CXX="clang++"
#echo $CC
go build -buildmode=c-shared -o fmr.so main.go
