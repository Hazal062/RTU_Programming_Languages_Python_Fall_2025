// Name: Hazal Guc
// StudentID: 231ADB264
// Lab: Programming Languages - Lab 3

package main

import (
	"bufio"
	"container/heap"
	"errors"
	"flag"
	"fmt"
	"math"
	"math/rand"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	firstName = "Hazal"
	surname   = "Guc"
	studentID = "231ADB264"
)

func main() {
	rN := flag.Int("r", -1, "generate N random integers (N >= 10)")
	inFile := flag.String("i", "", "read integers from input file")
	inDir := flag.String("d", "", "process directory containing .txt files")

	flag.Parse()

	modes := 0
	if *rN != -1 {
		modes++
	}
	if *inFile != "" {
		modes++
	}
	if *inDir != "" {
		modes++
	}
	if modes != 1 {
		exitErr("Use exactly one mode: -r N OR -i file OR -d dir")
	}

	if *rN != -1 {
		if err := modeRandom(*rN); err != nil {
			exitErr(err.Error())
		}
		return
	}

	if *inFile != "" {
		if err := modeFile(*inFile); err != nil {
			exitErr(err.Error())
		}
		return
	}

	if *inDir != "" {
		if err := modeDirectory(*inDir); err != nil {
			exitErr(err.Error())
		}
		return
	}
}

func modeRandom(n int) error {
	if n < 10 {
		return errors.New("N must be >= 10")
	}

	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	nums := make([]int, n)
	for i := 0; i < n; i++ {
		nums[i] = rng.Intn(2001) - 1000
	}

	return sortPipelineAndPrint(nums)
}

func modeFile(path string) error {
	nums, err := readIntsFromFile(path)
	if err != nil {
		return err
	}
	if len(nums) < 10 {
		return errors.New("Fewer than 10 valid numbers in file")
	}
	return sortPipelineAndPrint(nums)
}

func modeDirectory(dir string) error {
	info, err := os.Stat(dir)
	if err != nil {
		return fmt.Errorf("Directory not found: %s", dir)
	}
	if !info.IsDir() {
		return fmt.Errorf("Not a directory: %s", dir)
	}

	parent := filepath.Dir(filepath.Clean(dir))
	base := filepath.Base(filepath.Clean(dir))
	outDirName := fmt.Sprintf("%s_sorted_%s_%s_%s", base, strings.ToLower(firstName), strings.ToLower(surname), studentID)
	outDir := filepath.Join(parent, outDirName)

	if err := os.MkdirAll(outDir, 0o755); err != nil {
		return fmt.Errorf("Cannot create output directory: %s", outDir)
	}

	entries, err := os.ReadDir(dir)
	if err != nil {
		return fmt.Errorf("Cannot read directory: %s", dir)
	}

	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		if filepath.Ext(e.Name()) != ".txt" {
			continue
		}

		inPath := filepath.Join(dir, e.Name())
		nums, err := readIntsFromFile(inPath)
		if err != nil {
			return fmt.Errorf("%s: %v", e.Name(), err)
		}
		if len(nums) < 10 {
			return fmt.Errorf("%s: fewer than 10 valid numbers", e.Name())
		}

		sorted, err := concurrentChunkSort(nums)
		if err != nil {
			return fmt.Errorf("%s: %v", e.Name(), err)
		}

		outPath := filepath.Join(outDir, e.Name())
		if err := writeIntsOnePerLine(outPath, sorted); err != nil {
			return fmt.Errorf("%s: cannot write output: %v", e.Name(), err)
		}
	}

	return nil
}

func sortPipelineAndPrint(nums []int) error {
	n := len(nums)
	chunkCount := chunkCountFor(n)

	fmt.Printf("Original numbers:\n%v\n\n", nums)

	chunks := splitIntoChunks(copyInts(nums), chunkCount)

	fmt.Printf("Chunks before sorting:\n")
	printChunks(chunks)
	fmt.Println()

	sortedChunks := sortChunksConcurrently(chunks)

	fmt.Printf("Chunks after sorting:\n")
	printChunks(sortedChunks)
	fmt.Println()

	merged := mergeSortedChunks(sortedChunks)

	fmt.Printf("Final merged sorted result:\n%v\n", merged)
	return nil
}

