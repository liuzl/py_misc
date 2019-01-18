package main

import (
	"C"
	"fmt"

	"github.com/liuzl/fmr"
)

var g *fmr.Grammar

//export init_grammar
func init_grammar(s *C.char) {
	f := C.GoString(s)
	fmt.Println(f)
	var err error
	g, err = fmr.GrammarFromFile(f)
	if err != nil {
		fmt.Println(f, " ", err.Error())
		panic(err)
	}
	fmt.Printf("grammar file loaded from %s\n", f)
}

//export extract
func extract(l, s *C.char) *C.char {
	//line = "直辖市：北京、上海、天津"
	//start = "cities"
	line := C.GoString(l)
	start := C.GoString(s)
	fmt.Println("extract")
	trees, err := g.ExtractMaxAll(line, start)
	if err != nil {
		fmt.Println(err.Error())
		return C.CString(err.Error())
	}
	for _, tree := range trees {
		sem, err := tree.Semantic()
		if err != nil {
			fmt.Println(err.Error())
			return C.CString(err.Error())
		} else {
			fmt.Println(sem)
			return C.CString(sem)
		}
	}
	return C.CString("no result")
}

func main() {
}
