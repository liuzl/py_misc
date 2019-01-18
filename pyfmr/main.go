package main

import (
	"C"
	"fmt"

	"github.com/liuzl/fmr"
)

var g *fmr.Grammar

//export Hello
func Hello(n string) {
	fmt.Println("hello, ", n)
}

//export InitGrammar
func InitGrammar(f string) {
	var err error
	g, err = fmr.GrammarFromFile("sf.grammar")
	if err != nil {
		fmt.Println(f, " ", err.Error())
		panic(err)
	}
	fmt.Printf("grammar file loaded from %s\n", f)
}

//export Extract
func Extract(line, start string) []string {
	line = "直辖市：北京、上海、天津"
	start = "cities"
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
	if g == nil {
		fmt.Println("g is nil")
	}
}
