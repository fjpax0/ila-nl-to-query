import json
import time
import logging
from log_utils.logger_config import logger

def correct_json_with_llm(input_json, client, max_retries=2, backoff_factor=2):
    """
    Corrects mismatched curly braces in a JSON string using a language model with limited retries.

    Args:
        input_json (str): The JSON string to be corrected.
        client: The HTTP client instance used to make API calls.
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
        backoff_factor (int, optional): Factor by which the wait time increases after each retry. Defaults to 2.

    Returns:
        str: The corrected JSON string.

    Raises:
        ValueError: If the JSON cannot be corrected after the maximum number of retries.
        RuntimeError: If there's an issue with the API request.
    """

    # Define the system prompt
    system_prompt = """
You are an expert JSON validator. Your primary task is to analyze JSON structures provided by users to ensure they are syntactically correct, with particular attention to the proper use and balancing of curly braces `{}`. 

When given a JSON input:
1. **Check for Balanced Braces**: Ensure that every opening brace `{` has a corresponding closing brace `}`.
2. **Validate Syntax**: Verify that the JSON adheres to standard syntax rules, including proper use of commas, colons, quotes, and brackets.
3. **Provide Feedback**:
   - If the JSON is valid, confirm its correctness.
   - If there are errors, identify the specific issues and do the corrections into json format.

**Guidelines**:
- Do not execute or interpret the data within the JSON; focus solely on its structural validity.
- Present your findings in a clear and organized manner, using formatting (like code blocks) to enhance readability.
- Maintain a professional and helpful tone, guiding the user to understand and resolve any issues with their JSON.

**Example Interaction**:

*User Input with excess } *:
{"filter": {"exists": {"property": ["test_dw_well_logs", "test_depth_logs_container", "dailyDrillingReport"]}}, "aggregates": {"important_events": {"uniqueValues": {"property": ["test_dw_well_logs", "test_depth_logs_container", "dailyDrillingReport"], "aggregates": {"count_events": {"count": {"property": ["test_dw_well_logs", "test_depth_logs_container", "dailyDrillingReport"]}}}}}}}}

Sample corrected output:
{"filter":{"exists":{"property":["test_dw_well_logs","test_depth_logs_container","dailyDrillingReport"]}},"aggregates":{"important_events":{"uniqueValues":{"property":["test_dw_well_logs","test_depth_logs_container","dailyDrillingReport"],"aggregates":{"count_events":{"count":{"property":["test_dw_well_logs","test_depth_logs_container","dailyDrillingReport"]}}}}}}}

output: Strictly: the output should just be the json nothing else.

"""

    # Initialize attempt counter and storage for the last incorrect JSON
    attempt = 0
    last_corrected_json = None

    while attempt < max_retries:
        try:
            attempt += 1
            logger.info(f"Attempt {attempt} of {max_retries} to correct JSON.")

            # Construct the user message
            user_message = f"json to fix: {input_json}"

            # Prepare the request payload
            body = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0,
                "model": "gpt-4o-mini",
            }

            # Define the API endpoint
            proxy_path = f"/api/v1/projects/{client.config.project}/ai/chat/completions"

            # Make the API call to the language model
            response = client.post(url=proxy_path, json=body).json()

            # Extract the assistant's reply
            corrected_json = response['choices'][0]['message']['content'].strip()
            last_corrected_json = corrected_json  # Store the last attempted corrected JSON
            
            # Attempt to validate the corrected JSON
            try:
                print('last_corrected_json', last_corrected_json)
                logger.info("Validating the corrected JSON.")
                json.loads(last_corrected_json)
                # Re-serialize to ensure proper formatting
                
                logger.info("JSON corrected and validated successfully.")
                return last_corrected_json  # Success, exit the function
            except json.JSONDecodeError as e:
                logger.warning(f"JSONDecodeError on attempt {attempt}: {e}")
                if attempt < max_retries:
                    sleep_time = backoff_factor ** (attempt - 1)
                    logger.info(f"Retrying after {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error("Maximum retry attempts reached. Unable to correct JSON.")
                    logger.error(f"Final incorrect JSON: {last_corrected_json}")
                    raise ValueError(f"Unable to correct JSON after {max_retries} attempts.") from e

        except Exception as e:
            logger.exception(f"An error occurred on attempt {attempt}: {e}")
            if attempt < max_retries:
                sleep_time = backoff_factor ** (attempt - 1)
                logger.info(f"Retrying after {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error("Maximum retry attempts reached. Unable to correct JSON due to repeated errors.")
                if last_corrected_json:
                    logger.error(f"Final incorrect JSON: {last_corrected_json}")
                raise RuntimeError(f"Unable to correct JSON after {max_retries} attempts due to errors.") from e

    # After all retries are exhausted, attempt to fix by removing the final '}'
    if last_corrected_json:
        logger.info("Attempting to fix JSON by removing the final '}'.")
        fixed_json = last_corrected_json.rstrip('}')
        try:
            logger.info("Validating the JSON after removing the final '}'.")
            json.loads(fixed_json)
            logger.info("JSON fixed by removing the final '}' and validated successfully.")
            return fixed_json  # Return the fixed JSON
        except json.JSONDecodeError as e:
            logger.error("Unable to fix JSON by removing the final '}'.")
            logger.error(f"Final attempted JSON after removal: {fixed_json}")
            raise ValueError(f"Unable to correct JSON after {max_retries} attempts.") from e

    # If all retries are exhausted without a valid JSON, raise an error
    logger.error(f"Final incorrect JSON after all retries: {last_corrected_json}")
    raise ValueError(f"Unable to correct JSON after {max_retries} attempts.")
