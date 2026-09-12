from dataclasses import dataclass, asdict
import json
import time

@dataclass
class AgentProfile:
    agent_name: str
    model_engine: str
    temperature: float
    # We can assign default values easily
    max_retries: int = 3
    is_active: bool = True

print("--- INITIALIZING AGENT ---")
# Instantiate our agent profile
primary_agent = AgentProfile(
    agent_name="DataBot_v1", 
    model_engine="gpt-4-turbo", 
    temperature=0.2
)

print(f"Agent '{primary_agent.agent_name}' initialized on {primary_agent.model_engine}.")

config_filename = "agent_config.json"
with open(config_filename,"w") as file:
    json.dump(asdict(primary_agent), file, indent=4)


def mock_api_call(payload: dict, simulate_timeout=False, simulate_missing_key=False):
    print("\n--- INITIATING API CALL ---")
    
    try:
        # Simulating a scenario where the LLM forgets to return a mandatory key
        if simulate_missing_key:
            malformed_response = {"text": "Hello, world!"}
            # This will trigger a KeyError because "usage_metrics" doesn't exist
            tokens = malformed_response["usage_metrics"] 
            
        # Simulating a network timeout
        if simulate_timeout:
            time.sleep(1)
            raise TimeoutError("The LLM API endpoint took too long to respond.")
            
        print("API Call Successful!")
        return True

    # Catching SPECIFIC errors ensures we don't accidentally hide unrelated bugs
    except KeyError as e:
        print(f"[CRITICAL ERROR] LLM output parsing failed. Missing expected key: {e}")
        # In a real app, we might trigger an automatic retry here
        
    except TimeoutError as e:
        print(f"[NETWORK ERROR] {e} Switching to backup endpoint...")
        
    # The 'finally' block executes 100% of the time, regardless of success or failure.
    # Perfect for closing database connections or logging final timestamps.
    finally:
        print("API transaction finalized (Connection Closed).")

if __name__ == "__main__":
    # Test 1: Simulate a bad JSON output from the LLM
    mock_api_call(payload={"data": "test"}, simulate_missing_key=True)
    
    # Test 2: Simulate a server timeout
    mock_api_call(payload={"data": "test"}, simulate_timeout=True)