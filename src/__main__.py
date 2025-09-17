#!/usr/bin/env python3
"""Quick test script for the simplified application."""

from src.client import VitosClient

def main():
    print("Testing simplified Vito's Pizza Cafe application...")
    print("=" * 60)

    # Create client
    client = VitosClient(thread_id="test")

    # Test simple queries
    test_queries = [
        "What's on the menu?",
        "Do you deliver?",
        "How can I create an account?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)
        response = client.query(query)
        print(f"Response: {response}")
        print()

if __name__ == "__main__":
    main()