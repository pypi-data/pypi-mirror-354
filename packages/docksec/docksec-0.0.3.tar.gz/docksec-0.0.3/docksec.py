#!/usr/bin/env python3

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Docker Security Analysis Tool')
    parser.add_argument('dockerfile', help='Path to the Dockerfile to analyze')
    parser.add_argument('-i', '--image', help='Docker image ID to scan (optional)')
    parser.add_argument('-o', '--output', help='Output file for the report (default: security_report.txt)')
    parser.add_argument('--ai-only', action='store_true', help='Run only AI-based recommendations')
    parser.add_argument('--scan-only', action='store_true', help='Run only Dockerfile/image scanning')
    
    args = parser.parse_args()
    
    # Validate that the Dockerfile exists
    if not os.path.isfile(args.dockerfile):
        print(f"Error: Dockerfile not found at {args.dockerfile}")
        sys.exit(1)
    
    # Determine which tools to run
    run_ai = not args.scan_only
    run_scan = not args.ai_only
    
    if not run_ai and not run_scan:
        run_ai = run_scan = True  # Run both by default
    
    # Run the AI-based recommendation tool
    if run_ai:
        print("Running AI-based Dockerfile analysis...")
        try:
            import main
            # Assuming main.py has a main function or similar entry point
            # You might need to adjust this based on how main.py is structured
            main.main([args.dockerfile])  # or however main.py expects arguments
        except ImportError:
            print("Error: AI analysis module not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error running AI analysis: {e}")
    
    # Run the scanner tool
    if run_scan:
        print("Running Dockerfile and image scanner...")
        try:
            import docker_scanner
            # Assuming docker_scanner.py has a main function
            # You might need to adjust this based on how docker_scanner.py is structured
            scanner_args = [args.dockerfile]
            if args.image:
                scanner_args.append(args.image)
            docker_scanner.main(scanner_args)  # or however docker_scanner.py expects arguments
        except ImportError:
            print("Error: Scanner module not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error running scanner: {e}")
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()