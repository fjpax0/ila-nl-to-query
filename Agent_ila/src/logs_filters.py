import json
import os

def append_to_json(file_path: str, generated_ila_filter: dict, user_query: str, ila_result: dict):
    """
    Appends the generated filter and user query to a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        generated_ila_filter (dict): The generated filter data to append.
        user_query (str): The user query to append.
        ila_result (dict): The ILA result to append.
    """
    # Read existing data from the file if it exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []  # If file is empty or invalid, start with an empty list
    else:
        existing_data = []

    # Append the new entry
    new_entry = {"user_query": user_query, "generated_ila_filter": generated_ila_filter, 'ila_result': ila_result}
    existing_data.append(new_entry)

    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

# Example usage
# if __name__ == "__main__":
    # file_path = 'generated_f_prompt.json'
    # generated_ila_filter = {"example_key": "example_value"}  # Replace with actual data
    # user_query = "What is the average ROP in the Tor formation?"
    # append_to_json(file_path, generated_ila_filter, user_query, )
