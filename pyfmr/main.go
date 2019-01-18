package main

import (
	"C"
	"github.com/liuzl/fmr"
)

func Sum(a, b int) int {
	return a + b
}

//export GrammarFromFile
func GrammarFromFile(f string) *fmr.Grammar {
	g, err := fmr.GrammarFromFile(f)
	if err != nil {
		panic(err)
	}
	return g
}

func Extract(g *fmr.Grammar, line, start string) []string {
	trees, err := g.ExtractMaxAll(line, start)
	if err != nil {
		return []string{err.Error()}
	}
	var ret []string
	for _, tree := range trees {
		sem, err := tree.Semantic()
		if err != nil {
			ret = append(ret, err.Error())
		} else {
			ret = append(ret, sem)
		}
	}
	return ret
}

func main() {
	GrammarFromFile("sf.grammar")
}
