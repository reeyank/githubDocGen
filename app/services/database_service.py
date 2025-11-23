from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rich.console import Console
import certifi

console = Console()

class MongoDBService:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri, tlsCAFile=certifi.where())
            # The ping command is cheap and does not require auth. It will confirm connection.
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            console.log(f"[green]Successfully connected to MongoDB Atlas database: {self.db_name}[/green]")
            return True
        except ConnectionFailure as e:
            console.log(f"[red]MongoDB Atlas connection failed: {e}[/red]")
            self.client = None
            self.db = None
            return False
        except Exception as e:
            console.log(f"[red]An unexpected error occurred during MongoDB connection: {e}[/red]")
            self.client = None
            self.db = None
            return False

    def disconnect(self):
        if self.client:
            self.client.close()
            console.log("[yellow]Disconnected from MongoDB Atlas.[/yellow]")
            self.client = None
            self.db = None

    def get_collection(self, collection_name: str):
        if self.db is None:
            console.log("[red]Not connected to MongoDB Atlas. Please call connect() first.[/red]")
            return None
        return self.db[collection_name]

    def insert_one(self, collection_name: str, document: dict):
        collection = self.get_collection(collection_name)
        if collection:
            result = collection.insert_one(document)
            console.log(f"[green]Inserted document with ID: {result.inserted_id}[/green]")
            return result.inserted_id
        return None

    def find_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        if collection:
            return collection.find_one(query)
        return None

    def update_one(self, collection_name: str, query: dict, new_values: dict):
        collection = self.get_collection(collection_name)
        if collection:
            result = collection.update_one(query, {'$set': new_values})
            console.log(f"[green]Matched {result.matched_count} documents and modified {result.modified_count}.[/green]")
            return result.modified_count
        return None

    def delete_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        if collection:
            result = collection.delete_one(query)
            console.log(f"[green]Deleted {result.deleted_count} documents.[/green]")
            return result.deleted_count
        return None

    def create_vector_index(self, collection_name: str, index_name: str, embedding_field: str, dimensions: int, metric: str = "cosine"):
        console.log(f"[yellow]Placeholder: To create a vector index '{index_name}' on collection '{collection_name}', field '{embedding_field}', with {dimensions} dimensions and metric '{metric}'. This should be done directly in MongoDB Atlas or via the Atlas API.[/yellow]")
        # In a real application, you would use MongoDB Atlas API to create the index programmatically.
        # Example of how to define an index (not executable code):
        # {
        #     "fields": [
        #         {
        #             "numDimensions": dimensions,
        #             "path": embedding_field,
        #             "similarity": metric,
        #             "type": "vector"
        #         }
        #     ]
        # }

    def vector_search(self, collection_name: str, query_vector: list[float], index_name: str, limit: int = 10):
        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": index_name,
                        "path": "embedding",  # Assuming the embedding field is named 'embedding'
                        "queryVector": query_vector,
                        "numCandidates": limit * 10,  # Search more candidates for better recall
                        "limit": limit
                    }
                },
                {
                    "$project": {
                        "_id": 0,  # Exclude the _id field
                        "embedding": 0, # Exclude the embedding field from results
                        "score": { "$meta": "vectorSearchScore" }
                    }
                }
            ]
            results = list(collection.aggregate(pipeline))
            console.log(f"[green]Performed vector search on '{collection_name}' with index '{index_name}'. Found {len(results)} results.[/green]")
            return results
        except Exception as e:
            console.log(f"[red]Error during vector search: {e}[/red]")
            return []

if __name__ == "__main__":
    # Example Usage (replace with your actual MongoDB Atlas URI and database name)
    # It's recommended to use environment variables for connection strings in a real application
    MONGO_URI = "mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority"
    DB_NAME = "doc_generator_db"
    COLLECTION_NAME = "analysis_results"

    db_service = MongoDBService(MONGO_URI, DB_NAME)
    if db_service.connect():
        # Insert example data
        example_doc = {"repo_url": "https://github.com/test/repo", "analysis": {"language": "Python"}}
        db_service.insert_one(COLLECTION_NAME, example_doc)

        # Find example data
        found_doc = db_service.find_one(COLLECTION_NAME, {"repo_url": "https://github.com/test/repo"})
        if found_doc:
            console.log(f"[blue]Found document: {found_doc}[/blue]")
        
        # Update example data
        db_service.update_one(COLLECTION_NAME, {"repo_url": "https://github.com/test/repo"}, {"analysis.language": "Python3"})

        # Delete example data
        db_service.delete_one(COLLECTION_NAME, {"repo_url": "https://github.com/test/repo"})

        db_service.disconnect()
