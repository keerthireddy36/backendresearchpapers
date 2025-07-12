from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class Author:
    name: str
    affiliation: Optional[str] = None
    is_corresponding: bool = False
    email: Optional[str] = None

@dataclass
class Paper:
    pubmed_id: str
    title: str
    publication_date: date
    authors: List[Author]
    
    def get_non_academic_authors(self) -> List[Author]:
        return [author for author in self.authors if self._is_non_academic(author)]
    
    def get_company_affiliations(self) -> List[str]:
        companies = set()
        for author in self.authors:
            if author.affiliation and self._is_pharma_biotech(author.affiliation):
                companies.add(author.affiliation)
        return list(companies)
    
    def get_corresponding_author_email(self) -> Optional[str]:
        for author in self.authors:
            if author.is_corresponding and author.email:
                return author.email
        return None
    
    @staticmethod
    def _is_non_academic(author: Author) -> bool:
        if not author.affiliation:
            return False
            
        academic_keywords = [
            'university', 'college', 'institute', 'school', 
            'academy', 'hospital', 'labs?', 'research', 'foundation'
        ]
        affiliation_lower = author.affiliation.lower()
        return not any(keyword in affiliation_lower for keyword in academic_keywords)
    
    @staticmethod
    def _is_pharma_biotech(affiliation: str) -> bool:
        if not affiliation:
            return False
            
        industry_keywords = [
            'pharma', 'biotech', 'pharmaceutical', 'bio-tech',
            'genentech', 'pfizer', 'novartis', 'roche', 'merck',
            'gsk', 'sanofi', 'astrazeneca', 'bayer', 'eli lilly',
            'bristol-myers', 'abbvie', 'amgen', 'biogen', 'gilead'
        ]
        affiliation_lower = affiliation.lower()
        return any(keyword in affiliation_lower for keyword in industry_keywords)
