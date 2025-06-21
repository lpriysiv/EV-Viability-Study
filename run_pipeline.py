from scripts import charging_stations_cluster
from scripts import evs_by_category


def main():
    charging_stations_cluster.run()
    evs_by_category.run()

if __name__ == "__main__":
    main()