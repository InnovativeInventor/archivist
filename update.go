package main

import (
	"bufio"
	"encoding/json"
	"github.com/willf/bloom"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	var size uint
	var probability float64
	var bloomfilter bloom.BloomFilter

	size = 1
	probability = 100000

	size = size * 1000000000
	probability = 1/probability


	if len(os.Args) == 2 {
		log.Println("Created bloom filter with size", size, "probability", probability)
		bloomfilter = *bloom.NewWithEstimates(size, probability)
		/*bloomfilter = *bloom.NewWithEstimates(400000000, 0.0001)*/
	} else {
		file, _ := ioutil.ReadFile("bloom.json")
		err := json.Unmarshal(file, &bloomfilter)
		if err != nil {
			log.Fatal(err.Error())
		}
		if bloomfilter.TestString("test") {
			log.Println("Ok! Loaded bloom filter properly")
		} else {
			log.Fatal("Bloom filter not loaded properly")
		}
	}

	bloomfilter = add(bloomfilter)

	save(bloomfilter)

}

func save(bloomfilter bloom.BloomFilter) {
	data, err := json.Marshal(&bloomfilter)
	if err != nil {
		log.Fatal(err.Error())
	}
	ioutil.WriteFile("bloom.json", data, os.ModePerm)
}

func add(bloomfilter bloom.BloomFilter) bloom.BloomFilter {
	fileglob := "../../archivebot/*.txt"

	files, err := filepath.Glob(fileglob)
	if err != nil {
		log.Fatal(err)
	}

	count := 0
	for _, filename := range files {
		file, err := os.Open(filename)
		log.Println("Adding to bloom filter:", filename)
		if err != nil {
			log.Println(err)
			file.Close()
			continue
		}
		/*defer file.Close()*/

		scanner := bufio.NewScanner(file)
		buf := make([]byte, 0, 64*1024)
		scanner.Buffer(buf, 2048*1024)
		for scanner.Scan() {
			bloomfilter.AddString(strings.TrimSpace(scanner.Text()))
			count += 1
		}

		if err := scanner.Err(); err != nil {
			log.Println(err)
			continue
		}

		file.Close()
	}

	bloomfilter.AddString("test")
	log.Println("Successfully added the following number of items to the bloom filter:")
	log.Println(count)

	return bloomfilter
}
