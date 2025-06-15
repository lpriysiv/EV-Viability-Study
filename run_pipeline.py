import scripts.fetch as fetch
import scripts.preprocess as preprocess
import scripts.model as model
import scripts.visualize as visualize

def main():
    raw_data = fetch.run()
    clean_data = preprocess.run(raw_data)
    results = model.run(clean_data)
    visualize.run(clean_data, results)

if __name__ == "__main__":
    main()