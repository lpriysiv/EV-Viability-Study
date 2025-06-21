from scripts import charging_stations_cluster
from scripts import evs_by_category
from scripts import ev_trends


def main():
    charging_stations_cluster.run()
    evs_by_category.run()
    ev_trends.run()

if __name__ == "__main__":
    main()