from scripts import charging_stations_cluster, ev_registrations_by_region, evs_by_category, ev_trends
from util import merge_regional_registrations


def main():
    charging_stations_cluster.run()
    evs_by_category.run()
    ev_trends.run()
    # Merge regional registrations data
    #merge_regional_registrations.run()
    ev_registrations_by_region.run()
    print("All scripts executed successfully.")


if __name__ == "__main__":
    main()