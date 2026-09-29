import time
import random

# This script simulates basic database operations and highlights potential optimization areas.
# It's a simplified representation, not a full-fledged database system.

class MockDatabase:
    def __init__(self, db_type):
        self.db_type = db_type
        self.data = {}
        self.indexes = {}
        print(f"Initializing {self.db_type} mock database...")

    def create_table(self, table_name):
        if table_name not in self.data:
            self.data[table_name] = []
            self.indexes[table_name] = {}
            print(f"Table '{table_name}' created.")
        else:
            print(f"Table '{table_name}' already exists.")

    def insert_row(self, table_name, row_data):
        if table_name in self.data:
            self.data[table_name].append(row_data)
            # Simulate index update (simplified)
            for key, value in row_data.items():
                if key in self.indexes[table_name]:
                    if value not in self.indexes[table_name][key]:
                        self.indexes[table_name][key][value] = []
                    self.indexes[table_name][key][value].append(len(self.data[table_name]) - 1)
            # print(f"Inserted into '{table_name}': {row_data}")
        else:
            print(f"Table '{table_name}' does not exist.")

    def query(self, table_name, query_params):
        if table_name not in self.data:
            print(f"Table '{table_name}' does not exist.")
            return []

        start_time = time.time()
        results = []

        # Simulate query execution with basic optimization (index lookup if available)
        if query_params and any(key in self.indexes[table_name] for key in query_params):
            # Use index if possible
            potential_row_indices = set(range(len(self.data[table_name])))
            for key, value in query_params.items():
                if key in self.indexes[table_name] and value in self.indexes[table_name][key]:
                    potential_row_indices.intersection_update(self.indexes[table_name][key][value])
                else:
                    potential_row_indices.clear() # No match for this indexed field
                    break

            for index in potential_row_indices:
                row = self.data[table_name][index]
                # Full check to ensure all query params match
                if all(row.get(k) == v for k, v in query_params.items()):
                    results.append(row)
        else:
            # Full table scan if no suitable index or no query params
            for row in self.data[table_name]:
                if all(row.get(k) == v for k, v in query_params.items()):
                    results.append(row)

        end_time = time.time()
        print(f"[{self.db_type}] Query executed in {end_time - start_time:.6f} seconds. Found {len(results)} results.")
        return results

    def add_index(self, table_name, column_name):
        if table_name in self.data:
            if column_name not in self.indexes[table_name]:
                self.indexes[table_name][column_name] = {}
                for i, row in enumerate(self.data[table_name]):
                    value = row.get(column_name)
                    if value not in self.indexes[table_name][column_name]:
                        self.indexes[table_name][column_name][value] = []
                    self.indexes[table_name][column_name][value].append(i)
                print(f"Index added to '{table_name}' on column '{column_name}'.")
            else:
                print(f"Index on '{table_name}.{column_name}' already exists.")
        else:
            print(f"Table '{table_name}' does not exist.")

# --- Simulation --- 

# PostgreSQL-like configuration (simulated)
pg_db = MockDatabase("PostgreSQL")
pg_db.create_table("users")

# Populate with some data
for i in range(1000):
    pg_db.insert_row("users", {"id": i, "name": f"User_{i}", "age": random.randint(18, 65), "city": random.choice(["Ankara", "Istanbul", "Izmir", "Antalya"])} )

# Add an index for optimization
pg_db.add_index("users", "city")

# Simulate a query - without index would be slow
print("\nSimulating PostgreSQL query for users in Istanbul:")
pg_db.query("users", {"city": "Istanbul"})

# Simulate an AI-related query (e.g., finding users with specific age ranges for model training)
print("\nSimulating PostgreSQL query for users aged 30-40:")
pg_db.query("users", {"age": random.randint(30, 40)})

# MySQL-like configuration (simulated)
mysql_db = MockDatabase("MySQL")
mysql_db.create_table("products")

# Populate with some data
for i in range(2000):
    mysql_db.insert_row("products", {"id": i, "name": f"Product_{i}", "price": round(random.uniform(10.0, 500.0), 2), "category": random.choice(["Electronics", "Books", "Clothing", "Home"])} )

# Add an index for optimization
mysql_db.add_index("products", "category")

# Simulate a query - without index would be slow
print("\nSimulating MySQL query for products in Electronics category:")
mysql_db.query("products", {"category": "Electronics"})

# Simulate an AI-related query (e.g., finding products with prices above a certain threshold for recommendation engine)
print("\nSimulating MySQL query for products with price > 200.00:")
# Note: This mock doesn't handle range queries efficiently without specific index types,
# but demonstrates the concept of querying for specific criteria.
mysql_db.query("products", {"price": 250.50}) # Simplified for demo

print("\nSimulation complete. Observe the query times to see the impact of indexing.")
