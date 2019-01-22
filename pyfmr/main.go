package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"fmt"
	"sync"
	"unsafe"

	"github.com/liuzl/fmr"
)

var (
	index    = make(map[string]int)
	mutex    sync.RWMutex
	grammars []*fmr.Grammar
	g        *fmr.Grammar
)

//export init_grammar
func init_grammar(s *C.char) int {
	f := C.GoString(s)
	mutex.RLock()
	defer mutex.RUnlock()
	if i, has := index[f]; has {
		g = grammars[i]
		return i
	}

	i := len(grammars)

	var err error
	g, err = fmr.GrammarFromFile(f)
	if err != nil {
		fmt.Println(f, " ", err.Error())
		panic(err)
	}
	grammars = append(grammars, g)
	index[f] = i
	//fmt.Printf("grammar file loaded from %s\n", f)
	return i
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

//export extractx
func extractx(i int, l, s *C.char) *C.char {
	if i < 0 || i >= len(grammars) {
		return C.CString("no grammar")
	}
	lg := grammars[i]
	line := C.GoString(l)
	start := C.GoString(s)
	trees, err := lg.ExtractMaxAll(line, start)
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
