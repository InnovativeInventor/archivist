package main

import (
    "fmt"
    "path/filepath"
	"log"
	"bufio"
	"os"
	"github.com/willf/bloom"
)

func main() {
	fileglob := "/Volumes/Cabinet/archivebot/*/*.*"
	files, err := filepath.Glob(fileglob)
    if err != nil {
        log.Fatal(err)
    }

	bloomfilter := bloom.NewWithEstimates(400000000, 0.0001)

	count := 0

	for _, filename := range files {
		file, err := os.Open(filename)
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
			bloomfilter.AddString(scanner.Text())
			count += 1
		}

		if err := scanner.Err(); err != nil {
			log.Println(err)
			continue
		}

		file.Close()
    }

	log.Println("Successfully added the following number of items to the bloom filter:")
	log.Println(count)

	filename := "items.txt"
	file, err := os.Open(filename)
	if err != nil {
		log.Println(err)
		file.Close()
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	buf := make([]byte, 0, 64*1024)
	scanner.Buffer(buf, 2048*1024)
	for scanner.Scan() {
		url := scanner.Text()
		if ! bloomfilter.TestAndAddString(url) {
			fmt.Println(url)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Println(err)
	}
}

