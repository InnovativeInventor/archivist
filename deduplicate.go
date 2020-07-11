package main

import (
    "fmt"
	"log"
	"bufio"
	"encoding/json"
	"io/ioutil"
	"os"
	"github.com/willf/bloom"
	"strings"
)

func main() {
	var bloomfilter bloom.BloomFilter

	file, _ := ioutil.ReadFile("bloom.json")
	err := json.Unmarshal(file, &bloomfilter)
	if err != nil {
		log.Fatal(err.Error())
	}

	if bloomfilter.TestString("test") && ! bloomfilter.TestString("nulltest"){
		log.Println("Ok! Loaded bloom filter properly")
	} else {
		log.Fatal("Bloom filter not loaded properly")
	}

	filename := "items.txt"
	file_items, err := os.Open(filename)
	if err != nil {
		log.Println(err)
		file_items.Close()
	}
	defer file_items.Close()

	scanner := bufio.NewScanner(file_items)
	buf := make([]byte, 0, 64*1024)
	scanner.Buffer(buf, 2048*1024)
	for scanner.Scan() {
		url := scanner.Text()
		if ! bloomfilter.TestAndAddString(strings.TrimSpace(url)) {
			fmt.Println(url)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Println(err)
	}
}

