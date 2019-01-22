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
		cs := C.CString(err.Error())
		C.free(unsafe.Pointer(cs))
		return cs
	}
	for _, tree := range trees {
		sem, err := tree.Semantic()
		if err != nil {
			cs := C.CString(err.Error())
			C.free(unsafe.Pointer(cs))
			return cs
		} else {
			// return the first one
			cs := C.CString(sem)
			C.free(unsafe.Pointer(cs))
			return cs
		}
	}
	cs := C.CString("no result")
	C.free(unsafe.Pointer(cs))
	return cs
}

func main() {
}
