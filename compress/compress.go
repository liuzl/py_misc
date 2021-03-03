package main

import (
	"bytes"
	"compress/zlib"
	"encoding/base64"
	"fmt"
	"io"
)

func encode(content string) string {
	src := []byte(content)
	var in bytes.Buffer
	w := zlib.NewWriter(&in)
	w.Write(src)
	w.Close()
	return base64.StdEncoding.EncodeToString(in.Bytes())
}

func decode(s string) string {
	data, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		return ""
	}
	var out bytes.Buffer
	r, _ := zlib.NewReader(bytes.NewReader(data))
	io.Copy(&out, r)
	return out.String()
}

func main() {
	s := "123123123"
	content := ""
	for i := 0; i < 100; i++ {
		content += s
	}
	fmt.Println(content)
	fmt.Println(decode(encode(content)))
	fmt.Println(decode("eJwzNDI2HEWjaBQNHAIAaLuvyQ=="))
}
