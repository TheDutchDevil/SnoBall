import csv

idmap = {}
clustermap = {}

with open('clusters.csv') as clusters:
    clusterreader = csv.DictReader(clusters, delimiter=',', quotechar='|')

    for row in clusterreader:
        if row["Cluster ID"] in clustermap:
            idmap[row["id"]] = clustermap[row["Cluster ID"]]
        else:
            clustermap[row["Cluster ID"]] = row["id"]
            idmap[row["id"]] = row["id"]


    print("Done reading clusters")

with open("paper_authors.csv") as paperauthors:
    with open("new_paper_authors.csv", 'w+') as newfile:
        paperauthorsreader = csv.DictReader(paperauthors, delimiter=",")
        writer = csv.DictWriter(newfile, fieldnames=["paper_id","author_id"])

        writer.writeheader()

        for row in paperauthorsreader:
            writer.writerow({"paper_id": row["paper_id"], "author_id": idmap[row["author_id"]]})

        newfile.flush()