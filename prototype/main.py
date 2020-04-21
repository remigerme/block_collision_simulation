import simulation as simu
import loadconfig


def main():
	settings = loadconfig.get_config()
	simu.Simulation(settings).run()


if __name__ == "__main__":
	main()