func concurrentChunkSort(nums []int) ([]int, error) {
	chunkCount := chunkCountFor(len(nums))
	chunks := splitIntoChunks(copyInts(nums), chunkCount)
	sortedChunks := sortChunksConcurrently(chunks)
	return mergeSortedChunks(sortedChunks), nil
}

func chunkCountFor(n int) int {
	if n <= 0 {
		return 4
	}
	k := int(math.Ceil(math.Sqrt(float64(n))))
	if k < 4 {
		k = 4
	}
	if k > n {
		k = n
	}
	if k < 1 {
		k = 1
	}
	return k
}

func splitIntoChunks(nums []int, k int) [][]int {
	n := len(nums)
	if k <= 0 {
		k = 1
	}
	if k > n && n > 0 {
		k = n
	}
	chunks := make([][]int, 0, k)

	base := 0
	if k > 0 {
		base = n / k
	}
	rem := 0
	if k > 0 {
		rem = n % k
	}

	start := 0
	for i := 0; i < k; i++ {
		size := base
		if i < rem {
			size++
		}
		end := start + size
		if end > n {
			end = n
		}
		chunks = append(chunks, nums[start:end])
		start = end
	}
	return chunks
}

func sortChunksConcurrently(chunks [][]int) [][]int {
	var wg sync.WaitGroup
	wg.Add(len(chunks))

	for i := range chunks {
		i := i
		go func() {
			sort.Ints(chunks[i])
			wg.Done()
		}()
	}

	wg.Wait()
	return chunks
}

func mergeSortedChunks(chunks [][]int) []int {
	total := 0
	for _, c := range chunks {
		total += len(c)
	}
	out := make([]int, 0, total)

	h := &minHeap{}
	heap.Init(h)

	for i, c := range chunks {
		if len(c) == 0 {
			continue
		}
		heap.Push(h, heapItem{val: c[0], chunk: i, idx: 0})
	}

	for h.Len() > 0 {
		it := heap.Pop(h).(heapItem)
		out = append(out, it.val)

		nextIdx := it.idx + 1
		if nextIdx < len(chunks[it.chunk]) {
			heap.Push(h, heapItem{val: chunks[it.chunk][nextIdx], chunk: it.chunk, idx: nextIdx})
		}
	}

	return out
}

type heapItem struct {
	val   int
	chunk int
	idx   int
}

type minHeap []heapItem

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i].val < h[j].val }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)        { *h = append(*h, x.(heapItem)) }
func (h *minHeap) Pop() any          { old := *h; n := len(old); x := old[n-1]; *h = old[:n-1]; return x }

func readIntsFromFile(path string) ([]int, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("File not found: %s", path)
	}
	defer f.Close()

	var nums []int
	sc := bufio.NewScanner(f)
	lineNo := 0
	for sc.Scan() {
		lineNo++
		s := strings.TrimSpace(sc.Text())
		if s == "" {
			continue
		}
		v, err := strconv.Atoi(s)
		if err != nil {
			return nil, fmt.Errorf("Invalid integer on line %d", lineNo)
		}
		nums = append(nums, v)
	}
	if err := sc.Err(); err != nil {
		return nil, fmt.Errorf("Cannot read file: %s", path)
	}
	return nums, nil
}

func writeIntsOnePerLine(path string, nums []int) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	for _, v := range nums {
		if _, err := fmt.Fprintf(w, "%d\n", v); err != nil {
			return err
		}
	}
	return w.Flush()
}

func printChunks(chunks [][]int) {
	for i, c := range chunks {
		fmt.Printf("Chunk %d: %v\n", i+1, c)
	}
}

func copyInts(a []int) []int {
	b := make([]int, len(a))
	copy(b, a)
	return b
}

func exitErr(msg string) {
	fmt.Fprintln(os.Stderr, msg)
	os.Exit(1)
}
