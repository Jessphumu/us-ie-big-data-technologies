from pymongo import MongoClient

# Connect to the local MongoDB container
client = MongoClient("mongodb://localhost:27017/")
db = client["quality_assurance"]
collection = db["qc_certificates"]

# 1. Create the compound index to eliminate unindexed document scans
collection.create_index([("supplier", 1), ("inspection_metrics.defect_flag", 1)])
print("Compound index created.")

# 2. Execute the multi-stage aggregation pipeline
pipeline = [
    {
        "$group": {
            "_id": {
                "supplier": "$supplier",
                "heat_number": "$heat_number"
            },
            "total_inspections": {"$sum": 1},
            "total_defects": {"$sum": "$inspection_metrics.defect_flag"},
            "mean_tolerance_dev": {"$avg": "$inspection_metrics.tolerance_dev"}
        }
    },
    {
        "$project": {
            "supplier": "$_id.supplier",
            "heat_number": "$_id.heat_number",
            "defect_rate": {"$divide": ["$total_defects", "$total_inspections"]},
            "mean_tolerance_dev": 1,
            "_id": 0
        }
    },
    {"$sort": {"defect_rate": -1}},
    {"$limit": 1}
]

print("Executing aggregation to find elevated defect rates...")
results = collection.aggregate(pipeline)
for result in results:
    print(result)c
