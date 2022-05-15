import cli
import test



def main():
	args = cli.get_args()
	test.run_environment(args)
	

if __name__ == '__main__':
	main()

