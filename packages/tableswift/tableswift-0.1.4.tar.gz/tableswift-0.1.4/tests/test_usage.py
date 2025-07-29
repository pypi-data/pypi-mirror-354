import tableswift as ts
from tableswift import generate_labels
from tableswift import generate_code



if __name__ == "__main__":
    ts.configure(api_key="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")
    
    # Generate labels for the samples
    labeled_data = ts.generate_labels(instruction="label the input samples", 
                                      task="data_transformation",
                                      column_name="name",
                                      demonstrations=[{"Input": "sample1", "Output": "label1"},
                                                     {"Input": "sample2", "Output": "label2"}],
                                      samples_to_label=[{"Input": "sample1", "Output": ""},
                                                        {"Input": "sample2", "Output": ""},
                                                        {"Input": "sample3", "Output": ""}])
    print("labeled_data:")
    for data in labeled_data:
        print(data)
    
    # Generate code for the package
    code, router_code = ts.generate_code(instruction="Transform input into output",
                     task="data_transformation",
                     samples=[{"Input": "sample1", "Output": "label1"},
                              {"Input": "sample2", "Output": "label2"}],
                     lang="python",
                     num_trials=1,
                     num_retry=3,
                     num_iterations=1)
    print("Generated Code:")
    print(code)
    print("Router Code:")
    print(router_code)
    # Execute the generated code
    inputs = [{"Input": "sample1", "Output": ""},
              {"Input": "sample2", "Output": ""},
              {"Input": "sample3", "Output": ""}]
    results, invalid_data = ts.execute_code(code=code,
                                            instruction="Transform input into output",
                                            task="data_transformation",
                                            lang="python",
                                            inputs=inputs,
                                            samples=[{"Input": "sample1", "Output": "label1"},
                                                     {"Input": "sample2", "Output": "label2"}],
                                            router_code=router_code)
    print("Execution Results:")
    for result in results:
        print(result)
    
    