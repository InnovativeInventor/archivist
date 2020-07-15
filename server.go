package main

import (
    "fmt"
	"log"
	/*"bufio"*/
	"encoding/json"
	"io/ioutil"
	/*"os"*/
	"github.com/willf/bloom"
	"github.com/go-martini/martini"
	"encoding/base64"
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
		fmt.Println("Ok! Loaded bloom filter properly")
	} else {
		log.Fatal("Bloom filter not loaded properly")
	}

	log.Println("Ready for reading input")
	fmt.Println("Ready for reading input")

	m := martini.Classic()

	m.Get("/:url", func(params martini.Params) []byte {
		url, err := base64.StdEncoding.DecodeString(params["url"])
		if err != nil {
			log.Fatal(err.Error())
		}
		if ! bloomfilter.TestAndAdd(url) {
			return url
		} else {
			return []byte("")
		}
	})
	m.Run()

	/*scanner := bufio.NewScanner(os.Stdin)*/
	/*buf := make([]byte, 0, 64*1024)*/
	/*scanner.Buffer(buf, 2048*1024)*/
	/*for scanner.Scan() {*/
		/*url := scanner.Text()*/
		/*if ! bloomfilter.TestAndAdd(strings.TrimSpace(url)) {*/
			/*fmt.Println(url)*/
		/*} else {*/
			/*fmt.Println("null")*/
		/*}*/
	/*}*/

	/*if err := scanner.Err(); err != nil {*/
		/*log.Println(err)*/
	/*}*/
}

