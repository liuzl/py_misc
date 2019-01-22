package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"fmt"
	"unsafe"

	"github.com/liuzl/fmr"
)

var g *fmr.Grammar

//export init_grammar
func init_grammar(s *C.char) {
	f := C.GoString(s)
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
	line := C.GoString(l)
	start := C.GoString(s)
	trees, err := g.ExtractMaxAll(line, start)
	if err != nil {
		return C.CString(err.Error())
	}
	for _, tree := range trees {
		sem, err := tree.Semantic()
		if err != nil {
			return C.CString(err.Error())
		} else {
			// return the first one
			return C.CString(sem)
		}
	}
	return C.CString("no result")
}

//export gofree
func gofree(cs *C.char) {
	C.free(unsafe.Pointer(cs))
}

func main() {
}
