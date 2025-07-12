import requests
from typing import List, Optional
from datetime import datetime
from .models import Paper, Author
from xml.etree import ElementTree as ET
import time

class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    def __init__(self, email: str, api_key: Optional[str] = None, delay: float = 0.34):
        self.email = email
        self.api_key = api_key
        self.delay = delay  # PubMed recommends no more than 3 requests per second
        
    def search_papers(self, query: str, max_results: int = 100) -> List[Paper]:
        """Search PubMed for papers matching the query"""
        time.sleep(self.delay)
        
        # Step 1: Search and get PMIDs
        search_url = f"{self.BASE_URL}esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'email': self.email,
            'tool': 'research_paper_fetcher',
            'api_key': self.api_key
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        id_list = [id_elem.text for id_elem in root.findall('.//IdList/Id')]
        if not id_list:
            return []
        
        # Step 2: Fetch details for each paper
        return self.fetch_paper_details(id_list)
    
    def fetch_paper_details(self, pubmed_ids: List[str]) -> List[Paper]:
        """Fetch detailed information for a list of PubMed IDs"""
        if not pubmed_ids:
            return []
            
        time.sleep(self.delay)
        
        fetch_url = f"{self.BASE_URL}efetch.fcgi"
        params = {
            'db': 'pubmed',
            'id': ','.join(pubmed_ids),
            'retmode': 'xml',
            'email': self.email,
            'tool': 'research_paper_fetcher',
            'api_key': self.api_key
        }
        
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        
        papers = []
        root = ET.fromstring(response.content)
        
        for article in root.findall('.//PubmedArticle'):
            paper = self._parse_article(article)
            if paper:
                papers.append(paper)
        
        return papers
    
    def _parse_article(self, article: ET.Element) -> Optional[Paper]:
        """Parse a single article from PubMed XML"""
        try:
            # Extract PubMed ID
            pubmed_id = article.find('.//PMID').text
            
            # Extract title
            title = article.find('.//ArticleTitle').text or "No title available"
            if isinstance(title, str):
                title = ' '.join(title.split())  # Clean up whitespace
            
            # Extract publication date
            pub_date_elem = article.find('.//PubDate')
            year = pub_date_elem.find('Year').text if pub_date_elem is not None else None
            month = pub_date_elem.find('Month').text if pub_date_elem is not None else '01'
            day = pub_date_elem.find('Day').text if pub_date_elem is not None else '01'
            
            try:
                publication_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
            except (ValueError, AttributeError):
                publication_date = datetime.now().date()
            
            # Extract authors
            authors = []
            author_list = article.find('.//AuthorList')
            if author_list is not None:
                for author_elem in author_list.findall('Author'):
                    last_name = author_elem.find('LastName').text if author_elem.find('LastName') is not None else None
                    fore_name = author_elem.find('ForeName').text if author_elem.find('ForeName') is not None else None
                    if last_name and fore_name:
                        name = f"{fore_name} {last_name}"
                    elif last_name:
                        name = last_name
                    else:
                        continue
                    
                    # Check for corresponding author
                    is_corresponding = author_elem.get('ValidYN', 'N') == 'Y'
                    
                    # Extract affiliation
                    affiliation = author_elem.find('AffiliationInfo/Affiliation').text if author_elem.find('AffiliationInfo/Affiliation') is not None else None
                    
                    # Extract email (from affiliation or separate field)
                    email = None
                    if affiliation and '@' in affiliation:
                        # Try to extract email from affiliation
                        email_parts = [part for part in affiliation.split() if '@' in part]
                        if email_parts:
                            email = email_parts[0].strip('.,;')
                    
                    authors.append(Author(
                        name=name,
                        affiliation=affiliation,
                        is_corresponding=is_corresponding,
                        email=email
                    ))
            
            return Paper(
                pubmed_id=pubmed_id,
                title=title,
                publication_date=publication_date,
                authors=authors
            )
        except Exception as e:
            return None
