from ddtrace import tracer
import time
import random
import string

@tracer.wrap()
def generate_random_string(length):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@tracer.wrap()
def process_data(data):
    """Simulate data processing."""
    time.sleep(random.uniform(0.1, 0.5))
    return data.upper()

@tracer.wrap()
def calculate_checksum(data):
    """Calculate a simple checksum."""
    return sum(ord(c) for c in data)

@tracer.wrap()
def do_some_work():
    """Perform a series of operations."""
    print("Starting do_some_work()")
    
    with tracer.trace('generate_data'):
        data = generate_random_string(random.randint(10, 20))
    
    with tracer.trace('process_data'):
        processed_data = process_data(data)
    
    with tracer.trace('calculate_checksum'):
        checksum = calculate_checksum(processed_data)
    
    time.sleep(random.uniform(0.1, 0.3))
    
    result = {
        'original': data,
        'processed': processed_data,
        'checksum': checksum
    }
    
    print(f"Finished do_some_work(), result: {result}")
    return result

@tracer.wrap()
def analyze_result(result):
    """Analyze the result of do_some_work."""
    time.sleep(random.uniform(0.2, 0.5))
    analysis = {
        'original_length': len(result['original']),
        'processed_length': len(result['processed']),
        'checksum_valid': result['checksum'] % 2 == 0
    }
    return analysis

def main():
    """The main function that generates traces."""
    iteration = 0
    while True:
        iteration += 1
        print(f"\nStarting main operation trace (Iteration {iteration})")
        
        with tracer.trace('main_operation') as span:
            span.set_tag('iteration', iteration)
            
            with tracer.trace('work_phase'):
                result = do_some_work()
            
            with tracer.trace('analysis_phase'):
                analysis = analyze_result(result)
            
            span.set_tag('checksum', result['checksum'])
            span.set_tag('checksum_valid', analysis['checksum_valid'])
        
        print(f"Result: {result}")
        print(f"Analysis: {analysis}")
        print(f"Finished main operation trace (Iteration {iteration})")
        
        sleep_time = random.uniform(1.0, 3.0)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
