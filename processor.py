from typing import List
from .models import Paper
import csv
import sys
from io import StringIO
from datetime import date

class PaperProcessor:
    @staticmethod
    def filter_papers(papers: List[Paper]) -> List[Paper]:
        """Filter papers to only those with pharmaceutical/biotech affiliations"""
        return [
            paper for paper in papers 
            if any(paper._is_pharma_biotech(author.affiliation) 
                  for author in paper.authors 
                  if author.affiliation)
        ]
    
    @staticmethod
    def papers_to_csv(papers: List[Paper], output_file: Optional[str] = None) -> None:
        """Convert papers to CSV and write to file or stdout"""
        if not papers:
            print("No papers found matching the criteria.", file=sys.stderr)
            return
            
        output = StringIO() if output_file is None else open(output_file, 'w', newline='')
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'PubmedID',
            'Title',
            'Publication Date',
            'Non-academic Author(s)',
            'Company Affiliation(s)',
            'Corresponding Author Email'
        ])
        
        # Write rows
        for paper in papers:
            non_academic_authors = paper.get_non_academic_authors()
            company_affiliations = paper.get_company_affiliations()
            corresponding_email = paper.get_corresponding_author_email()
            
            writer.writerow([
                paper.pubmed_id,
                paper.title,
                paper.publication_date.strftime('%Y-%m-%d'),
                '; '.join(author.name for author in non_academic_authors),
                '; '.join(company_affiliations),
                corresponding_email if corresponding_email else ''
            ])
        
        if output_file is None:
            print(output.getvalue())
            output.close()
        else:
            output.close()
            print(f"Results saved to {output_file}", file=sys.stderr)
