import argparse
from generator import Generator
from sorter import Sorter
import time


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()

    generator_parser = subs.add_parser('generate', description='Generates random file with N rows')
    generator_parser.set_defaults(method='generate')
    generator_parser.add_argument('--num-rows', required=True, type=int, help='Sets num of rows in file to generate')
    generator_parser.add_argument('--max-len', required=True, type=int, help='Sets max len of row to generate')
    generator_parser.add_argument('--output-file', required=True, type=str, help='Sets path to the output-file')

    sorter_parser = subs.add_parser('sort', description='Sorts input-file and saves result to output-file')
    sorter_parser.set_defaults(method='sort')
    sorter_parser.add_argument('--input-file', required=True, type=str, help='Sets path to the input-file')
    sorter_parser.add_argument('--output-file', required=True, type=str, help='Sets path to the output-file')
    sorter_parser.add_argument('--memory', required=True, type=int, help='Helps to find out available memory')

    args = parser.parse_args()

    if args.method == "generate":
        Generator(num_rows=args.num_rows, max_len=args.max_len, output_file=args.output_file).generate()
    elif args.method == "sort":

        start_time = time.time()
        Sorter(input_file=args.input_file, output_file=args.output_file, memory=args.memory).sort()
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
