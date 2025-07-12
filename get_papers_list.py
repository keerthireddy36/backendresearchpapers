#!/usr/bin/env python
import argparse
from typing import Optional
from research_paper_fetcher.api_client import PubMedClient
from research_paper_fetcher.processor import PaperProcessor
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed with pharmaceutical/biotech affiliations."
    )
    parser.add_argument(
        'query',
        type=str,
        help='PubMed search query'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Output CSV file path (default: print to stdout)',
        default=None
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug output'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=100,
        help='Maximum number of results to fetch (default: 100)'
    )
    parser.add_argument(
        '--email',
        type=str,
        default='your-email@example.com',
        help='Email address for PubMed API (required)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='PubMed API key (optional)'
    )
    
    args = parser.parse_args()
    
    if args.debug:
        print(f"Debug: Query: {args.query}", file=sys.stderr)
        print(f"Debug: Max results: {args.max_results}", file=sys.stderr)
    
    try:
        # Initialize PubMed client
        client = PubMedClient(email=args.email, api_key=args.api_key)
        
        if args.debug:
            print("Debug: Fetching papers...", file=sys.stderr)
        
        # Fetch papers
        papers = client.search_papers(args.query, max_results=args.max_results)
        
        if args.debug:
            print(f"Debug: Found {len(papers)} papers before filtering", file=sys.stderr)
        
        # Filter papers
        filtered_papers = PaperProcessor.filter_papers(papers)
        
        if args.debug:
            print(f"Debug: Found {len(filtered_papers)} papers after filtering", file=sys.stderr)
        
        # Output results
        PaperProcessor.papers_to_csv(filtered_papers, args.file)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
